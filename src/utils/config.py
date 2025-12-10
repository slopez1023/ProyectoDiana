"""
Módulo de configuración del sistema.

Define constantes, rutas y parámetros globales del sistema.
"""

import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
INPUT_DIR = DATA_DIR / 'input'
PROCESSED_DIR = DATA_DIR / 'processed'
OUTPUT_DIR = BASE_DIR / 'output'
REPORTS_DIR = OUTPUT_DIR / 'reports'
CHARTS_DIR = OUTPUT_DIR / 'charts'

# Archivo de entrada por defecto
DEFAULT_EXCEL_FILE = "RE-SM-01 Tablero de Control de Indicadores 2025.xls"

# Configuración de análisis
MESES_ORDEN = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

# Umbrales de análisis
Z_SCORE_THRESHOLD = 2.5  # Para detección de anomalías
VOLATILITY_THRESHOLD = 15.0  # Coeficiente de variación
STABILITY_THRESHOLD = 0.5  # Pendiente casi nula

# Colores institucionales
COLORS_SEMAFORO = {
    'Verde': '#28a745',
    'Amarillo': '#ffc107',
    'Rojo': '#dc3545',
    'Gris': '#6c757d'
}

# Configuración de reportes
REPORT_TITLE = "Informe de Indicadores MIPG"
ENTITY_NAME = "Secretaría de Planeación"
REPORT_AUTHOR = "Sistema Automático de Análisis"

# Configuración de logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
