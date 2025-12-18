"""
Templates de prompts para LLM
"""

CLASSIFICATION_SYSTEM_PROMPT = """Eres un asistente experto en clasificacion de documentos logisticos.
Tu tarea es analizar texto extraido por OCR y determinar el tipo de documento."""

CLASSIFICATION_PROMPT = """Analiza el siguiente texto extraido de un documento logistico y clasifica su tipo.

TIPOS VALIDOS:
1. ALBARAN - Documento de entrega de mercancias (albaran, delivery note)
2. ORDEN_ENVIO - Orden de despacho o envio (shipping order, picking list)
3. NOTA_RECEPCION - Comprobante de recepcion de mercancias (receiving note, goods received)
4. PARTE_TRANSPORTE - Documento de transporte de mercancias (transport sheet, CMR)

TEXTO DEL DOCUMENTO:
{ocr_text}

Responde SOLO con un objeto JSON en este formato:
{{
    "document_type": "TIPO",
    "confidence": 0.95,
    "reasoning": "Breve explicacion de por que clasificaste asi"
}}

NOTA: document_type debe ser exactamente uno de: ALBARAN, ORDEN_ENVIO, NOTA_RECEPCION, PARTE_TRANSPORTE"""

EXTRACTION_SYSTEM_PROMPT = """Eres un asistente experto en extraccion de datos de documentos logisticos.
Extrae campos estructurados con precision. Si un campo no esta presente, usa null."""

EXTRACTION_PROMPT_ALBARAN = """Extrae los siguientes campos del albaran de entrega.

TEXTO DEL DOCUMENTO:
{ocr_text}

Extrae estos campos en formato JSON:
{{
    "numero_albaran": "Numero del albaran (patron: ALB-YYYYMMDD)",
    "fecha_emision": "Fecha en formato YYYY-MM-DD",
    "proveedor": {{
        "razon_social": "Nombre del proveedor",
        "cif": "CIF del proveedor",
        "direccion": "Direccion del proveedor"
    }},
    "cliente": {{
        "razon_social": "Nombre del cliente",
        "cif": "CIF del cliente",
        "direccion_entrega": "Direccion de entrega"
    }},
    "productos": [
        {{
            "codigo_producto": "Codigo del producto",
            "descripcion": "Descripcion del producto",
            "cantidad": 0,
            "precio_unitario": 0.0,
            "subtotal": 0.0
        }}
    ],
    "total": 0.0,
    "firma_transportista": true/false,
    "sello_empresa": true/false,
    "observaciones": "Observaciones si las hay"
}}

IMPORTANTE:
- Usa null para campos que no encuentres
- cantidad debe ser numero entero
- precios deben ser numeros decimales
- fechas en formato YYYY-MM-DD
- firma_transportista y sello_empresa son booleanos"""

EXTRACTION_PROMPT_ORDEN_ENVIO = """Extrae los siguientes campos de la orden de envio.

TEXTO DEL DOCUMENTO:
{ocr_text}

Extrae estos campos en formato JSON:
{{
    "numero_orden": "Numero de orden (patron: ORD-YYYYMMDD)",
    "fecha_orden": "Fecha en formato YYYY-MM-DD",
    "fecha_envio_programada": "Fecha programada en formato YYYY-MM-DD",
    "origen": {{
        "ubicacion": "Nombre del almacen/ubicacion",
        "direccion": "Direccion completa",
        "codigo_postal": "Codigo postal"
    }},
    "destino": {{
        "ubicacion": "Cliente o ubicacion destino",
        "direccion": "Direccion de entrega",
        "codigo_postal": "Codigo postal"
    }},
    "productos": [
        {{
            "codigo": "Codigo del producto",
            "descripcion": "Descripcion",
            "cantidad_ordenada": 0,
            "ubicacion_almacen": "Ubicacion en almacen"
        }}
    ],
    "transportista": "Nombre del transportista",
    "instrucciones_especiales": "Instrucciones especiales"
}}"""

EXTRACTION_PROMPT_NOTA_RECEPCION = """Extrae los siguientes campos de la nota de recepcion.

TEXTO DEL DOCUMENTO:
{ocr_text}

Extrae estos campos en formato JSON:
{{
    "numero_recepcion": "Numero de recepcion (patron: REC-YYYYMMDD)",
    "fecha_recepcion": "Fecha en formato YYYY-MM-DD",
    "referencia_pedido": "Numero de pedido original",
    "referencia_albaran": "Numero de albaran asociado",
    "proveedor": "Nombre del proveedor",
    "productos_recibidos": [
        {{
            "codigo": "Codigo del producto",
            "descripcion": "Descripcion",
            "cantidad_esperada": 0,
            "cantidad_recibida": 0,
            "estado": "correcto/danado/faltante",
            "observaciones": "Observaciones del producto"
        }}
    ],
    "discrepancias": true/false,
    "firma_receptor": true/false,
    "observaciones_calidad": "Observaciones generales de calidad"
}}

NOTA: estado debe ser exactamente: correcto, danado, o faltante"""

EXTRACTION_PROMPT_PARTE_TRANSPORTE = """Extrae los siguientes campos del parte de transporte.

TEXTO DEL DOCUMENTO:
{ocr_text}

Extrae estos campos en formato JSON:
{{
    "numero_parte": "Numero del parte (patron: PT-YYYYMMDD)",
    "fecha_salida": "Fecha y hora en formato YYYY-MM-DD HH:MM",
    "fecha_llegada_estimada": "Fecha y hora estimada en formato YYYY-MM-DD HH:MM",
    "matricula_vehiculo": "Matricula (patron: 1234-ABC)",
    "conductor": {{
        "nombre": "Nombre del conductor",
        "dni": "DNI",
        "licencia": "Numero de licencia"
    }},
    "origen": {{
        "ubicacion": "Ubicacion de origen",
        "codigo_postal": "Codigo postal"
    }},
    "destino": {{
        "ubicacion": "Ubicacion de destino",
        "codigo_postal": "Codigo postal"
    }},
    "carga": [
        {{
            "numero_albaran": "Numero de albaran",
            "bultos": 0,
            "peso_kg": 0.0
        }}
    ],
    "kilometraje_inicial": 0,
    "kilometraje_final": null,
    "firma_origen": true/false,
    "firma_destino": null,
    "incidencias": "Incidencias durante el transporte"
}}"""

# Mapeo de tipo de documento a prompt de extraccion
EXTRACTION_PROMPTS = {
    "ALBARAN": EXTRACTION_PROMPT_ALBARAN,
    "ORDEN_ENVIO": EXTRACTION_PROMPT_ORDEN_ENVIO,
    "NOTA_RECEPCION": EXTRACTION_PROMPT_NOTA_RECEPCION,
    "PARTE_TRANSPORTE": EXTRACTION_PROMPT_PARTE_TRANSPORTE
}

AMBIGUITY_RESOLUTION_PROMPT = """Resuelve la ambiguedad en el siguiente campo extraido de un documento.

CAMPO: {field_name}
VALORES CANDIDATOS: {candidates}
CONTEXTO: {context}

Selecciona el valor mas probable y explicalo brevemente.

Responde en formato JSON:
{{
    "selected_value": "valor seleccionado",
    "confidence": 0.9,
    "reasoning": "Breve explicacion"
}}"""
