"""
Módulo de importación y procesamiento de datos Excel.

Este módulo contiene la clase ExcelDataLoader que se encarga de:
- Cargar el archivo Excel del tablero de indicadores
- Validar la estructura de datos
- Limpiar y normalizar la información
- Extraer indicadores y sus valores por período

Aplica principios SOLID:
- Single Responsibility: Una clase, una responsabilidad (carga de datos)
- Open/Closed: Extensible para nuevos formatos sin modificar código existente
- Dependency Inversion: Depende de abstracciones (interfaces de datos)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import warnings
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


class ExcelDataLoader:
    """
    Clase responsable de cargar y procesar datos del archivo Excel de indicadores MIPG.
    
    Attributes:
        file_path (str): Ruta al archivo Excel
        df_raw (pd.DataFrame): DataFrame con datos crudos
        df_processed (pd.DataFrame): DataFrame con datos procesados
        metadata (Dict): Metadatos del archivo y procesamiento
    """
    
    def __init__(self, file_path: str):
        """
        Inicializa el cargador de datos.
        
        Args:
            file_path (str): Ruta completa al archivo Excel
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el archivo no tiene el formato esperado
        """
        self.file_path = file_path
        self.df_raw = None
        self.df_processed = None
        self.metadata = {
            'file_path': file_path,
            'load_timestamp': datetime.now(),
            'total_indicators': 0,
            'valid_indicators': 0,
            'invalid_indicators': 0
        }
        
        logger.info(f"Inicializando ExcelDataLoader para archivo: {file_path}")
    
    def load_data(self, sheet_name: str = 0) -> pd.DataFrame:
        """
        Carga los datos del archivo Excel.
        
        Args:
            sheet_name (str|int): Nombre o índice de la hoja a cargar
            
        Returns:
            pd.DataFrame: DataFrame con los datos cargados
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            Exception: Si hay error al leer el archivo
        """
        try:
            logger.info(f"Cargando datos desde: {self.file_path}")
            
            # Leer primero sin encabezados para detectar la estructura
            df_temp = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                header=None,
                engine='xlrd'
            )
            
            # Buscar la fila que contiene "Nombre del Indicador"
            header_row = None
            for i in range(min(10, len(df_temp))):
                row_values = df_temp.iloc[i].astype(str).tolist()
                if any('Nombre del Indicador' in str(val) for val in row_values):
                    header_row = i
                    logger.info(f"Encabezados encontrados en fila {i}")
                    break
            
            if header_row is None:
                header_row = 0
                logger.warning("No se encontró fila de encabezados, usando fila 0")
            
            # Volver a leer con el encabezado correcto
            self.df_raw = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                header=header_row,
                engine='xlrd'
            )
            
            # Si hay una segunda fila de encabezados (sub-encabezados de semaforización)
            # la procesaremos en el método de limpieza
            
            logger.info(f"Datos cargados: {self.df_raw.shape[0]} filas, {self.df_raw.shape[1]} columnas")
            self.metadata['total_indicators'] = len(self.df_raw)
            
            return self.df_raw
            
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {self.file_path}")
            raise FileNotFoundError(f"No se encontró el archivo: {self.file_path}")
        except Exception as e:
            logger.error(f"Error al cargar el archivo: {str(e)}")
            raise Exception(f"Error al cargar datos: {str(e)}")
    
    def validate_structure(self) -> Tuple[bool, List[str]]:
        """
        Valida que el DataFrame tenga la estructura esperada del tablero de indicadores.
        
        Returns:
            Tuple[bool, List[str]]: (es_válido, lista_de_errores)
        """
        errors = []
        
        if self.df_raw is None:
            errors.append("No se han cargado datos. Ejecute load_data() primero.")
            return False, errors
        
        # Validar que existan columnas mínimas requeridas
        required_columns = ['Nombre del Indicador', 'Meta']
        
        for col in required_columns:
            if col not in self.df_raw.columns:
                errors.append(f"Falta la columna requerida: {col}")
        
        # Validar que existan columnas de meses
        month_columns = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        found_months = [col for col in month_columns if col in self.df_raw.columns]
        
        if len(found_months) == 0:
            errors.append("No se encontraron columnas de períodos mensuales")
        
        # Validar columnas de semaforización
        semaforo_columns = ['Nivel Obtenido', 'Nivel Satisfactorio', 'Nivel Crítico']
        found_semaforo = [col for col in semaforo_columns if col in self.df_raw.columns]
        
        if len(found_semaforo) < 2:
            logger.warning("No se encontraron todas las columnas de semaforización")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info("Estructura de datos validada correctamente")
        else:
            logger.warning(f"Errores de validación encontrados: {len(errors)}")
            
        return is_valid, errors
    
    def clean_data(self) -> pd.DataFrame:
        """
        Limpia y normaliza los datos del DataFrame.
        
        - Elimina filas completamente vacías
        - Limpia espacios en blanco
        - Normaliza valores numéricos
        - Maneja valores especiales (#DIV/0!, NA, etc.)
        
        Returns:
            pd.DataFrame: DataFrame limpio
        """
        logger.info("Iniciando limpieza de datos...")
        
        if self.df_raw is None:
            raise ValueError("No hay datos cargados. Ejecute load_data() primero.")
        
        df = self.df_raw.copy()
        
        # Eliminar primera fila si contiene sub-encabezados de semaforización
        if df.iloc[0].astype(str).str.contains('Nivel', case=False, na=False).any():
            logger.info("Eliminando fila de sub-encabezados de semaforización")
            df = df.iloc[1:].reset_index(drop=True)
        
        # Eliminar filas completamente vacías
        df = df.dropna(how='all')
        
        # Limpiar nombres de columnas
        df.columns = [str(col).strip() if col else col for col in df.columns]
        
        # Renombrar columnas que tengan nombres genéricos después de "Semaforizacion"
        # Las columnas sin nombre después de "Semaforizacion" son los niveles
        col_names = list(df.columns)
        semaforo_idx = None
        for i, col in enumerate(col_names):
            if 'Semaforizacion' in str(col):
                semaforo_idx = i
                break
        
        if semaforo_idx is not None:
            # Las siguientes 3 columnas son los niveles
            if semaforo_idx + 1 < len(col_names):
                col_names[semaforo_idx] = 'Nivel Obtenido'
            if semaforo_idx + 2 < len(col_names):
                col_names[semaforo_idx + 1] = 'Nivel Satisfactorio'
            if semaforo_idx + 3 < len(col_names):
                col_names[semaforo_idx + 2] = 'Nivel Crítico'
            
            df.columns = col_names
            logger.info("Columnas de semaforización renombradas correctamente")
        
        # Limpiar espacios en la columna de nombres de indicadores
        if 'Nombre del Indicador' in df.columns:
            df['Nombre del Indicador'] = df['Nombre del Indicador'].str.strip()
            # Eliminar filas sin nombre de indicador
            df = df[df['Nombre del Indicador'].notna()]
            df = df[df['Nombre del Indicador'] != '']
        
        # Identificar columnas de períodos (meses)
        month_columns = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        existing_months = [col for col in month_columns if col in df.columns]
        
        # Limpiar valores en columnas de meses
        for col in existing_months:
            # Reemplazar valores especiales
            df[col] = df[col].replace(['#DIV/0!', '#DIV/0', 'NA', 'N/A', 'na', ''], np.nan)
            
            # Convertir a string y limpiar porcentajes
            df[col] = df[col].astype(str).str.replace('%', '').str.strip()
            
            # Convertir a numérico
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Limpiar columna Meta
        if 'Meta' in df.columns:
            df['Meta'] = df['Meta'].replace(['NA', 'N/A', ''], np.nan)
            df['Meta'] = df['Meta'].astype(str).str.replace('%', '').str.strip()
            df['Meta'] = pd.to_numeric(df['Meta'], errors='coerce')
        
        # Limpiar columnas de semaforización
        semaforo_cols = ['Nivel Obtenido', 'Nivel Satisfactorio', 'Nivel Crítico']
        for col in semaforo_cols:
            if col in df.columns:
                df[col] = df[col].replace(['NA', 'N/A', ''], np.nan)
                df[col] = df[col].astype(str).str.replace('%', '').str.strip()
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        self.df_processed = df
        self.metadata['valid_indicators'] = len(df)
        self.metadata['invalid_indicators'] = self.metadata['total_indicators'] - len(df)
        
        logger.info(f"Limpieza completada. Indicadores válidos: {len(df)}")
        
        return df
    
    def extract_historico_from_sheet(self, sheet_name: str) -> Dict:
        """
        Extrae el histórico completo de un indicador desde su hoja individual.
        
        Args:
            sheet_name (str): Nombre de la hoja del indicador
            
        Returns:
            Dict: Diccionario con datos históricos por trimestre/periodo
        """
        try:
            df_sheet = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                header=None,
                engine='xlrd'
            )
            
            # Buscar la fila "RESULTADOS VIGENCIA"
            resultados_row = None
            for i in range(len(df_sheet)):
                if pd.notna(df_sheet.iloc[i, 1]) and 'RESULTADOS VIGENCIA' in str(df_sheet.iloc[i, 1]):
                    resultados_row = i
                    break
            
            if resultados_row is None:
                return {}
            
            # La siguiente fila tiene los encabezados de periodos
            periodos_row = resultados_row + 1
            resultado_row = None
            
            # Buscar la fila con "RESULTADO"
            for i in range(periodos_row, min(periodos_row + 10, len(df_sheet))):
                if pd.notna(df_sheet.iloc[i, 0]) and 'RESULTADO' in str(df_sheet.iloc[i, 0]).upper():
                    resultado_row = i
                    break
            
            if resultado_row is None:
                return {}
            
            # Extraer periodos y valores
            historico = {}
            
            # Leer encabezados de periodos y valores
            for col in range(1, df_sheet.shape[1]):
                periodo = df_sheet.iloc[periodos_row, col]
                if pd.notna(periodo) and str(periodo) not in ['Promedio', 'NaN', 'nan', '']:
                    valor = df_sheet.iloc[resultado_row, col]
                    if pd.notna(valor):
                        try:
                            historico[str(periodo)] = float(valor)
                        except (ValueError, TypeError):
                            pass
            
            return historico
            
        except Exception as e:
            logger.debug(f"No se pudo extraer histórico de {sheet_name}: {e}")
            return {}
    
    def extract_indicators_data(self, incluir_historico: bool = True) -> List[Dict]:
        """
        Extrae información estructurada de cada indicador.
        
        Args:
            incluir_historico (bool): Si True, extrae datos históricos de las hojas individuales
        
        Returns:
            List[Dict]: Lista de diccionarios con datos de cada indicador
        """
        logger.info("Extrayendo datos estructurados de indicadores...")
        
        if self.df_processed is None:
            raise ValueError("No hay datos procesados. Ejecute clean_data() primero.")
        
        indicators_data = []
        
        month_columns = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        existing_months = [col for col in month_columns if col in self.df_processed.columns]
        
        # Obtener lista de hojas disponibles si se requiere histórico
        hojas_disponibles = []
        if incluir_historico:
            try:
                xl_file = pd.ExcelFile(self.file_path, engine='xlrd')
                hojas_disponibles = [h for h in xl_file.sheet_names if h != 'CONSOLIDADO']
                logger.info(f"Extrayendo histórico de {len(hojas_disponibles)} hojas individuales")
            except Exception as e:
                logger.warning(f"No se pudieron listar las hojas: {e}")
                incluir_historico = False
        
        for idx, row in self.df_processed.iterrows():
            # Extraer valores mensuales del consolidado (año actual)
            monthly_values = {}
            for month in existing_months:
                value = row.get(month, np.nan)
                if pd.notna(value):
                    monthly_values[month] = float(value)
            
            # Intentar extraer histórico de hoja individual
            historico = {}
            if incluir_historico and hojas_disponibles:
                num_indicador = int(row.get('#', idx + 1))
                if 0 < num_indicador <= len(hojas_disponibles):
                    hoja_nombre = hojas_disponibles[num_indicador - 1]
                    historico = self.extract_historico_from_sheet(hoja_nombre)
                    if historico:
                        logger.debug(f"Indicador {num_indicador}: {len(historico)} periodos históricos")
            
            # Combinar valores actuales y históricos
            valores_completos = {**historico, **monthly_values}
            
            # Crear diccionario de indicador
            indicator = {
                'id': idx,
                'numero': int(row.get('#', idx + 1)),
                'nombre': row.get('Nombre del Indicador', 'Sin nombre'),
                'meta': row.get('Meta', np.nan),
                'nivel_obtenido': row.get('Nivel Obtenido', np.nan),
                'nivel_satisfactorio': row.get('Nivel Satisfactorio', np.nan),
                'nivel_critico': row.get('Nivel Crítico', np.nan),
                'valores_mensuales': valores_completos,  # Histórico + año actual
                'historico': historico,  # Solo histórico (para referencia)
                'valores_actuales': monthly_values,  # Solo año actual (para referencia)
                'total_periodos': len(valores_completos),
                'promedio': np.mean(list(monthly_values.values())) if monthly_values else np.nan
            }
            
            indicators_data.append(indicator)
        
        logger.info(f"Extracción completada: {len(indicators_data)} indicadores procesados")
        
        return indicators_data
    
    def get_summary(self) -> Dict:
        """
        Genera un resumen del procesamiento de datos.
        
        Returns:
            Dict: Diccionario con estadísticas del procesamiento
        """
        summary = {
            'metadata': self.metadata,
            'shape': self.df_processed.shape if self.df_processed is not None else (0, 0),
            'columns': list(self.df_processed.columns) if self.df_processed is not None else [],
            'missing_values': self.df_processed.isnull().sum().to_dict() if self.df_processed is not None else {}
        }
        
        return summary


def load_and_process_excel(file_path: str) -> Tuple[pd.DataFrame, List[Dict], Dict]:
    """
    Función de conveniencia para cargar y procesar el archivo Excel en un solo paso.
    
    Args:
        file_path (str): Ruta al archivo Excel
        
    Returns:
        Tuple[pd.DataFrame, List[Dict], Dict]: (dataframe_procesado, lista_indicadores, resumen)
        
    Example:
        >>> df, indicators, summary = load_and_process_excel("tablero.xls")
        >>> print(f"Se procesaron {len(indicators)} indicadores")
    """
    loader = ExcelDataLoader(file_path)
    
    # Cargar datos
    loader.load_data()
    
    # Validar estructura
    is_valid, errors = loader.validate_structure()
    if not is_valid:
        logger.warning(f"Advertencias de validación: {errors}")
    
    # Limpiar datos
    df_clean = loader.clean_data()
    
    # Extraer indicadores
    indicators = loader.extract_indicators_data()
    
    # Obtener resumen
    summary = loader.get_summary()
    
    return df_clean, indicators, summary
