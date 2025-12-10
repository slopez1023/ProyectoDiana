"""
Módulo de visualización de indicadores.

Genera gráficos profesionales para el análisis de indicadores MIPG:
- Gráficos de tendencia temporal
- Gráficos comparativos entre indicadores
- Visualizaciones con semaforización
- Dashboards interactivos con Plotly

Utiliza Plotly para gráficos interactivos y Matplotlib para exportación estática.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Configuración de estilos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Colores institucionales para semaforización
COLORS_SEMAFORO = {
    'Verde': '#28a745',      # Verde satisfactorio
    'Amarillo': '#ffc107',   # Amarillo alerta
    'Rojo': '#dc3545',       # Rojo crítico
    'Gris': '#6c757d'        # Gris sin datos
}

# Paleta de colores profesional
COLOR_PALETTE = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']


class ChartGenerator:
    """
    Generador de gráficos para indicadores MIPG.
    
    Crea visualizaciones profesionales siguiendo estándares
    de diseño para entidades públicas.
    """
    
    def __init__(self, theme: str = 'plotly_white'):
        """
        Inicializa el generador de gráficos.
        
        Args:
            theme (str): Tema de Plotly a utilizar
        """
        self.theme = theme
        self.meses_orden = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        logger.info("ChartGenerator inicializado")
    
    def grafico_tendencia_indicador(
        self,
        indicador: Dict,
        analisis: Dict,
        mostrar_meta: bool = True,
        titulo_personalizado: Optional[str] = None
    ) -> go.Figure:
        """
        Genera gráfico de tendencia temporal para un indicador individual.
        
        Args:
            indicador (Dict): Datos del indicador
            analisis (Dict): Análisis del indicador
            mostrar_meta (bool): Si se debe mostrar línea de meta
            titulo_personalizado (str, optional): Título personalizado
            
        Returns:
            go.Figure: Figura de Plotly con el gráfico
        """
        valores_mensuales = indicador.get('valores_mensuales', {})
        
        if not valores_mensuales:
            nombre_ind = indicador.get('nombre', 'Indicador')
            if not isinstance(nombre_ind, str):
                nombre_ind = str(nombre_ind)
            logger.warning(f"No hay datos para graficar: {nombre_ind}")
            return None
        
        # Detectar si son meses o años (u otros períodos)
        periodos_disponibles = list(valores_mensuales.keys())
        es_mensual = any(mes in periodos_disponibles for mes in self.meses_orden)
        
        # Preparar datos según el tipo
        periodos = []
        valores = []
        
        if es_mensual:
            # Datos mensuales - usar orden de meses
            for mes in self.meses_orden:
                if mes in valores_mensuales and pd.notna(valores_mensuales[mes]):
                    periodos.append(mes)
                    valores.append(valores_mensuales[mes])
        else:
            # Datos anuales u otros - ordenar las claves
            for periodo in sorted(periodos_disponibles):
                if pd.notna(valores_mensuales[periodo]):
                    periodos.append(str(periodo))
                    valores.append(valores_mensuales[periodo])
        
        if not periodos:
            nombre_ind = indicador.get('nombre', 'Indicador')
            if not isinstance(nombre_ind, str):
                nombre_ind = str(nombre_ind)
            logger.warning(f"No hay datos válidos para graficar: {nombre_ind}")
            return None
        
        # Crear figura
        fig = go.Figure()
        
        # Línea de tendencia principal
        color_linea = self._get_color_by_semaforo(analisis.get('semaforo', 'Gris'))
        
        fig.add_trace(go.Scatter(
            x=periodos,
            y=valores,
            mode='lines+markers',
            name='Valor Real',
            line=dict(color=color_linea, width=3),
            marker=dict(size=10, line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Valor: %{y:.2f}%<extra></extra>'
        ))
        
        # Agregar línea de meta
        if mostrar_meta and pd.notna(indicador.get('meta')):
            meta = indicador.get('meta')
            fig.add_trace(go.Scatter(
                x=periodos,
                y=[meta] * len(periodos),
                mode='lines',
                name='Meta',
                line=dict(color='#dc3545', width=2, dash='dash'),
                hovertemplate='<b>Meta</b><br>%{y:.2f}%<extra></extra>'
            ))
        
        # Título y etiquetas
        nombre_ind = indicador.get('nombre', 'Indicador')
        if not isinstance(nombre_ind, str):
            nombre_ind = str(nombre_ind)
        titulo = titulo_personalizado or f"{nombre_ind}"
        
        fig.update_layout(
            title={
                'text': titulo,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'family': 'Arial Black'}
            },
            xaxis_title='Período',
            yaxis_title='Valor (%)',
            template=self.theme,
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=500
        )
        
        # Agregar anotación de periodicidad y tendencia
        fig.add_annotation(
            text=f"Periodicidad: {analisis.get('periodicidad', 'N/A')} | "
                 f"Tendencia: {analisis.get('tendencia', 'N/A')} | "
                 f"Estado: {analisis.get('semaforo', 'N/A')}",
            xref="paper", yref="paper",
            x=0.5, y=-0.15,
            showarrow=False,
            font=dict(size=11, color='gray'),
            xanchor='center'
        )
        
        return fig
    
    def grafico_comparativo_indicadores(
        self,
        indicadores_list: List[Dict],
        analisis_list: List[Dict],
        top_n: int = 10,
        ordenar_por: str = 'promedio'
    ) -> go.Figure:
        """
        Genera gráfico comparativo de múltiples indicadores.
        
        Args:
            indicadores_list (List[Dict]): Lista de indicadores
            analisis_list (List[Dict]): Lista de análisis
            top_n (int): Cantidad de indicadores a mostrar
            ordenar_por (str): Criterio de ordenamiento
            
        Returns:
            go.Figure: Gráfico comparativo
        """
        # Preparar datos
        datos_comp = []
        
        for ind, anal in zip(indicadores_list[:top_n], analisis_list[:top_n]):
            estadisticas = anal.get('estadisticas', {})
            
            # Obtener nombre y convertir a string si es necesario
            nombre = ind.get('nombre', 'Sin nombre')
            if not isinstance(nombre, str):
                nombre = str(nombre)
            
            datos_comp.append({
                'nombre': nombre[:50],  # Truncar nombres largos
                'promedio': estadisticas.get('promedio', 0),
                'meta': ind.get('meta', 0),
                'semaforo': anal.get('semaforo', 'Gris')
            })
        
        df_comp = pd.DataFrame(datos_comp)
        
        if df_comp.empty:
            logger.warning("No hay datos para comparar")
            return None
        
        # Ordenar
        if ordenar_por == 'promedio':
            df_comp = df_comp.sort_values('promedio', ascending=True)
        
        # Crear figura
        fig = go.Figure()
        
        # Barras de promedio
        colors = [COLORS_SEMAFORO.get(s, '#6c757d') for s in df_comp['semaforo']]
        
        fig.add_trace(go.Bar(
            y=df_comp['nombre'],
            x=df_comp['promedio'],
            orientation='h',
            name='Promedio Real',
            marker=dict(color=colors),
            text=df_comp['promedio'].round(2),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Promedio: %{x:.2f}%<extra></extra>'
        ))
        
        # Línea de referencia de meta
        fig.add_trace(go.Scatter(
            y=df_comp['nombre'],
            x=df_comp['meta'],
            mode='markers',
            name='Meta',
            marker=dict(symbol='diamond', size=12, color='red'),
            hovertemplate='<b>%{y}</b><br>Meta: %{x:.2f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': f'Comparativo de Indicadores (Top {top_n})',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'family': 'Arial Black'}
            },
            xaxis_title='Valor Promedio (%)',
            yaxis_title='Indicador',
            template=self.theme,
            height=max(400, top_n * 50),
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        
        return fig
    
    def grafico_semaforizacion_general(
        self,
        analisis_list: List[Dict]
    ) -> go.Figure:
        """
        Genera gráfico de distribución de estados de semaforización.
        
        Args:
            analisis_list (List[Dict]): Lista de análisis de indicadores
            
        Returns:
            go.Figure: Gráfico de pastel con distribución
        """
        # Contar estados de semáforo
        conteo_semaforo = {}
        for anal in analisis_list:
            semaforo = anal.get('semaforo', 'Gris')
            conteo_semaforo[semaforo] = conteo_semaforo.get(semaforo, 0) + 1
        
        # Preparar datos
        labels = list(conteo_semaforo.keys())
        values = list(conteo_semaforo.values())
        colors = [COLORS_SEMAFORO.get(label, '#6c757d') for label in labels]
        
        # Crear gráfico de pastel
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>',
            textinfo='label+percent',
            textfont_size=13
        )])
        
        fig.update_layout(
            title={
                'text': 'Distribución de Estados de Semaforización',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'family': 'Arial Black'}
            },
            template=self.theme,
            height=500,
            showlegend=True
        )
        
        return fig
    
    def grafico_tendencias_multiple(
        self,
        indicadores_list: List[Dict],
        max_indicadores: int = 5
    ) -> go.Figure:
        """
        Genera gráfico con múltiples líneas de tendencia.
        
        Args:
            indicadores_list (List[Dict]): Lista de indicadores
            max_indicadores (int): Máximo de líneas a graficar
            
        Returns:
            go.Figure: Gráfico con múltiples tendencias
        """
        fig = go.Figure()
        
        for i, indicador in enumerate(indicadores_list[:max_indicadores]):
            valores_mensuales = indicador.get('valores_mensuales', {})
            
            if not valores_mensuales:
                continue
            
            # Detectar tipo de períodos
            periodos_disponibles = list(valores_mensuales.keys())
            es_mensual = any(mes in periodos_disponibles for mes in self.meses_orden)
            
            # Preparar datos
            periodos = []
            valores = []
            
            if es_mensual:
                for mes in self.meses_orden:
                    if mes in valores_mensuales and pd.notna(valores_mensuales[mes]):
                        periodos.append(mes)
                        valores.append(valores_mensuales[mes])
            else:
                for periodo in sorted(periodos_disponibles):
                    if pd.notna(valores_mensuales[periodo]):
                        periodos.append(str(periodo))
                        valores.append(valores_mensuales[periodo])
            
            if not periodos:
                continue
            
            # Agregar línea
            color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
            nombre = indicador.get('nombre', f'Indicador {i+1}')
            if not isinstance(nombre, str):
                nombre = str(nombre)
            nombre = nombre[:40]
            
            fig.add_trace(go.Scatter(
                x=periodos,
                y=valores,
                mode='lines+markers',
                name=nombre,
                line=dict(color=color, width=2),
                marker=dict(size=6),
                hovertemplate=f'<b>{nombre}</b><br>%{{x}}: %{{y:.2f}}%<extra></extra>'
            ))
        
        fig.update_layout(
            title={
                'text': 'Tendencias Comparativas de Indicadores',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'family': 'Arial Black'}
            },
            xaxis_title='Período',
            yaxis_title='Valor (%)',
            template=self.theme,
            hovermode='x unified',
            height=600,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        return fig
    
    def grafico_estadisticas_generales(
        self,
        analisis_list: List[Dict],
        top_n: int = 15
    ) -> go.Figure:
        """
        Genera gráfico de caja (boxplot) con estadísticas de indicadores.
        
        Args:
            analisis_list (List[Dict]): Lista de análisis
            top_n (int): Número de indicadores a mostrar
            
        Returns:
            go.Figure: Gráfico de estadísticas
        """
        # Preparar datos
        datos = []
        
        for anal in analisis_list[:top_n]:
            estadisticas = anal.get('estadisticas', {})
            if estadisticas.get('total_periodos', 0) > 0:
                datos.append({
                    'nombre': anal.get('nombre', 'Sin nombre')[:30],
                    'promedio': estadisticas.get('promedio', 0),
                    'minimo': estadisticas.get('minimo', 0),
                    'maximo': estadisticas.get('maximo', 0),
                    'desviacion': estadisticas.get('desviacion_estandar', 0)
                })
        
        df = pd.DataFrame(datos)
        
        if df.empty:
            return None
        
        # Crear subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Promedios por Indicador', 'Rango (Mín-Máx) por Indicador')
        )
        
        # Gráfico de promedios
        fig.add_trace(
            go.Bar(
                y=df['nombre'],
                x=df['promedio'],
                orientation='h',
                name='Promedio',
                marker=dict(color='#2E86AB'),
                text=df['promedio'].round(2),
                textposition='outside'
            ),
            row=1, col=1
        )
        
        # Gráfico de rangos
        fig.add_trace(
            go.Scatter(
                y=df['nombre'],
                x=df['minimo'],
                mode='markers',
                name='Mínimo',
                marker=dict(symbol='triangle-left', size=10, color='#C73E1D')
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                y=df['nombre'],
                x=df['maximo'],
                mode='markers',
                name='Máximo',
                marker=dict(symbol='triangle-right', size=10, color='#6A994E')
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title={
                'text': 'Estadísticas Generales de Indicadores',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'family': 'Arial Black'}
            },
            template=self.theme,
            height=max(500, top_n * 40),
            showlegend=True
        )
        
        return fig
    
    def _get_color_by_semaforo(self, semaforo: str) -> str:
        """
        Obtiene el color correspondiente al estado del semáforo.
        
        Args:
            semaforo (str): Estado del semáforo
            
        Returns:
            str: Código de color hexadecimal
        """
        return COLORS_SEMAFORO.get(semaforo, '#6c757d')
    
    def guardar_grafico(self, fig: go.Figure, ruta_salida: str, formato: str = 'html'):
        """
        Guarda un gráfico en el formato especificado.
        
        Args:
            fig (go.Figure): Figura de Plotly a guardar
            ruta_salida (str): Ruta donde guardar el archivo
            formato (str): Formato de salida ('html', 'png', 'pdf', 'svg')
        """
        try:
            if formato == 'html':
                fig.write_html(ruta_salida)
            elif formato in ['png', 'jpg', 'jpeg']:
                fig.write_image(ruta_salida, format=formato)
            elif formato == 'pdf':
                fig.write_image(ruta_salida, format='pdf')
            elif formato == 'svg':
                fig.write_image(ruta_salida, format='svg')
            else:
                logger.warning(f"Formato no soportado: {formato}")
                return
            
            logger.info(f"Gráfico guardado en: {ruta_salida}")
            
        except Exception as e:
            logger.error(f"Error al guardar gráfico: {str(e)}")


def generar_todos_graficos(
    indicadores_list: List[Dict],
    analisis_list: List[Dict],
    directorio_salida: str
) -> Dict[str, str]:
    """
    Genera todos los gráficos del sistema y los guarda en el directorio especificado.
    
    Args:
        indicadores_list (List[Dict]): Lista de indicadores
        analisis_list (List[Dict]): Lista de análisis
        directorio_salida (str): Directorio donde guardar los gráficos
        
    Returns:
        Dict[str, str]: Diccionario con rutas de gráficos generados
    """
    import os
    
    generator = ChartGenerator()
    rutas = {}
    
    # Crear directorio si no existe
    os.makedirs(directorio_salida, exist_ok=True)
    
    logger.info(f"Generando gráficos en: {directorio_salida}")
    
    # 1. Gráfico de semaforización general
    fig_semaforo = generator.grafico_semaforizacion_general(analisis_list)
    if fig_semaforo:
        ruta = os.path.join(directorio_salida, 'semaforizacion_general.html')
        generator.guardar_grafico(fig_semaforo, ruta)
        rutas['semaforizacion_general'] = ruta
    
    # 2. Gráfico comparativo
    fig_comp = generator.grafico_comparativo_indicadores(indicadores_list, analisis_list, top_n=10)
    if fig_comp:
        ruta = os.path.join(directorio_salida, 'comparativo_indicadores.html')
        generator.guardar_grafico(fig_comp, ruta)
        rutas['comparativo'] = ruta
    
    # 3. Tendencias múltiples
    fig_tend = generator.grafico_tendencias_multiple(indicadores_list, max_indicadores=5)
    if fig_tend:
        ruta = os.path.join(directorio_salida, 'tendencias_multiples.html')
        generator.guardar_grafico(fig_tend, ruta)
        rutas['tendencias_multiples'] = ruta
    
    # 4. Estadísticas generales
    fig_stats = generator.grafico_estadisticas_generales(analisis_list, top_n=15)
    if fig_stats:
        ruta = os.path.join(directorio_salida, 'estadisticas_generales.html')
        generator.guardar_grafico(fig_stats, ruta)
        rutas['estadisticas'] = ruta
    
    logger.info(f"Se generaron {len(rutas)} gráficos")
    
    return rutas
