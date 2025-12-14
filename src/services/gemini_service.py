"""
Servicio de integración con Google Gemini API.

Este módulo maneja la extracción de entidades de contactos
usando el modelo Gemini de Google.
"""

import json
import re
from typing import Dict, Any, Optional
import asyncio

import google.generativeai as genai

from ..utils.logger import get_logger

logger = get_logger(__name__)


# Prompt de extracción mejorado para forzar JSON puro
EXTRACTION_PROMPT = """Extrae la información del siguiente mensaje y responde SOLAMENTE con JSON válido, SIN texto adicional, SIN markdown, SIN explicaciones.

Formato JSON requerido (una sola línea):
{{"nombre": "nombre completo", "telefono": "solo dígitos", "quien_lo_recomendo": "nombre del referido"}}

Reglas de extracción:
- nombre: nombre completo del contacto
- telefono: solo números, sin espacios ni guiones
- quien_lo_recomendo: nombre de quien recomienda (busca: "recomendado por", "de parte de", "me lo pasó", "referido por")
- Si falta algún dato, usa cadena vacía ""

IMPORTANTE: Tu respuesta debe ser SOLAMENTE el objeto JSON, nada más.

Mensaje: {message}

JSON:"""


class GeminiService:
    """
    Servicio para extracción de entidades usando Google Gemini.

    Attributes:
        api_key: API key de Google Gemini.
        model_name: Nombre del modelo a utilizar.
        timeout: Timeout en segundos para las peticiones.
        model: Instancia del modelo de Gemini.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-1.5-flash",
        timeout: int = 30
    ):
        """
        Inicializa el servicio de Gemini.

        Args:
            api_key: API key de Google Gemini.
            model_name: Nombre del modelo (default: gemini-1.5-flash).
            timeout: Timeout en segundos (default: 30).

        Example:
            >>> service = GeminiService(api_key="your-api-key")
        """
        self.api_key = api_key
        self.model_name = model_name
        self.timeout = timeout

        # Configurar Gemini
        genai.configure(api_key=api_key)

        # Configuración de generación para forzar respuestas JSON
        generation_config = {
            "temperature": 0.1,  # Baja temperatura para respuestas más deterministas
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )

        logger.info(
            "gemini_service_initialized",
            model_name=model_name,
            timeout=timeout
        )

    async def extract_contact_info(self, message_text: str) -> Dict[str, Any]:
        """
        Extrae información de contacto de un mensaje de texto.

        Args:
            message_text: Texto del mensaje a procesar.

        Returns:
            dict con keys:
                - success: bool indicando si la extracción fue exitosa
                - data: dict con nombre, telefono, quien_lo_recomendo
                - error: str con mensaje de error (si success=False)

        Example:
            >>> service = GeminiService(api_key="key")
            >>> result = await service.extract_contact_info(
            ...     "Juan 3001234567 ref María"
            ... )
            >>> result["success"]
            True
            >>> result["data"]["nombre"]
            'Juan'
        """
        logger.info(
            "extracting_contact_info",
            message_length=len(message_text)
        )

        try:
            # Preparar el prompt
            prompt = EXTRACTION_PROMPT.format(message=message_text)

            # Llamar a Gemini API de forma asíncrona con timeout
            response = await asyncio.wait_for(
                self._call_gemini_async(prompt),
                timeout=self.timeout
            )

            # Extraer y parsear la respuesta
            response_text = response.text.strip()

            logger.debug(
                "gemini_response_received",
                response_length=len(response_text)
            )

            # Parsear JSON de la respuesta
            contact_data = self._parse_json_response(response_text)

            if not contact_data:
                logger.error("failed_to_parse_gemini_response")
                return {
                    "success": False,
                    "error": "No se pudo parsear la respuesta de Gemini"
                }

            # Normalizar teléfono
            if contact_data.get("telefono"):
                contact_data["telefono"] = self._normalize_phone(
                    contact_data["telefono"]
                )

            logger.info(
                "contact_extraction_successful",
                nombre=contact_data.get("nombre", ""),
                has_telefono=bool(contact_data.get("telefono")),
                has_referido=bool(contact_data.get("quien_lo_recomendo"))
            )

            return {
                "success": True,
                "data": contact_data
            }

        except asyncio.TimeoutError:
            logger.error(
                "gemini_timeout",
                timeout=self.timeout
            )
            return {
                "success": False,
                "error": f"Timeout al procesar con Gemini ({self.timeout}s)"
            }

        except Exception as e:
            logger.error(
                "gemini_extraction_failed",
                error=str(e),
                error_type=type(e).__name__
            )
            return {
                "success": False,
                "error": f"Error al procesar con Gemini: {str(e)}"
            }

    async def _call_gemini_async(self, prompt: str):
        """
        Llama a la API de Gemini de forma asíncrona.

        Args:
            prompt: Prompt a enviar a Gemini.

        Returns:
            Respuesta de Gemini.
        """
        # Ejecutar la llamada síncrona en un thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.model.generate_content,
            prompt
        )

    def _parse_json_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        Parsea la respuesta JSON de Gemini.

        Args:
            response_text: Texto de respuesta de Gemini.

        Returns:
            Diccionario con datos extraídos o None si falla.
        """
        # Limpiar respuesta: remover markdown, espacios, saltos de línea extras
        cleaned = response_text.strip()

        # Remover bloques de código markdown si existen (```json ... ```)
        if cleaned.startswith("```"):
            cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)
            cleaned = cleaned.strip()

        try:
            # Intentar parsear directamente
            data = json.loads(cleaned)
            return data

        except json.JSONDecodeError:
            # Intentar extraer JSON de la respuesta
            # Gemini a veces incluye texto adicional
            logger.debug("attempting_to_extract_json_from_response")

            # Buscar patrón JSON en la respuesta (mejorado para multilínea)
            # Busca desde { hasta } incluyendo todo el contenido
            json_match = re.search(r'\{.*?\}', response_text, re.DOTALL)

            if json_match:
                try:
                    json_str = json_match.group()
                    logger.debug(
                        "extracted_json",
                        json_preview=json_str[:100]
                    )
                    data = json.loads(json_str)
                    return data
                except json.JSONDecodeError as e:
                    logger.warning(
                        "json_parse_failed_after_extraction",
                        error=str(e),
                        extracted_text=json_str[:200]
                    )

            logger.warning(
                "failed_to_parse_json",
                response_preview=response_text[:200]
            )
            return None

    def _normalize_phone(self, phone: str) -> str:
        """
        Normaliza un número de teléfono.

        Args:
            phone: Número de teléfono en cualquier formato.

        Returns:
            Número normalizado.

        Example:
            >>> service = GeminiService(api_key="key")
            >>> service._normalize_phone("300 123 4567")
            '+573001234567'
            >>> service._normalize_phone("+57 315-789-4561")
            '+573157894561'
        """
        if not phone:
            return ""

        # Remover todo excepto dígitos y +
        cleaned = re.sub(r"[^\d+]", "", phone)

        # Si no tiene código de país, agregar +57 (Colombia)
        if not cleaned.startswith("+"):
            cleaned = "+57" + cleaned

        return cleaned

    async def health_check(self) -> bool:
        """
        Verifica que el servicio de Gemini esté funcionando.

        Returns:
            True si el servicio está disponible, False en caso contrario.
        """
        try:
            response = await asyncio.wait_for(
                self._call_gemini_async("Test: responde con OK"),
                timeout=10
            )
            logger.info("gemini_health_check_passed")
            return True

        except Exception as e:
            logger.error(
                "gemini_health_check_failed",
                error=str(e)
            )
            return False
