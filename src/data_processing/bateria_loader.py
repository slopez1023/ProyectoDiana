"""
Módulo para cargar y procesar la batería de indicadores sectoriales.

Este módulo maneja el archivo Excel con múltiples hojas, cada una representando
un sector diferente del plan de desarrollo.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BateriaIndicadoresLoader:
    """
    Clase para cargar indicadores sectoriales desde archivo Excel multi-hoja.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.sectores_data = {}
        self.metadata = {
            'file_path': file_path,
            'load_timestamp': datetime.now(),
            'total_sectores': 0,
            'total_indicadores': 0
        }
    
    def load_all_sectores(self) -> Dict[str, pd.DataFrame]:
        """
        Carga todas las hojas del archivo (excepto hojas vacías).
        
        Returns:
            Dict: Diccionario con nombre_sector: dataframe
        """
        logger.info(f"Cargando batería de indicadores desde: {self.file_path}")
        
        # Obtener lista de hojas
        xl_file = pd.ExcelFile(self.file_path)
        hojas = xl_file.sheet_names
        
        # Excluir hojas vacías o irrelevantes
        hojas_validas = [h for h in hojas if h not in ['Hoja1', 'Sheet1', 'Sheet2']]
        
        logger.info(f"Se encontraron {len(hojas_validas)} sectores válidos")
        
        for hoja in hojas_validas:
            try:
                df = self._load_sector(hoja)
                if df is not None and len(df) > 0:
                    self.sectores_data[hoja] = df
                    logger.info(f"Sector '{hoja}' cargado: {len(df)} indicadores")
            except Exception as e:
                logger.error(f"Error al cargar sector '{hoja}': {e}")
        
        self.metadata['total_sectores'] = len(self.sectores_data)
        self.metadata['total_indicadores'] = sum(len(df) for df in self.sectores_data.values())
        
        return self.sectores_data
    
    def _load_sector(self, sheet_name: str) -> pd.DataFrame:
        """
        Carga una hoja específica del archivo.
        
        Args:
            sheet_name: Nombre de la hoja a cargar
            
        Returns:
            DataFrame procesado del sector
        """
        # Leer sin encabezados para detectar estructura
        df_temp = pd.read_excel(
            self.file_path,
            sheet_name=sheet_name,
            header=None
        )
        
        # Buscar fila de encabezados (contiene "Código Sector")
        header_row = None
        for i in range(min(10, len(df_temp))):
            row_values = df_temp.iloc[i].astype(str).tolist()
            if any('Código Sector' in str(val) for val in row_values):
                header_row = i
                break
        
        if header_row is None:
            logger.warning(f"No se encontraron encabezados en hoja {sheet_name}")
            return None
        
        # Leer con encabezados correctos
        df = pd.read_excel(
            self.file_path,
            sheet_name=sheet_name,
            header=header_row
        )
        
        # Limpiar datos
        df = df.dropna(how='all')  # Eliminar filas vacías
        df = df.reset_index(drop=True)
        
        # Agregar columna de sector
        df['Sector_Hoja'] = sheet_name
        
        return df
    
    def extract_indicadores_por_sector(self) -> Dict[str, List[Dict]]:
        """
        Extrae información estructurada de indicadores por sector.
        
        Returns:
            Dict: {nombre_sector: [lista_de_indicadores]}
        """
        logger.info("Extrayendo indicadores por sector...")
        
        indicadores_por_sector = {}
        
        for sector, df in self.sectores_data.items():
            indicadores = []
            
            for idx, row in df.iterrows():
                # Buscar columnas de valores numéricos (resultados mensuales/anuales)
                valores_dict = {}
                for col in df.columns:
                    if col not in ['Código Sector', 'Sector', 'Código Objetivo Resultado', 
                                   'Objetivo de Resultado', 'Código Indicador de Resultado',
                                   'Indicador de Resultado', 'Unidad de Medida', 'Meta Cuatrienio',
                                   'Sector_Hoja']:
                        valor = row.get(col)
                        if pd.notna(valor) and isinstance(valor, (int, float)):
                            valores_dict[str(col)] = float(valor)
                
                indicador = {
                    'id': f"{sector}_{idx}",
                    'sector': sector,
                    'codigo_sector': row.get('Código Sector', ''),
                    'nombre_sector': row.get('Sector', sector),
                    'codigo_objetivo': row.get('Código Objetivo Resultado', ''),
                    'objetivo': row.get('Objetivo de Resultado', ''),
                    'codigo_indicador': row.get('Código Indicador de Resultado', ''),
                    'nombre': row.get('Indicador de Resultado', 'Sin nombre'),
                    'unidad_medida': row.get('Unidad de Medida', ''),
                    'meta_cuatrienio': row.get('Meta Cuatrienio', np.nan),
                    'meta': row.get('Meta Cuatrienio', np.nan),  # Alias para compatibilidad
                    'valores': valores_dict,
                    'valores_mensuales': valores_dict,  # Alias para compatibilidad con visualización
                    'total_periodos': len(valores_dict),
                    'promedio': np.mean(list(valores_dict.values())) if valores_dict else np.nan
                }
                
                indicadores.append(indicador)
            
            indicadores_por_sector[sector] = indicadores
        
        logger.info(f"Extracción completada: {len(indicadores_por_sector)} sectores procesados")
        
        return indicadores_por_sector
    
    def get_all_indicadores_flat(self) -> List[Dict]:
        """
        Obtiene todos los indicadores en una lista plana.
        
        Returns:
            List: Lista de todos los indicadores de todos los sectores
        """
        indicadores_por_sector = self.extract_indicadores_por_sector()
        
        todos_indicadores = []
        for indicadores in indicadores_por_sector.values():
            todos_indicadores.extend(indicadores)
        
        return todos_indicadores
    
    def get_summary(self) -> Dict:
        """
        Genera resumen de la batería de indicadores.
        
        Returns:
            Dict: Resumen con estadísticas
        """
        return {
            'metadata': self.metadata,
            'sectores': list(self.sectores_data.keys()),
            'total_sectores': self.metadata['total_sectores'],
            'total_indicadores': self.metadata['total_indicadores']
        }


def load_and_process_bateria(file_path: str) -> Tuple[Dict[str, pd.DataFrame], Dict[str, List[Dict]], Dict]:
    """
    Función de conveniencia para cargar y procesar la batería de indicadores.
    
    Args:
        file_path: Ruta al archivo Excel
        
    Returns:
        Tuple: (dict_dataframes_por_sector, dict_indicadores_por_sector, resumen)
    """
    loader = BateriaIndicadoresLoader(file_path)
    
    # Cargar todos los sectores
    sectores_df = loader.load_all_sectores()
    
    # Extraer indicadores
    indicadores_por_sector = loader.extract_indicadores_por_sector()
    
    # Obtener resumen
    summary = loader.get_summary()
    
    return sectores_df, indicadores_por_sector, summary
