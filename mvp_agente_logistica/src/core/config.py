"""
Configuracion global del sistema
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralConfig(BaseSettings):
    """Configuracion general"""
    version: str = "1.0.0"
    log_level: str = "INFO"
    log_file: str = "logs/agente.log"
    data_dir: str = "data/"
    temp_dir: str = "temp/"


class InputConfig(BaseSettings):
    """Configuracion de entrada"""
    supported_formats: List[str] = ["jpg", "jpeg", "png", "tiff", "pdf"]
    max_file_size_mb: int = 20
    min_resolution_dpi: int = 150


class PreprocessingConfig(BaseSettings):
    """Configuracion de preprocesamiento"""
    denoise: bool = True
    denoise_strength: int = 3
    deskew: bool = True
    deskew_threshold: float = 0.5
    enhance_contrast: bool = True
    contrast_method: str = "clahe"
    binarize: bool = False


class PaddleOCRConfig(BaseSettings):
    """Configuracion de PaddleOCR"""
    use_angle_cls: bool = True
    det_db_thresh: float = 0.3
    det_db_box_thresh: float = 0.6
    det_db_unclip_ratio: float = 1.5


class TesseractConfig(BaseSettings):
    """Configuracion de Tesseract"""
    psm: int = 3
    oem: int = 3


class OCRConfig(BaseSettings):
    """Configuracion de OCR"""
    primary_engine: str = "paddleocr"
    fallback_engine: str = "tesseract"
    language: str = "es"
    use_gpu: bool = False
    confidence_threshold: float = 0.7
    paddleocr: PaddleOCRConfig = Field(default_factory=PaddleOCRConfig)
    tesseract: TesseractConfig = Field(default_factory=TesseractConfig)


class LLMClassificationConfig(BaseSettings):
    """Configuracion de clasificacion LLM"""
    max_tokens: int = 100
    confidence_threshold: float = 0.8


class LLMExtractionConfig(BaseSettings):
    """Configuracion de extraccion LLM"""
    max_tokens: int = 2000
    use_json_mode: bool = True


class LLMConfig(BaseSettings):
    """Configuracion de LLM"""
    provider: str = "ollama"
    model: str = "llama3:8b"
    base_url: str = "http://localhost:11434"
    timeout_seconds: int = 30
    max_retries: int = 3
    temperature: float = 0.1
    classification: LLMClassificationConfig = Field(default_factory=LLMClassificationConfig)
    extraction: LLMExtractionConfig = Field(default_factory=LLMExtractionConfig)


class CrossValidationConfig(BaseSettings):
    """Configuracion de validacion cruzada"""
    enable: bool = True
    link_by: List[str] = ["numero_pedido", "cliente"]
    max_date_diff_days: int = 30


class ValidationConfig(BaseSettings):
    """Configuracion de validacion"""
    quantity_tolerance_percent: int = 10
    date_sequence_strict: bool = True
    require_all_mandatory_fields: bool = True
    cross_validation: CrossValidationConfig = Field(default_factory=CrossValidationConfig)


class OutputConfig(BaseSettings):
    """Configuracion de salida"""
    format: str = "json"
    pretty_print: bool = True
    include_raw_ocr: bool = True
    include_metadata: bool = True
    output_dir: str = "data/processed/"


class PerformanceConfig(BaseSettings):
    """Configuracion de performance"""
    max_workers: int = 4
    processing_timeout_seconds: int = 60
    enable_caching: bool = True
    cache_dir: str = "cache/"


class EvaluationConfig(BaseSettings):
    """Configuracion de evaluacion"""
    test_data_dir: str = "data/test/"
    ground_truth_file: str = "data/test/ground_truth.json"
    results_dir: str = "data/results/"
    generate_plots: bool = True


class Config(BaseSettings):
    """Configuracion principal del sistema"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    general: GeneralConfig = Field(default_factory=GeneralConfig)
    input: InputConfig = Field(default_factory=InputConfig)
    preprocessing: PreprocessingConfig = Field(default_factory=PreprocessingConfig)
    ocr: OCRConfig = Field(default_factory=OCRConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)

    @classmethod
    def load_from_yaml(cls, config_path: str = "config.yaml") -> "Config":
        """
        Carga configuracion desde archivo YAML

        Args:
            config_path: Ruta al archivo de configuracion

        Returns:
            Instancia de Config
        """
        if not Path(config_path).exists():
            raise FileNotFoundError(f"Archivo de configuracion no encontrado: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        return cls(**config_data)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte configuracion a diccionario"""
        return self.model_dump()

    def save_to_yaml(self, output_path: str = "config_generated.yaml") -> None:
        """
        Guarda configuracion actual en archivo YAML

        Args:
            output_path: Ruta de salida
        """
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, allow_unicode=True)


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Carga configuracion desde archivo o variables de entorno

    Args:
        config_path: Ruta al archivo de configuracion (opcional)

    Returns:
        Instancia de Config
    """
    if config_path is None:
        config_path = os.getenv("CONFIG_FILE", "config.yaml")

    if Path(config_path).exists():
        return Config.load_from_yaml(config_path)
    else:
        # Usar configuracion por defecto
        return Config()
