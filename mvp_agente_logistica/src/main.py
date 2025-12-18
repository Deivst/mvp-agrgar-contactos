"""
Punto de entrada CLI del agente logistico
"""
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .core.config import load_config
from .core.logger import setup_logger
from .core.pipeline import DocumentProcessingPipeline

app = typer.Typer(
    name="agente-logistica",
    help="Agente de IA para clasificacion y validacion de documentos logisticos",
    add_completion=False
)

console = Console()


@app.command()
def process(
    file: str = typer.Option(..., "--file", "-f", help="Ruta al documento a procesar"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Ruta del archivo de salida JSON"),
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Archivo de configuracion custom"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Modo verbose (logs detallados)"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Modo silencioso (solo errores)")
):
    """
    Procesa un documento individual
    """
    try:
        # Cargar configuracion
        config = load_config(config_file)

        # Configurar logger
        log_level = "DEBUG" if verbose else ("ERROR" if quiet else "INFO")
        logger = setup_logger(
            log_level=log_level,
            log_file=config.general.log_file if not quiet else None
        )

        # Verificar que el archivo existe
        if not Path(file).exists():
            console.print(f"[red]Error: Archivo no encontrado: {file}[/red]")
            raise typer.Exit(1)

        # Crear pipeline
        pipeline = DocumentProcessingPipeline(config)

        # Procesar documento
        console.print(f"\n[bold cyan]Procesando documento:[/bold cyan] {file}")
        result = pipeline.process_document(file, output)

        # Mostrar resumen
        console.print("\n[bold green]Documento procesado exitosamente![/bold green]\n")

        table = Table(title="Resultado del Procesamiento")
        table.add_column("Campo", style="cyan")
        table.add_column("Valor", style="green")

        table.add_row("Tipo de Documento", result.document_type.value)
        table.add_row("Confianza Clasificacion", f"{result.classification_confidence:.2%}")
        table.add_row("Confianza OCR", f"{result.ocr_average_confidence:.2%}")
        table.add_row("Motor OCR", result.ocr_engine_used)
        table.add_row("Bloques de Texto", str(result.total_text_blocks))
        table.add_row("Tiempo de Procesamiento", f"{result.processing_time_seconds:.2f}s")

        if output:
            table.add_row("Archivo de Salida", output)

        console.print(table)

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def batch(
    input_dir: str = typer.Option(..., "--input-dir", "-i", help="Directorio con documentos"),
    output_dir: str = typer.Option(..., "--output-dir", "-o", help="Directorio de salida"),
    pattern: str = typer.Option("*.*", "--pattern", "-p", help="Patron de archivos (ej: *.pdf)"),
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Archivo de configuracion"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Modo verbose")
):
    """
    Procesa un lote de documentos
    """
    try:
        # Cargar configuracion
        config = load_config(config_file)

        # Configurar logger
        log_level = "DEBUG" if verbose else "INFO"
        logger = setup_logger(log_level=log_level, log_file=config.general.log_file)

        # Obtener archivos
        input_path = Path(input_dir)
        if not input_path.exists():
            console.print(f"[red]Error: Directorio no encontrado: {input_dir}[/red]")
            raise typer.Exit(1)

        files = list(input_path.glob(pattern))
        if not files:
            console.print(f"[yellow]No se encontraron archivos con patron '{pattern}' en {input_dir}[/yellow]")
            raise typer.Exit(0)

        console.print(f"\n[bold cyan]Procesando {len(files)} documentos...[/bold cyan]\n")

        # Crear pipeline
        pipeline = DocumentProcessingPipeline(config)

        # Procesar lote
        file_paths = [str(f) for f in files]
        results = pipeline.process_batch(file_paths, output_dir)

        # Mostrar resumen
        console.print(f"\n[bold green]Lote completado:[/bold green] {len(results)}/{len(files)} documentos procesados\n")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Mostrar configuracion actual"),
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Archivo de configuracion")
):
    """
    Gestiona la configuracion del sistema
    """
    try:
        config_obj = load_config(config_file)

        if show:
            import json
            console.print("\n[bold cyan]Configuracion actual:[/bold cyan]\n")
            console.print_json(json.dumps(config_obj.to_dict(), indent=2))

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def version():
    """
    Muestra la version del agente
    """
    from . import __version__
    console.print(f"Agente Logistica MVP v{__version__}")


if __name__ == "__main__":
    app()
