"""
Modelos de campos extraidos de documentos
"""
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class Proveedor(BaseModel):
    """Datos del proveedor"""
    razon_social: str = Field(..., description="Razon social del proveedor")
    cif: Optional[str] = Field(None, description="CIF del proveedor")
    direccion: Optional[str] = Field(None, description="Direccion del proveedor")


class Cliente(BaseModel):
    """Datos del cliente"""
    razon_social: str = Field(..., description="Razon social del cliente")
    cif: Optional[str] = Field(None, description="CIF del cliente")
    direccion_entrega: Optional[str] = Field(None, description="Direccion de entrega")


class Producto(BaseModel):
    """Producto en documento"""
    codigo_producto: str = Field(..., description="Codigo del producto")
    descripcion: str = Field(..., description="Descripcion del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad")
    precio_unitario: Optional[float] = Field(None, ge=0, description="Precio unitario")
    subtotal: Optional[float] = Field(None, ge=0, description="Subtotal")

    @field_validator('cantidad')
    @classmethod
    def cantidad_positiva(cls, v: int) -> int:
        """Valida que la cantidad sea positiva"""
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        return v


class Ubicacion(BaseModel):
    """Ubicacion geografica"""
    ubicacion: str = Field(..., description="Nombre de ubicacion")
    direccion: Optional[str] = Field(None, description="Direccion completa")
    codigo_postal: Optional[str] = Field(None, description="Codigo postal")


class Conductor(BaseModel):
    """Datos del conductor"""
    nombre: str = Field(..., description="Nombre del conductor")
    dni: Optional[str] = Field(None, description="DNI del conductor")
    licencia: Optional[str] = Field(None, description="Numero de licencia")


class Carga(BaseModel):
    """Informacion de carga en transporte"""
    numero_albaran: str = Field(..., description="Numero de albaran asociado")
    bultos: int = Field(..., gt=0, description="Numero de bultos")
    peso_kg: float = Field(..., gt=0, description="Peso en kilogramos")


class ProductoRecibido(BaseModel):
    """Producto recibido en nota de recepcion"""
    codigo: str = Field(..., description="Codigo del producto")
    descripcion: str = Field(..., description="Descripcion del producto")
    cantidad_esperada: int = Field(..., gt=0, description="Cantidad esperada")
    cantidad_recibida: int = Field(..., ge=0, description="Cantidad recibida")
    estado: str = Field(..., description="Estado (correcto, danado, faltante)")
    observaciones: Optional[str] = Field(None, description="Observaciones")

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, v: str) -> str:
        """Valida que el estado sea uno de los permitidos"""
        estados_validos = ["correcto", "danado", "faltante"]
        if v.lower() not in estados_validos:
            raise ValueError(f"Estado debe ser uno de: {', '.join(estados_validos)}")
        return v.lower()


class ProductoOrdenado(BaseModel):
    """Producto en orden de envio"""
    codigo: str = Field(..., description="Codigo del producto")
    descripcion: str = Field(..., description="Descripcion del producto")
    cantidad_ordenada: int = Field(..., gt=0, description="Cantidad ordenada")
    ubicacion_almacen: Optional[str] = Field(None, description="Ubicacion en almacen")


# Modelos adicionales y aliases

class ProductoAlbaran(Producto):
    """Producto en albarán - alias de Producto"""
    pass


class ProductoOrden(ProductoOrdenado):
    """Producto en orden - alias de ProductoOrdenado"""
    pass


class Origen(BaseModel):
    """Ubicacion de origen con campos especificos"""
    almacen: str = Field(..., description="Nombre del almacen")
    direccion: str = Field(..., description="Direccion completa")
    codigo_postal: str = Field(..., description="Codigo postal")


class Destino(BaseModel):
    """Ubicacion de destino con campos especificos"""
    cliente: str = Field(..., description="Nombre del cliente")
    direccion_entrega: str = Field(..., description="Direccion de entrega")
    codigo_postal: str = Field(..., description="Codigo postal")
