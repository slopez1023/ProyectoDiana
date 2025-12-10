"""
Script principal del Sistema de Tablero de Control de Indicadores MIPG.

Este script ejecuta el proceso completo de análisis:
1. Carga de datos desde Excel
2. Procesamiento y limpieza
3. Análisis de indicadores
4. Generación de gráficos
5. Creación de reportes

Uso:
    python main.py
"""

import sys
import os
import logging
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_processing.excel_loader import load_and_process_excel
from analysis.indicator_analyzer import analizar_todos_indicadores
from visualization.chart_generator import generar_todos_graficos
from reporting.report_generator import generar_informe_pdf
from utils.config import *
from utils.helpers import create_output_filename

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler('sistema_indicadores.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Función principal del sistema.
    Ejecuta el flujo completo de análisis de indicadores.
    """
    logger.info("=" * 80)
    logger.info("SISTEMA DE TABLERO DE CONTROL DE INDICADORES MIPG")
    logger.info("Secretaría de Planeación")
    logger.info("=" * 80)
    
    try:
        # 1. CARGA DE DATOS
        logger.info("\n[PASO 1/5] Cargando y procesando datos del Excel...")
        
        archivo_excel = DEFAULT_EXCEL_FILE
        
        if not os.path.exists(archivo_excel):
            logger.error(f"No se encontró el archivo: {archivo_excel}")
            logger.error("Por favor, coloque el archivo Excel en el directorio raíz del proyecto.")
            return False
        
        df_procesado, indicadores_list, resumen = load_and_process_excel(archivo_excel)
        
        logger.info(f"✓ Datos cargados exitosamente")
        logger.info(f"  - Total indicadores procesados: {len(indicadores_list)}")
        logger.info(f"  - Dimensiones DataFrame: {df_procesado.shape}")
        
        # 2. ANÁLISIS DE INDICADORES
        logger.info("\n[PASO 2/5] Analizando indicadores...")
        
        analisis_list = analizar_todos_indicadores(indicadores_list)
        
        # Estadísticas del análisis
        verdes = sum(1 for a in analisis_list if a.get('semaforo') == 'Verde')
        amarillos = sum(1 for a in analisis_list if a.get('semaforo') == 'Amarillo')
        rojos = sum(1 for a in analisis_list if a.get('semaforo') == 'Rojo')
        
        logger.info(f"✓ Análisis completado")
        logger.info(f"  - Indicadores en estado satisfactorio (Verde): {verdes}")
        logger.info(f"  - Indicadores en estado alerta (Amarillo): {amarillos}")
        logger.info(f"  - Indicadores en estado crítico (Rojo): {rojos}")
        
        # 3. GENERACIÓN DE GRÁFICOS
        logger.info("\n[PASO 3/5] Generando gráficos...")
        
        # Crear directorios si no existen
        os.makedirs(CHARTS_DIR, exist_ok=True)
        
        rutas_graficos = generar_todos_graficos(
            indicadores_list,
            analisis_list,
            str(CHARTS_DIR)
        )
        
        logger.info(f"✓ Gráficos generados: {len(rutas_graficos)}")
        for nombre, ruta in rutas_graficos.items():
            logger.info(f"  - {nombre}: {ruta}")
        
        # 4. GENERACIÓN DE REPORTE PDF
        logger.info("\n[PASO 4/5] Generando informe PDF...")
        
        # Crear directorio si no existe
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
        nombre_reporte = create_output_filename('Informe_Indicadores_MIPG', 'pdf')
        ruta_reporte = os.path.join(REPORTS_DIR, nombre_reporte)
        
        exito_pdf = generar_informe_pdf(
            indicadores_list,
            analisis_list,
            ruta_reporte,
            entidad=ENTITY_NAME
        )
        
        if exito_pdf:
            logger.info(f"✓ Reporte PDF generado: {ruta_reporte}")
        else:
            logger.warning("⚠ No se pudo generar el reporte PDF")
        
        # 5. RESUMEN FINAL
        logger.info("\n[PASO 5/5] Proceso completado exitosamente")
        logger.info("\n" + "=" * 80)
        logger.info("RESUMEN DE EJECUCIÓN")
        logger.info("=" * 80)
        logger.info(f"✓ Indicadores analizados: {len(indicadores_list)}")
        logger.info(f"✓ Gráficos generados: {len(rutas_graficos)}")
        logger.info(f"✓ Reporte PDF: {ruta_reporte if exito_pdf else 'No generado'}")
        logger.info("=" * 80)
        
        logger.info("\nPara visualizar el dashboard interactivo, ejecute:")
        logger.info("  streamlit run src/dashboard.py")
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Error durante la ejecución: {str(e)}")
        logger.exception("Detalles del error:")
        return False


if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)
