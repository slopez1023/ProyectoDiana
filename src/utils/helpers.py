"""
Utilidades auxiliares del sistema.

Funciones helper para operaciones comunes.
"""

import pandas as pd
import numpy as np
from typing import Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Formatea un valor numérico como porcentaje.
    
    Args:
        value (float): Valor a formatear
        decimals (int): Número de decimales
        
    Returns:
        str: Valor formateado como porcentaje
    """
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimals}f}%"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    División segura que evita división por cero.
    
    Args:
        numerator (float): Numerador
        denominator (float): Denominador
        default (float): Valor por defecto si denominador es cero
        
    Returns:
        float: Resultado de la división o valor por defecto
    """
    if pd.isna(numerator) or pd.isna(denominator):
        return default
    
    if denominator == 0:
        return default
    
    return numerator / denominator


def clean_text(text: Any) -> str:
    """
    Limpia texto eliminando espacios y caracteres especiales.
    
    Args:
        text: Texto a limpiar
        
    Returns:
        str: Texto limpio
    """
    if pd.isna(text):
        return ""
    
    text = str(text).strip()
    text = ' '.join(text.split())  # Eliminar espacios múltiples
    
    return text


def validate_dataframe(df: pd.DataFrame, required_columns: list) -> tuple:
    """
    Valida que un DataFrame contenga las columnas requeridas.
    
    Args:
        df (pd.DataFrame): DataFrame a validar
        required_columns (list): Lista de columnas requeridas
        
    Returns:
        tuple: (is_valid, missing_columns)
    """
    if df is None or df.empty:
        return False, required_columns
    
    missing = [col for col in required_columns if col not in df.columns]
    
    return len(missing) == 0, missing


def get_month_name_es(month_number: int) -> str:
    """
    Obtiene el nombre del mes en español.
    
    Args:
        month_number (int): Número del mes (1-12)
        
    Returns:
        str: Nombre del mes
    """
    meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    
    if 1 <= month_number <= 12:
        return meses[month_number - 1]
    
    return "Mes inválido"


def create_output_filename(prefix: str, extension: str = 'xlsx') -> str:
    """
    Crea un nombre de archivo con timestamp.
    
    Args:
        prefix (str): Prefijo del nombre
        extension (str): Extensión del archivo
        
    Returns:
        str: Nombre del archivo con timestamp
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.{extension}"


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calcula el cambio porcentual entre dos valores.
    
    Args:
        old_value (float): Valor antiguo
        new_value (float): Valor nuevo
        
    Returns:
        float: Cambio porcentual
    """
    if pd.isna(old_value) or pd.isna(new_value):
        return np.nan
    
    if old_value == 0:
        return np.nan
    
    return ((new_value - old_value) / old_value) * 100


def describe_trend(pendiente: float) -> str:
    """
    Describe una tendencia basándose en la pendiente.
    
    Args:
        pendiente (float): Valor de la pendiente
        
    Returns:
        str: Descripción de la tendencia
    """
    if pd.isna(pendiente):
        return "Datos insuficientes"
    
    if abs(pendiente) < 0.5:
        return "Estable"
    elif pendiente > 0:
        if pendiente > 2.0:
            return "Crecimiento fuerte"
        else:
            return "Crecimiento moderado"
    else:
        if pendiente < -2.0:
            return "Retroceso fuerte"
        else:
            return "Retroceso moderado"


def export_to_excel(data: pd.DataFrame, output_path: str, sheet_name: str = 'Datos') -> bool:
    """
    Exporta un DataFrame a Excel.
    
    Args:
        data (pd.DataFrame): Datos a exportar
        output_path (str): Ruta de salida
        sheet_name (str): Nombre de la hoja
        
    Returns:
        bool: True si se exportó exitosamente
    """
    try:
        data.to_excel(output_path, sheet_name=sheet_name, index=False)
        logger.info(f"Datos exportados a: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error al exportar a Excel: {str(e)}")
        return False
