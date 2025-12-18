"""
Cliente para interactuar con Ollama
"""
import json
from typing import Any, Dict, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from ..core.config import Config
from ..core.logger import get_logger


class OllamaClient:
    """Cliente para interactuar con Ollama"""

    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa el cliente Ollama

        Args:
            config: Configuracion del sistema
        """
        self.config = config
        self.logger = get_logger(__name__)

        if config:
            self.model = config.llm.model
            self.base_url = config.llm.base_url
            self.timeout = config.llm.timeout_seconds
            self.max_retries = config.llm.max_retries
            self.temperature = config.llm.temperature
        else:
            self.model = "llama3:8b"
            self.base_url = "http://localhost:11434"
            self.timeout = 30
            self.max_retries = 3
            self.temperature = 0.1

        # Verificar conexion con Ollama
        self._verify_connection()

    def _verify_connection(self) -> None:
        """Verifica que Ollama este ejecutandose"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                self.logger.info(f"Ollama conectado. Modelos disponibles: {model_names}")

                # Verificar que el modelo configurado existe
                if not any(self.model in name for name in model_names):
                    self.logger.warning(
                        f"Modelo '{self.model}' no encontrado. "
                        f"Ejecuta: ollama pull {self.model}"
                    )
            else:
                raise ConnectionError(f"Ollama respondio con codigo: {response.status_code}")

        except requests.exceptions.RequestException as e:
            self.logger.error(f"No se pudo conectar con Ollama: {e}")
            raise ConnectionError(
                f"No se pudo conectar con Ollama en {self.base_url}. "
                "Asegurate de que Ollama este ejecutandose (ollama serve)"
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Genera respuesta del LLM

        Args:
            prompt: Prompt para el modelo
            system: System prompt (opcional)
            temperature: Temperature para generacion (usa config si None)

        Returns:
            Respuesta del modelo

        Raises:
            RuntimeError: Si la generacion falla
        """
        if temperature is None:
            temperature = self.temperature

        self.logger.debug(f"Generando con modelo: {self.model}")

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }

            if system:
                payload["system"] = system

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )

            if response.status_code != 200:
                raise RuntimeError(f"Ollama respondio con codigo: {response.status_code}")

            result = response.json()
            generated_text = result.get('response', '')

            self.logger.debug(f"Respuesta generada ({len(generated_text)} chars)")
            return generated_text

        except requests.exceptions.Timeout:
            self.logger.error("Timeout al generar con Ollama")
            raise RuntimeError("Timeout al generar con Ollama")
        except Exception as e:
            self.logger.error(f"Error al generar con Ollama: {e}")
            raise RuntimeError(f"Error al generar con Ollama: {e}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate_json(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Genera respuesta estructurada en JSON

        Args:
            prompt: Prompt para el modelo
            system: System prompt (opcional)
            temperature: Temperature para generacion (usa config si None)

        Returns:
            Respuesta del modelo parseada como JSON

        Raises:
            RuntimeError: Si la generacion falla
            ValueError: Si la respuesta no es JSON valido
        """
        # Agregar instrucciones para formato JSON al prompt
        json_prompt = f"""{prompt}

IMPORTANTE: Responde UNICAMENTE con un objeto JSON valido, sin texto adicional antes o despues del JSON."""

        response_text = self.generate(json_prompt, system, temperature)

        # Intentar extraer JSON de la respuesta
        try:
            # Buscar el JSON en la respuesta (a veces el modelo agrega texto extra)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')

            if start_idx == -1 or end_idx == -1:
                raise ValueError("No se encontro JSON en la respuesta")

            json_str = response_text[start_idx:end_idx + 1]
            parsed_json = json.loads(json_str)

            return parsed_json

        except json.JSONDecodeError as e:
            self.logger.error(f"Error al parsear JSON: {e}")
            self.logger.debug(f"Respuesta recibida: {response_text}")
            raise ValueError(f"La respuesta no es JSON valido: {e}")

    def check_health(self) -> bool:
        """
        Verifica el estado de Ollama

        Returns:
            True si Ollama esta disponible
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
