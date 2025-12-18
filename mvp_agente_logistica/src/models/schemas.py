"""
Schemas Pydantic para cada tipo de documento
"""
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from .fields import (
    Carga,
    Cliente,
    Conductor,
    Producto,
    ProductoOrdenado,
    ProductoRecibido,
    Proveedor,
    Ubicacion
)


class DocumentType(str, Enum):
    """Tipos de documentos soportados"""
    ALBARAN = "ALBARAN"
    ORDEN_ENVIO = "ORDEN_ENVIO"
    NOTA_RECEPCION = "NOTA_RECEPCION"
    PARTE_TRANSPORTE = "PARTE_TRANSPORTE"


class AlbaranSchema(BaseModel):
    """Schema para Albaran de Entrega"""
    numero_albaran: str = Field(..., pattern=r"^ALB-\d{8}$", description="Numero del albaran")
    fecha_emision: date = Field(..., description="Fecha de emision")
    proveedor: Proveedor = Field(..., description="Datos del proveedor")
    cliente: Cliente = Field(..., description="Datos del cliente")
    productos: List[Producto] = Field(..., min_length=1, description="Lista de productos")
    total: float = Field(..., ge=0, description="Total del albaran")
    firma_transportista: bool = Field(default=False, description="Indica si hay firma")
    sello_empresa: bool = Field(default=False, description="Indica si hay sello")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")

    @field_validator('fecha_emision')
    @classmethod
    def fecha_no_futuro(cls, v: date) -> date:
        """Valida que la fecha no sea futura"""
        if v > date.today():
            raise ValueError("La fecha de emision no puede ser futura")
        return v

    @field_validator('total')
    @classmethod
    def validar_total(cls, v: float, info) -> float:
        """Valida que el total coincida con la suma de subtotales"""
        values = info.data
        if 'productos' in values:
            suma_subtotales = sum(
                p.subtotal for p in values['productos'] if p.subtotal is not None
            )
            if suma_subtotales > 0 and abs(v - suma_subtotales) > 0.01:
                raise ValueError(f"El total ({v}) no coincide con la suma de subtotales ({suma_subtotales})")
        return v


class OrdenEnvioSchema(BaseModel):
    """Schema para Orden de Envio"""
    numero_orden: str = Field(..., pattern=r"^ORD-\d{8}$", description="Numero de orden")
    fecha_orden: date = Field(..., description="Fecha de la orden")
    fecha_envio_programada: date = Field(..., description="Fecha de envio programada")
    origen: Ubicacion = Field(..., description="Ubicacion de origen")
    destino: Ubicacion = Field(..., description="Ubicacion de destino")
    productos: List[ProductoOrdenado] = Field(..., min_length=1, description="Lista de productos")
    transportista: Optional[str] = Field(None, description="Nombre del transportista")
    instrucciones_especiales: Optional[str] = Field(None, description="Instrucciones especiales")

    @field_validator('fecha_envio_programada')
    @classmethod
    def fecha_envio_posterior(cls, v: date, info) -> date:
        """Valida que la fecha de envio sea posterior a la fecha de orden"""
        values = info.data
        if 'fecha_orden' in values and v < values['fecha_orden']:
            raise ValueError("La fecha de envio debe ser posterior a la fecha de orden")
        return v


class NotaRecepcionSchema(BaseModel):
    """Schema para Nota de Recepcion"""
    numero_recepcion: str = Field(..., pattern=r"^REC-\d{8}$", description="Numero de recepcion")
    fecha_recepcion: date = Field(..., description="Fecha de recepcion")
    referencia_pedido: str = Field(..., description="Numero de pedido original")
    referencia_albaran: str = Field(..., description="Numero de albaran asociado")
    proveedor: str = Field(..., description="Nombre del proveedor")
    productos_recibidos: List[ProductoRecibido] = Field(..., min_length=1, description="Productos recibidos")
    discrepancias: bool = Field(default=False, description="Indica si hay discrepancias")
    firma_receptor: bool = Field(default=False, description="Indica si hay firma del receptor")
    observaciones_calidad: Optional[str] = Field(None, description="Observaciones de calidad")

    @field_validator('fecha_recepcion')
    @classmethod
    def fecha_no_futuro(cls, v: date) -> date:
        """Valida que la fecha no sea futura"""
        if v > date.today():
            raise ValueError("La fecha de recepcion no puede ser futura")
        return v

    @field_validator('discrepancias')
    @classmethod
    def verificar_discrepancias(cls, v: bool, info) -> bool:
        """Verifica si hay discrepancias en productos"""
        values = info.data
        if 'productos_recibidos' in values:
            tiene_discrepancias = any(
                p.cantidad_esperada != p.cantidad_recibida or p.estado != "correcto"
                for p in values['productos_recibidos']
            )
            if tiene_discrepancias and not v:
                # Auto-marcar discrepancias si se detectan
                return True
        return v


class ParteTransporteSchema(BaseModel):
    """Schema para Parte de Transporte"""
    numero_parte: str = Field(..., pattern=r"^PT-\d{8}$", description="Numero del parte")
    fecha_salida: datetime = Field(..., description="Fecha y hora de salida")
    fecha_llegada_estimada: datetime = Field(..., description="Fecha y hora estimada de llegada")
    matricula_vehiculo: str = Field(..., pattern=r"^\d{4}-[A-Z]{3}$", description="Matricula del vehiculo")
    conductor: Conductor = Field(..., description="Datos del conductor")
    origen: Ubicacion = Field(..., description="Ubicacion de origen")
    destino: Ubicacion = Field(..., description="Ubicacion de destino")
    carga: List[Carga] = Field(..., min_length=1, description="Lista de cargas")
    kilometraje_inicial: int = Field(..., ge=0, description="Kilometraje inicial")
    kilometraje_final: Optional[int] = Field(None, ge=0, description="Kilometraje final")
    firma_origen: bool = Field(default=False, description="Indica si hay firma en origen")
    firma_destino: Optional[bool] = Field(None, description="Indica si hay firma en destino")
    incidencias: Optional[str] = Field(None, description="Incidencias durante el transporte")

    @field_validator('fecha_llegada_estimada')
    @classmethod
    def fecha_llegada_posterior(cls, v: datetime, info) -> datetime:
        """Valida que la fecha de llegada sea posterior a la de salida"""
        values = info.data
        if 'fecha_salida' in values and v <= values['fecha_salida']:
            raise ValueError("La fecha de llegada debe ser posterior a la de salida")
        return v

    @field_validator('kilometraje_final')
    @classmethod
    def kilometraje_final_mayor(cls, v: Optional[int], info) -> Optional[int]:
        """Valida que el kilometraje final sea mayor que el inicial"""
        if v is None:
            return v
        values = info.data
        if 'kilometraje_inicial' in values and v < values['kilometraje_inicial']:
            raise ValueError("El kilometraje final debe ser mayor o igual que el inicial")
        return v


class Discrepancy(BaseModel):
    """Representa una discrepancia detectada"""
    type: str = Field(..., description="Tipo de discrepancia (quantity_mismatch, missing_product, etc)")
    severity: str = Field(..., description="Severidad (critical, warning, info)")
    field: str = Field(..., description="Campo afectado")
    expected: Optional[str] = Field(None, description="Valor esperado")
    actual: Optional[str] = Field(None, description="Valor actual")
    description: str = Field(..., description="Descripcion de la discrepancia")
    suggested_action: str = Field(..., description="Accion sugerida")
    business_rule_violated: Optional[str] = Field(None, description="Regla de negocio violada")

    @field_validator('severity')
    @classmethod
    def validar_severity(cls, v: str) -> str:
        """Valida que la severidad sea valida"""
        severidades_validas = ["critical", "warning", "info"]
        if v.lower() not in severidades_validas:
            raise ValueError(f"Severidad debe ser una de: {', '.join(severidades_validas)}")
        return v.lower()


class ValidationReport(BaseModel):
    """Reporte de validacion completo"""
    report_id: str = Field(..., description="ID del reporte")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp del reporte")
    document_group_id: str = Field(..., description="ID del grupo de documentos")
    total_documents: int = Field(..., ge=1, description="Total de documentos validados")
    documents: List[dict] = Field(..., description="Lista de documentos validados")
    status: str = Field(..., description="Estado general (valid, warnings, invalid)")
    discrepancies: List[Discrepancy] = Field(default_factory=list, description="Lista de discrepancias")
    summary: dict = Field(..., description="Resumen de la validacion")
    recommendations: List[str] = Field(default_factory=list, description="Recomendaciones")

    @field_validator('status')
    @classmethod
    def validar_status(cls, v: str) -> str:
        """Valida que el status sea valido"""
        statuses_validos = ["valid", "warnings", "invalid", "requires_review"]
        if v.lower() not in statuses_validos:
            raise ValueError(f"Status debe ser uno de: {', '.join(statuses_validos)}")
        return v.lower()


# Modelos adicionales para el procesamiento completo

class ValidationResult(BaseModel):
    """Resultado de validación individual de un documento"""
    status: str = Field(..., description="Estado de validación (valid, invalid, warning)")
    errors: List[str] = Field(default_factory=list, description="Lista de errores")
    warnings: List[str] = Field(default_factory=list, description="Lista de advertencias")


class ProcessedDocument(BaseModel):
    """Documento procesado completo con toda la información"""
    metadata: Dict[str, Any] = Field(..., description="Metadatos del procesamiento")
    classification: Dict[str, Any] = Field(..., description="Información de clasificación")
    ocr_info: Dict[str, Any] = Field(..., description="Información del OCR")
    extracted_fields: Dict[str, Any] = Field(..., description="Campos extraídos")
    validation: ValidationResult = Field(..., description="Resultado de validación")
    raw_ocr_text: str = Field(..., description="Texto OCR completo sin procesar")


# Aliases para facilitar uso - versiones simplificadas de los schemas principales
AlbaranFields = AlbaranSchema
OrdenEnvioFields = OrdenEnvioSchema
NotaRecepcionFields = NotaRecepcionSchema
ParteTransporteFields = ParteTransporteSchema
