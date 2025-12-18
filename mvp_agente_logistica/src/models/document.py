"""
Modelos de datos geometricos y de OCR
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class DocumentType(str, Enum):
    """Tipos de documentos soportados"""
    ALBARAN = "ALBARAN"
    ORDEN_ENVIO = "ORDEN_ENVIO"
    NOTA_RECEPCION = "NOTA_RECEPCION"
    PARTE_TRANSPORTE = "PARTE_TRANSPORTE"


class BBox(BaseModel):
    """Bounding box de una region en el documento"""
    x1: int = Field(..., ge=0, description="Coordenada x superior izquierda")
    y1: int = Field(..., ge=0, description="Coordenada y superior izquierda")
    x2: int = Field(..., ge=0, description="Coordenada x inferior derecha")
    y2: int = Field(..., ge=0, description="Coordenada y inferior derecha")

    model_config = {"frozen": True}  # Inmutable

    @field_validator('x2')
    @classmethod
    def x2_must_be_greater_than_x1(cls, v: int, info) -> int:
        """Valida que x2 > x1"""
        values = info.data
        if 'x1' in values and v <= values['x1']:
            raise ValueError('x2 debe ser mayor que x1')
        return v

    @field_validator('y2')
    @classmethod
    def y2_must_be_greater_than_y1(cls, v: int, info) -> int:
        """Valida que y2 > y1"""
        values = info.data
        if 'y1' in values and v <= values['y1']:
            raise ValueError('y2 debe ser mayor que y1')
        return v

    def area(self) -> int:
        """Calcula area del bounding box"""
        return (self.x2 - self.x1) * (self.y2 - self.y1)

    def center(self) -> tuple[int, int]:
        """Retorna el centro del bounding box"""
        return ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    def width(self) -> int:
        """Retorna el ancho"""
        return self.x2 - self.x1

    def height(self) -> int:
        """Retorna el alto"""
        return self.y2 - self.y1


class OCRResult(BaseModel):
    """Resultado de OCR por linea"""
    text: str = Field(..., description="Texto extraido")
    bbox: BBox = Field(..., description="Bounding box del texto")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza (0-1)")

    model_config = {"frozen": True}

    @field_validator('text')
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        """Valida que el texto no este vacio"""
        if not v or v.strip() == "":
            raise ValueError("El texto no puede estar vacio")
        return v.strip()


class TableCell(BaseModel):
    """Celda de tabla"""
    row: int = Field(..., ge=0, description="Numero de fila")
    col: int = Field(..., ge=0, description="Numero de columna")
    text: str = Field(..., description="Texto de la celda")
    bbox: BBox = Field(..., description="Bounding box de la celda")

    model_config = {"frozen": True}


class ProcessedDocument(BaseModel):
    """Documento procesado completo"""
    file_path: str = Field(..., description="Ruta al archivo original")
    file_name: str = Field(..., description="Nombre del archivo")
    file_size_kb: float = Field(..., ge=0, description="Tamano del archivo en KB")
    processing_timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de procesamiento")
    processing_time_seconds: float = Field(..., ge=0, description="Tiempo de procesamiento en segundos")
    agent_version: str = Field(default="1.0.0", description="Version del agente")

    # Clasificacion
    document_type: DocumentType = Field(..., description="Tipo de documento")
    classification_confidence: float = Field(..., ge=0.0, le=1.0, description="Confianza de clasificacion")

    # OCR
    ocr_engine_used: str = Field(..., description="Motor OCR utilizado")
    ocr_average_confidence: float = Field(..., ge=0.0, le=1.0, description="Confianza promedio OCR")
    total_text_blocks: int = Field(..., ge=0, description="Total de bloques de texto")
    tables_detected: int = Field(default=0, ge=0, description="Numero de tablas detectadas")
    signatures_detected: bool = Field(default=False, description="Si se detectaron firmas")
    stamps_detected: bool = Field(default=False, description="Si se detectaron sellos")

    # Campos extraidos (se llenara segun el tipo de documento)
    extracted_fields: dict = Field(..., description="Campos extraidos del documento")

    # Validacion
    validation_status: str = Field(..., description="Estado de validacion (valid, warning, invalid)")
    validation_errors: List[str] = Field(default_factory=list, description="Errores de validacion")
    validation_warnings: List[str] = Field(default_factory=list, description="Warnings de validacion")

    # OCR Raw (opcional)
    raw_ocr_text: Optional[str] = Field(None, description="Texto OCR completo sin procesar")
