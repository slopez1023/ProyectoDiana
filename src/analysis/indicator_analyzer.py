"""
Módulo de análisis de indicadores.

Clasifica indicadores por periodicidad, calcula tendencias, identifica anomalías
y genera análisis automatizados del comportamiento de los indicadores MIPG.

Implementa:
- Clasificación automática de periodicidad
- Análisis de tendencias (crecimiento, estabilidad, retroceso)
- Detección de anomalías estadísticas
- Cálculo de cumplimiento de metas
- Semaforización automática
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Periodicidad(Enum):
    """Enumeración de tipos de periodicidad de indicadores."""
    MENSUAL = "Mensual"
    BIMESTRAL = "Bimestral"
    TRIMESTRAL = "Trimestral"
    CUATRIMESTRAL = "Cuatrimestral"
    SEMESTRAL = "Semestral"
    ANUAL = "Anual"
    INDETERMINADA = "Indeterminada"


class EstadoSemaforo(Enum):
    """Enumeración de estados del semáforo de indicadores."""
    VERDE = "Verde"  # Cumplimiento satisfactorio
    AMARILLO = "Amarillo"  # Cumplimiento aceptable con alertas
    ROJO = "Rojo"  # Cumplimiento crítico o incumplimiento
    GRIS = "Gris"  # Sin datos suficientes


class TendenciaIndicador(Enum):
    """Enumeración de tipos de tendencia."""
    CRECIMIENTO = "Crecimiento"
    ESTABILIDAD = "Estabilidad"
    RETROCESO = "Retroceso"
    VOLATIL = "Volátil"
    INSUFICIENTE = "Datos Insuficientes"


class IndicatorAnalyzer:
    """
    Clase para análisis avanzado de indicadores MIPG.
    
    Aplica análisis estadísticos y de negocio para interpretar
    el comportamiento de los indicadores institucionales.
    """
    
    def __init__(self):
        """Inicializa el analizador de indicadores."""
        self.meses_orden = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        logger.info("IndicatorAnalyzer inicializado")
    
    def clasificar_periodicidad(self, valores_mensuales: Dict[str, float]) -> Periodicidad:
        """
        Clasifica automáticamente la periodicidad de un indicador
        basándose en el patrón de datos disponibles.
        
        Args:
            valores_mensuales (Dict[str, float]): Diccionario con valores por mes
            
        Returns:
            Periodicidad: Tipo de periodicidad identificada
            
        Algoritmo:
        - Analiza la frecuencia de datos no nulos
        - Identifica patrones de captura (cada mes, cada 3 meses, etc.)
        - Retorna la periodicidad más probable
        """
        if not valores_mensuales:
            return Periodicidad.INDETERMINADA
        
        # Contar meses con datos
        meses_con_datos = len([v for v in valores_mensuales.values() if pd.notna(v)])
        
        # Identificar posiciones de meses con datos
        posiciones = []
        for i, mes in enumerate(self.meses_orden):
            if mes in valores_mensuales and pd.notna(valores_mensuales[mes]):
                posiciones.append(i)
        
        if len(posiciones) == 0:
            return Periodicidad.INDETERMINADA
        
        # Analizar intervalos entre mediciones
        if len(posiciones) > 1:
            intervalos = [posiciones[i+1] - posiciones[i] for i in range(len(posiciones)-1)]
            intervalo_promedio = np.mean(intervalos)
            
            # Clasificar según intervalo promedio
            if intervalo_promedio <= 1.5:
                return Periodicidad.MENSUAL
            elif 1.5 < intervalo_promedio <= 2.5:
                return Periodicidad.BIMESTRAL
            elif 2.5 < intervalo_promedio <= 3.5:
                return Periodicidad.TRIMESTRAL
            elif 3.5 < intervalo_promedio <= 5:
                return Periodicidad.CUATRIMESTRAL
            elif 5 < intervalo_promedio <= 7:
                return Periodicidad.SEMESTRAL
            else:
                return Periodicidad.ANUAL
        
        # Si solo hay un dato, analizar por cantidad de meses
        if meses_con_datos == 12:
            return Periodicidad.MENSUAL
        elif meses_con_datos == 6:
            return Periodicidad.BIMESTRAL
        elif meses_con_datos == 4:
            return Periodicidad.TRIMESTRAL
        elif meses_con_datos == 3:
            return Periodicidad.CUATRIMESTRAL
        elif meses_con_datos == 2:
            return Periodicidad.SEMESTRAL
        elif meses_con_datos == 1:
            return Periodicidad.ANUAL
        else:
            return Periodicidad.INDETERMINADA
    
    def calcular_semaforo(
        self,
        valor_actual: float,
        meta: float,
        nivel_satisfactorio: Optional[float] = None,
        nivel_critico: Optional[float] = None,
        nivel_obtenido: Optional[float] = None
    ) -> EstadoSemaforo:
        """
        Calcula el estado del semáforo para un indicador.
        
        Args:
            valor_actual (float): Valor actual del indicador
            meta (float): Meta establecida
            nivel_satisfactorio (float, optional): Umbral para verde
            nivel_critico (float, optional): Umbral para rojo
            nivel_obtenido (float, optional): Nivel obtenido (alternativa para nivel_satisfactorio)
            
        Returns:
            EstadoSemaforo: Estado calculado del semáforo
            
        Lógica de semaforización:
        - Verde: Cumple o supera nivel satisfactorio
        - Amarillo: Entre nivel crítico y nivel satisfactorio
        - Rojo: Por debajo del nivel crítico
        """
        # Si no hay valor actual, devolver gris
        if pd.isna(valor_actual):
            return EstadoSemaforo.GRIS
        
        # Si no hay meta ni nivel_obtenido, usar valor actual vs 100%
        if pd.isna(meta) and pd.isna(nivel_obtenido):
            # Clasificar por magnitud del valor actual
            if valor_actual >= 80:
                return EstadoSemaforo.VERDE
            elif valor_actual >= 60:
                return EstadoSemaforo.AMARILLO
            else:
                return EstadoSemaforo.ROJO
        
        # Determinar si es un indicador invertido (menor es mejor)
        # Ejemplos: PQRS Vencidos, Ausentismo, Accidentalidad, etc.
        es_invertido = False
        if pd.notna(meta) and pd.notna(nivel_critico):
            es_invertido = nivel_critico > meta  # Si el nivel crítico es mayor que la meta, es invertido
        
        # Si no hay niveles definidos, usar valores de meta o nivel_obtenido
        if pd.isna(nivel_satisfactorio):
            if pd.notna(nivel_obtenido):
                nivel_satisfactorio = nivel_obtenido
            elif pd.notna(meta):
                nivel_satisfactorio = meta
            else:
                nivel_satisfactorio = 0.80  # 80% como valor por defecto
        
        if pd.isna(nivel_critico):
            if pd.notna(meta):
                if es_invertido:
                    nivel_critico = meta * 1.25  # 125% de la meta (peor)
                else:
                    nivel_critico = meta * 0.75  # 75% de la meta
            else:
                if es_invertido:
                    nivel_critico = nivel_satisfactorio * 1.25
                else:
                    nivel_critico = nivel_satisfactorio * 0.75
        
        # Normalizar valores si están en diferentes escalas
        # Si la meta o niveles están en rango 0-1 y el valor actual está en 0-100, convertir
        if valor_actual > 1 and nivel_satisfactorio <= 1:
            valor_actual = valor_actual / 100
        # Si el valor actual está en 0-1 y los niveles están en 0-100, convertir niveles
        elif valor_actual <= 1 and nivel_satisfactorio > 1:
            nivel_satisfactorio = nivel_satisfactorio / 100
            nivel_critico = nivel_critico / 100 if pd.notna(nivel_critico) else nivel_critico
        
        # Determinar estado según si es indicador normal o invertido
        if es_invertido:
            # Para indicadores invertidos (menor es mejor): PQRS Vencidos, Ausentismo, etc.
            if valor_actual <= nivel_satisfactorio:
                return EstadoSemaforo.VERDE
            elif valor_actual <= nivel_critico:
                return EstadoSemaforo.AMARILLO
            else:
                return EstadoSemaforo.ROJO
        else:
            # Para indicadores normales (mayor es mejor)
            if valor_actual >= nivel_satisfactorio:
                return EstadoSemaforo.VERDE
            elif valor_actual >= nivel_critico:
                return EstadoSemaforo.AMARILLO
            else:
                return EstadoSemaforo.ROJO
    
    def analizar_tendencia(self, valores_mensuales: Dict[str, float]) -> Tuple[TendenciaIndicador, float]:
        """
        Analiza la tendencia de un indicador basándose en sus valores históricos.
        
        Args:
            valores_mensuales (Dict[str, float]): Valores por mes
            
        Returns:
            Tuple[TendenciaIndicador, float]: (tipo_tendencia, pendiente_calculada)
            
        Algoritmo:
        - Ordena valores cronológicamente
        - Calcula regresión lineal simple
        - Analiza variabilidad (desviación estándar)
        - Clasifica la tendencia según pendiente y variabilidad
        """
        if not valores_mensuales or len(valores_mensuales) < 2:
            return TendenciaIndicador.INSUFICIENTE, 0.0
        
        # Ordenar valores por mes
        valores_ordenados = []
        for mes in self.meses_orden:
            if mes in valores_mensuales and pd.notna(valores_mensuales[mes]):
                valores_ordenados.append(valores_mensuales[mes])
        
        if len(valores_ordenados) < 2:
            return TendenciaIndicador.INSUFICIENTE, 0.0
        
        # Calcular pendiente simple (regresión lineal)
        x = np.arange(len(valores_ordenados))
        y = np.array(valores_ordenados)
        
        # Regresión lineal: y = mx + b
        pendiente = np.polyfit(x, y, 1)[0]
        
        # Calcular variabilidad
        desviacion = np.std(valores_ordenados)
        promedio = np.mean(valores_ordenados)
        coef_variacion = (desviacion / promedio * 100) if promedio != 0 else 0
        
        # Clasificar tendencia
        umbral_estabilidad = 0.5  # Pendiente casi nula
        umbral_volatilidad = 15.0  # Coeficiente de variación alto
        
        if coef_variacion > umbral_volatilidad:
            return TendenciaIndicador.VOLATIL, pendiente
        elif abs(pendiente) < umbral_estabilidad:
            return TendenciaIndicador.ESTABILIDAD, pendiente
        elif pendiente > 0:
            return TendenciaIndicador.CRECIMIENTO, pendiente
        else:
            return TendenciaIndicador.RETROCESO, pendiente
    
    def detectar_anomalias(self, valores_mensuales: Dict[str, float]) -> List[Dict]:
        """
        Detecta valores anómalos usando el método de Z-score.
        
        Args:
            valores_mensuales (Dict[str, float]): Valores por mes
            
        Returns:
            List[Dict]: Lista de anomalías detectadas con detalles
            
        Criterio de anomalía:
        - Z-score > 2.5 (valor atípicamente alto)
        - Z-score < -2.5 (valor atípicamente bajo)
        """
        anomalias = []
        
        valores = [v for v in valores_mensuales.values() if pd.notna(v)]
        
        if len(valores) < 3:
            return anomalias  # No suficientes datos para detectar anomalías
        
        media = np.mean(valores)
        desviacion = np.std(valores)
        
        if desviacion == 0:
            return anomalias  # No hay variabilidad
        
        for mes, valor in valores_mensuales.items():
            if pd.notna(valor):
                z_score = (valor - media) / desviacion
                
                if abs(z_score) > 2.5:
                    anomalias.append({
                        'mes': mes,
                        'valor': valor,
                        'z_score': z_score,
                        'tipo': 'Alto' if z_score > 0 else 'Bajo',
                        'desviacion_porcentual': ((valor - media) / media * 100)
                    })
        
        return anomalias
    
    def calcular_estadisticas(self, valores_mensuales: Dict[str, float]) -> Dict:
        """
        Calcula estadísticas descriptivas del indicador.
        
        Args:
            valores_mensuales (Dict[str, float]): Valores por mes
            
        Returns:
            Dict: Diccionario con estadísticas calculadas
        """
        valores = [v for v in valores_mensuales.values() if pd.notna(v)]
        
        if not valores:
            return {
                'promedio': np.nan,
                'mediana': np.nan,
                'desviacion_estandar': np.nan,
                'minimo': np.nan,
                'maximo': np.nan,
                'rango': np.nan,
                'coeficiente_variacion': np.nan,
                'total_periodos': 0
            }
        
        promedio = np.mean(valores)
        
        return {
            'promedio': promedio,
            'mediana': np.median(valores),
            'desviacion_estandar': np.std(valores),
            'minimo': np.min(valores),
            'maximo': np.max(valores),
            'rango': np.max(valores) - np.min(valores),
            'coeficiente_variacion': (np.std(valores) / promedio * 100) if promedio != 0 else 0,
            'total_periodos': len(valores)
        }
    
    def generar_analisis_completo(self, indicador: Dict) -> Dict:
        """
        Genera un análisis completo de un indicador individual.
        
        Args:
            indicador (Dict): Diccionario con datos del indicador
            
        Returns:
            Dict: Análisis completo con todas las métricas
        """
        valores_mensuales = indicador.get('valores_mensuales', {})
        
        # Clasificar periodicidad
        periodicidad = self.clasificar_periodicidad(valores_mensuales)
        
        # Analizar tendencia
        tendencia, pendiente = self.analizar_tendencia(valores_mensuales)
        
        # Calcular estadísticas
        estadisticas = self.calcular_estadisticas(valores_mensuales)
        
        # Detectar anomalías
        anomalias = self.detectar_anomalias(valores_mensuales)
        
        # Calcular semáforo (usando el último valor disponible o el promedio)
        ultimo_valor = None
        for mes in reversed(self.meses_orden):
            if mes in valores_mensuales and pd.notna(valores_mensuales[mes]):
                ultimo_valor = valores_mensuales[mes]
                break
        
        # Si no hay último valor, usar el promedio
        if ultimo_valor is None and valores_mensuales:
            valores_lista = [v for v in valores_mensuales.values() if pd.notna(v)]
            if valores_lista:
                ultimo_valor = np.mean(valores_lista)
        
        semaforo = self.calcular_semaforo(
            ultimo_valor if ultimo_valor is not None else np.nan,
            indicador.get('meta', np.nan),
            indicador.get('nivel_satisfactorio', np.nan),
            indicador.get('nivel_critico', np.nan),
            indicador.get('nivel_obtenido', np.nan)
        )
        
        # Generar interpretación textual
        interpretacion = self._generar_interpretacion(
            indicador['nombre'],
            periodicidad,
            tendencia,
            semaforo,
            estadisticas,
            anomalias
        )
        
        return {
            'indicador_id': indicador.get('id'),
            'nombre': indicador.get('nombre'),
            'periodicidad': periodicidad.value,
            'tendencia': tendencia.value,
            'pendiente': pendiente,
            'semaforo': semaforo.value,
            'estadisticas': estadisticas,
            'anomalias': anomalias,
            'total_anomalias': len(anomalias),
            'interpretacion': interpretacion,
            'ultima_actualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _generar_interpretacion(
        self,
        nombre: str,
        periodicidad: Periodicidad,
        tendencia: TendenciaIndicador,
        semaforo: EstadoSemaforo,
        estadisticas: Dict,
        anomalias: List[Dict]
    ) -> str:
        """
        Genera una interpretación textual automática del indicador.
        
        Returns:
            str: Texto de interpretación para el usuario
        """
        partes = []
        
        # Introducción
        partes.append(f"El indicador '{nombre}' presenta periodicidad {periodicidad.value.lower()}.")
        
        # Tendencia
        if tendencia == TendenciaIndicador.CRECIMIENTO:
            partes.append("Se observa una tendencia de crecimiento positivo en los valores registrados.")
        elif tendencia == TendenciaIndicador.RETROCESO:
            partes.append("Se identifica una tendencia de retroceso que requiere atención.")
        elif tendencia == TendenciaIndicador.ESTABILIDAD:
            partes.append("Los valores se mantienen estables a lo largo del período analizado.")
        elif tendencia == TendenciaIndicador.VOLATIL:
            partes.append("Se presenta alta variabilidad en los valores, indicando comportamiento volátil.")
        
        # Semáforo
        if semaforo == EstadoSemaforo.VERDE:
            partes.append("El estado actual es SATISFACTORIO, cumpliendo con las metas establecidas.")
        elif semaforo == EstadoSemaforo.AMARILLO:
            partes.append("El estado actual es ACEPTABLE, pero requiere seguimiento para evitar deterioro.")
        elif semaforo == EstadoSemaforo.ROJO:
            partes.append("El estado actual es CRÍTICO, no cumpliendo con los niveles mínimos esperados.")
        
        # Estadísticas
        if pd.notna(estadisticas['promedio']):
            partes.append(f"El promedio de los valores es {estadisticas['promedio']:.2f}%.")
        
        # Anomalías
        if anomalias:
            partes.append(f"Se detectaron {len(anomalias)} valores anómalos que requieren revisión.")
        
        return " ".join(partes)


def analizar_todos_indicadores(indicadores_list: List[Dict]) -> List[Dict]:
    """
    Analiza una lista completa de indicadores.
    
    Args:
        indicadores_list (List[Dict]): Lista de indicadores a analizar
        
    Returns:
        List[Dict]: Lista de análisis completos
    """
    analyzer = IndicatorAnalyzer()
    resultados = []
    
    logger.info(f"Iniciando análisis de {len(indicadores_list)} indicadores...")
    
    for indicador in indicadores_list:
        try:
            analisis = analyzer.generar_analisis_completo(indicador)
            resultados.append(analisis)
        except Exception as e:
            logger.error(f"Error al analizar indicador {indicador.get('nombre')}: {str(e)}")
            continue
    
    logger.info(f"Análisis completado: {len(resultados)} indicadores procesados")
    
    return resultados
