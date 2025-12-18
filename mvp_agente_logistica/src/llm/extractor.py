"""
Extractor de campos estructurados usando LLM
"""
from typing import Any, Dict, Optional

from dateutil import parser
from pydantic import ValidationError

from ..core.config import Config
from ..core.logger import get_logger
from ..models.document import DocumentType
from ..models.schemas import (
    AlbaranSchema,
    NotaRecepcionSchema,
    OrdenEnvioSchema,
    ParteTransporteSchema
)
from .ollama_client import OllamaClient
from .prompts import EXTRACTION_PROMPTS, EXTRACTION_SYSTEM_PROMPT


class FieldExtractor:
    """Extrae campos estructurados usando LLM"""

    def __init__(self, llm_client: Optional[OllamaClient] = None, config: Optional[Config] = None):
        """
        Inicializa el extractor

        Args:
            llm_client: Cliente LLM (crea uno nuevo si es None)
            config: Configuracion del sistema
        """
        self.config = config
        self.logger = get_logger(__name__)

        if llm_client is None:
            self.llm = OllamaClient(config)
        else:
            self.llm = llm_client

        # Mapeo de tipos a schemas
        self.schema_map = {
            DocumentType.ALBARAN: AlbaranSchema,
            DocumentType.ORDEN_ENVIO: OrdenEnvioSchema,
            DocumentType.NOTA_RECEPCION: NotaRecepcionSchema,
            DocumentType.PARTE_TRANSPORTE: ParteTransporteSchema
        }

    def extract_fields(
        self,
        ocr_text: str,
        doc_type: DocumentType,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Extrae campos segun template del tipo de documento

        Args:
            ocr_text: Texto extraido por OCR
            doc_type: Tipo de documento
            max_retries: Numero maximo de reintentos si falla la validacion

        Returns:
            Diccionario con campos extraidos y validados

        Raises:
            ValueError: Si no se pueden extraer los campos
        """
        self.logger.info(f"Extrayendo campos para {doc_type.value}...")

        # Obtener prompt segun tipo
        prompt_template = EXTRACTION_PROMPTS.get(doc_type.value)
        if not prompt_template:
            raise ValueError(f"No hay template de extraccion para {doc_type.value}")

        # Truncar texto si es muy largo
        max_length = 3000
        if len(ocr_text) > max_length:
            ocr_text_truncated = ocr_text[:max_length] + "..."
            self.logger.debug(f"Texto OCR truncado a {max_length} caracteres")
        else:
            ocr_text_truncated = ocr_text

        # Generar prompt
        prompt = prompt_template.format(ocr_text=ocr_text_truncated)

        # Intentar extraccion con reintentos
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.debug(f"Intento de extraccion {attempt}/{max_retries}")

                # Llamar al LLM
                extracted_data = self.llm.generate_json(
                    prompt=prompt,
                    system=EXTRACTION_SYSTEM_PROMPT
                )

                # Normalizar datos
                normalized_data = self._normalize_data(extracted_data, doc_type)

                # Validar con schema Pydantic
                schema_class = self.schema_map[doc_type]
                validated = schema_class(**normalized_data)

                self.logger.info("Campos extraidos y validados exitosamente")
                return validated.model_dump()

            except ValidationError as e:
                self.logger.warning(f"Error de validacion en intento {attempt}: {e}")

                if attempt < max_retries:
                    # Agregar errores al prompt para retry
                    error_msg = self._format_validation_errors(e)
                    prompt = f"""{prompt}

ATENCION: El intento anterior tuvo estos errores de validacion:
{error_msg}

Por favor, corrige estos errores en tu respuesta."""
                else:
                    raise ValueError(f"No se pudieron validar los campos despues de {max_retries} intentos: {e}")

            except Exception as e:
                self.logger.error(f"Error durante extraccion: {e}")
                if attempt == max_retries:
                    raise ValueError(f"Error durante extraccion de campos: {e}")

        raise ValueError("Extraccion fallida")

    def _normalize_data(self, data: Dict[str, Any], doc_type: DocumentType) -> Dict[str, Any]:
        """
        Normaliza datos extraidos (fechas, numeros, etc)

        Args:
            data: Datos extraidos
            doc_type: Tipo de documento

        Returns:
            Datos normalizados
        """
        normalized = data.copy()

        # Normalizar fechas
        date_fields = ['fecha_emision', 'fecha_orden', 'fecha_recepcion', 'fecha_envio_programada']
        for field in date_fields:
            if field in normalized and normalized[field]:
                normalized[field] = self._normalize_date(normalized[field])

        # Normalizar datetime
        datetime_fields = ['fecha_salida', 'fecha_llegada_estimada']
        for field in datetime_fields:
            if field in normalized and normalized[field]:
                normalized[field] = self._normalize_datetime(normalized[field])

        return normalized

    def _normalize_date(self, date_str: str) -> str:
        """Normaliza fecha a formato ISO YYYY-MM-DD"""
        try:
            parsed = parser.parse(date_str, dayfirst=True)
            return parsed.strftime("%Y-%m-%d")
        except Exception as e:
            self.logger.warning(f"No se pudo normalizar fecha '{date_str}': {e}")
            return date_str

    def _normalize_datetime(self, datetime_str: str) -> str:
        """Normaliza datetime a formato ISO"""
        try:
            parsed = parser.parse(datetime_str, dayfirst=True)
            return parsed.strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            self.logger.warning(f"No se pudo normalizar datetime '{datetime_str}': {e}")
            return datetime_str

    def _format_validation_errors(self, error: ValidationError) -> str:
        """Formatea errores de validacion para el LLM"""
        errors = []
        for err in error.errors():
            field = ".".join(str(loc) for loc in err['loc'])
            msg = err['msg']
            errors.append(f"- Campo '{field}': {msg}")

        return "\n".join(errors)
