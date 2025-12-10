"""
Dashboard Interactivo de Indicadores MIPG
Aplicación Streamlit para visualización y análisis de indicadores institucionales.

Funcionalidades:
- Navegación por indicadores
- Filtros por periodicidad, estado de semáforo y tendencia
- Visualizaciones interactivas
- Exportación de reportes
- Análisis automático de indicadores
"""

import streamlit as st
import pandas as pd
import sys
import os
import logging
from pathlib import Path

# Configurar logger
logger = logging.getLogger(__name__)

# Agregar directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_processing.excel_loader import load_and_process_excel
from data_processing.bateria_loader import load_and_process_bateria
from analysis.indicator_analyzer import analizar_todos_indicadores
from visualization.chart_generator import ChartGenerator
from reporting.report_generator import generar_informe_pdf

# Configuración de la página
st.set_page_config(
    page_title="Tablero de Control de Indicadores MIPG",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
    }
    .semaforo-verde {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 0.3rem;
        font-weight: bold;
    }
    .semaforo-amarillo {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 0.3rem;
        font-weight: bold;
    }
    .semaforo-rojo {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 0.3rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_datos(ruta_archivo):
    """
    Carga y procesa los datos del Excel (Tablero MIPG).
    Utiliza cache de Streamlit para evitar recargas innecesarias.
    """
    try:
        df, indicadores, resumen = load_and_process_excel(ruta_archivo)
        analisis = analizar_todos_indicadores(indicadores)
        return df, indicadores, analisis, resumen
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return None, None, None, None


@st.cache_data
def cargar_datos_bateria(ruta_archivo):
    """
    Carga y procesa los datos de la batería de indicadores sectoriales.
    Utiliza cache de Streamlit para evitar recargas innecesarias.
    """
    try:
        sectores_df, indicadores_por_sector, resumen = load_and_process_bateria(ruta_archivo)
        return sectores_df, indicadores_por_sector, resumen
    except Exception as e:
        st.error(f"Error al cargar la batería de indicadores: {str(e)}")
        return None, None, None


def analizar_indicadores_bateria(indicadores_list):
    """
    Analiza indicadores de la batería sectorial usando el analizador completo.
    Normaliza la estructura para que sea compatible con el análisis estándar.
    """
    from analysis.indicator_analyzer import IndicatorAnalyzer
    import numpy as np
    
    analyzer = IndicatorAnalyzer()
    analisis_list = []
    
    for indicador in indicadores_list:
        # Normalizar estructura del indicador para el analizador
        valores_mensuales = indicador.get('valores_mensuales', {})
        
        # Convertir nombre a string si es necesario
        nombre = indicador.get('nombre', 'Sin nombre')
        if not isinstance(nombre, str):
            nombre = str(nombre)
        
        # Crear estructura compatible
        indicador_normalizado = {
            'id': indicador['id'],
            'nombre': nombre,
            'meta': indicador.get('meta_cuatrienio', np.nan),
            'nivel_obtenido': indicador.get('meta_cuatrienio', np.nan),
            'nivel_satisfactorio': np.nan,
            'nivel_critico': np.nan,
            'valores_mensuales': valores_mensuales,
            'total_periodos': len(valores_mensuales),
            'promedio': indicador.get('promedio', np.nan)
        }
        
        try:
            # Usar el analizador completo
            analisis = analyzer.generar_analisis_completo(indicador_normalizado)
            # Agregar información del sector
            analisis['sector'] = indicador['sector']
            analisis['codigo_sector'] = indicador.get('codigo_sector', '')
            analisis['nombre_sector'] = indicador.get('nombre_sector', '')
            analisis['objetivo'] = indicador.get('objetivo', '')
            analisis['unidad_medida'] = indicador.get('unidad_medida', '')
        except Exception as e:
            logger.error(f"Error al analizar indicador {nombre}: {e}")
            # Fallback a análisis básico
            analisis = {
                'id': indicador['id'],
                'nombre': nombre,
                'sector': indicador['sector'],
                'periodicidad': 'Anual',
                'semaforo': 'Gris',
                'tendencia': 'Estable',
                'promedio': indicador.get('promedio', 0),
                'estadisticas': {
                    'promedio': indicador.get('promedio', 0),
                    'minimo': 0,
                    'maximo': 0
                },
                'interpretacion': f"Indicador del sector {indicador['sector']}: {nombre}",
                'anomalias': []
            }
        
        analisis_list.append(analisis)
    
    return analisis_list


def mostrar_header():
    """Muestra el encabezado principal del dashboard."""
    st.markdown('<div class="main-header">📊 Alcaldía de Filandia</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Tablero de Control de Indicadores MIPG - Sistema de Gestión de Indicadores Institucionales</div>', unsafe_allow_html=True)
    st.markdown("---")


def mostrar_metricas_generales(analisis_list):
    """Muestra métricas generales en tarjetas."""
    col1, col2, col3, col4 = st.columns(4)
    
    total_indicadores = len(analisis_list)
    
    # Contar por semáforo
    verdes = sum(1 for a in analisis_list if a.get('semaforo') == 'Verde')
    amarillos = sum(1 for a in analisis_list if a.get('semaforo') == 'Amarillo')
    rojos = sum(1 for a in analisis_list if a.get('semaforo') == 'Rojo')
    
    # Calcular porcentajes
    pct_verde = (verdes / total_indicadores * 100) if total_indicadores > 0 else 0
    
    with col1:
        st.metric("Total Indicadores", total_indicadores)
    
    with col2:
        st.metric("✅ Estado Satisfactorio", f"{verdes} ({pct_verde:.1f}%)")
    
    with col3:
        st.metric("⚠️ Estado Alerta", amarillos)
    
    with col4:
        st.metric("❌ Estado Crítico", rojos)


def filtrar_indicadores(analisis_list, periodicidad, semaforo, tendencia, busqueda):
    """
    Aplica filtros a la lista de análisis de indicadores.
    """
    resultados = analisis_list.copy()
    
    # Filtro por periodicidad
    if periodicidad != "Todas":
        resultados = [a for a in resultados if a.get('periodicidad') == periodicidad]
    
    # Filtro por semáforo
    if semaforo != "Todos":
        resultados = [a for a in resultados if a.get('semaforo') == semaforo]
    
    # Filtro por tendencia
    if tendencia != "Todas":
        resultados = [a for a in resultados if a.get('tendencia') == tendencia]
    
    # Filtro por búsqueda de texto
    if busqueda:
        resultados = [a for a in resultados if busqueda.lower() in a.get('nombre', '').lower()]
    
    return resultados


def mostrar_detalle_indicador(indicador, analisis):
    """Muestra el detalle completo de un indicador individual."""
    st.subheader(f"📈 {indicador['nombre']}")
    
    # Información general
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Periodicidad:**")
        st.write(analisis['periodicidad'])
        st.markdown("**Meta:**")
        st.write(f"{indicador.get('meta', 'N/A')}%")
    
    with col2:
        st.markdown("**Tendencia:**")
        st.write(analisis['tendencia'])
        st.markdown("**Promedio:**")
        estadisticas = analisis.get('estadisticas', {})
        st.write(f"{estadisticas.get('promedio', 0):.2f}%")
    
    with col3:
        st.markdown("**Estado Semáforo:**")
        semaforo = analisis['semaforo']
        if semaforo == 'Verde':
            st.markdown('<div class="semaforo-verde">✅ SATISFACTORIO</div>', unsafe_allow_html=True)
        elif semaforo == 'Amarillo':
            st.markdown('<div class="semaforo-amarillo">⚠️ ALERTA</div>', unsafe_allow_html=True)
        elif semaforo == 'Rojo':
            st.markdown('<div class="semaforo-rojo">❌ CRÍTICO</div>', unsafe_allow_html=True)
        else:
            st.write("⚪ Sin datos")
    
    st.markdown("---")
    
    # Gráfico de tendencia
    generator = ChartGenerator()
    fig = generator.grafico_tendencia_indicador(indicador, analisis, mostrar_meta=True)
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Interpretación automática
    st.markdown("### 📝 Interpretación Automática")
    st.info(analisis.get('interpretacion', 'No disponible'))
    
    # Estadísticas detalladas
    with st.expander("📊 Ver Estadísticas Detalladas"):
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            st.metric("Mínimo", f"{estadisticas.get('minimo', 0):.2f}%")
            st.metric("Máximo", f"{estadisticas.get('maximo', 0):.2f}%")
            st.metric("Mediana", f"{estadisticas.get('mediana', 0):.2f}%")
        
        with stats_col2:
            st.metric("Desviación Estándar", f"{estadisticas.get('desviacion_estandar', 0):.2f}")
            st.metric("Rango", f"{estadisticas.get('rango', 0):.2f}")
            st.metric("Coef. Variación", f"{estadisticas.get('coeficiente_variacion', 0):.2f}%")
    
    # Anomalías detectadas
    anomalias = analisis.get('anomalias', [])
    if anomalias:
        with st.expander(f"⚠️ Anomalías Detectadas ({len(anomalias)})"):
            df_anomalias = pd.DataFrame(anomalias)
            st.dataframe(df_anomalias, use_container_width=True)
    
    # Valores mensuales
    with st.expander("📅 Ver Valores por Período"):
        valores = indicador.get('valores_mensuales', {})
        if valores:
            df_valores = pd.DataFrame([
                {'Período': mes, 'Valor': f"{valor:.2f}%"}
                for mes, valor in valores.items()
            ])
            st.dataframe(df_valores, use_container_width=True)


def pagina_inicio(df, indicadores_list, analisis_list):
    """Página principal del dashboard."""
    mostrar_header()
    
    # Métricas generales
    mostrar_metricas_generales(analisis_list)
    
    st.markdown("---")
    
    # Gráficos generales
    st.subheader("📊 Visualizaciones Generales")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Semaforización", "📈 Comparativo", "📉 Tendencias"])
    
    generator = ChartGenerator()
    
    with tab1:
        fig_semaforo = generator.grafico_semaforizacion_general(analisis_list)
        if fig_semaforo:
            st.plotly_chart(fig_semaforo, use_container_width=True)
    
    with tab2:
        fig_comparativo = generator.grafico_comparativo_indicadores(indicadores_list, analisis_list, top_n=10)
        if fig_comparativo:
            st.plotly_chart(fig_comparativo, use_container_width=True)
    
    with tab3:
        fig_tendencias = generator.grafico_tendencias_multiple(indicadores_list, max_indicadores=5)
        if fig_tendencias:
            st.plotly_chart(fig_tendencias, use_container_width=True)


def pagina_indicadores(indicadores_list, analisis_list):
    """Página de exploración de indicadores individuales."""
    st.title("🔍 Explorar Indicadores")
    
    # Sidebar con filtros
    st.sidebar.markdown("## 🔧 Filtros")
    
    # Verificar si hay indicadores con sectores (batería sectorial)
    tiene_sectores = any('sector' in ind for ind in indicadores_list)
    
    # Filtro por sector (solo para batería sectorial)
    filtro_sector = "Todos"
    if tiene_sectores:
        sectores = sorted(list(set([ind.get('sector', 'Sin sector') for ind in indicadores_list])))
        filtro_sector = st.sidebar.selectbox("Sector", ["Todos"] + sectores)
    
    # Obtener opciones únicas
    periodicidades = sorted(list(set([a.get('periodicidad', 'Indeterminada') for a in analisis_list])))
    semaforos = ['Todos', 'Verde', 'Amarillo', 'Rojo', 'Gris']
    tendencias = sorted(list(set([a.get('tendencia', 'Insuficiente') for a in analisis_list])))
    
    # Filtros
    filtro_periodicidad = st.sidebar.selectbox("Periodicidad", ["Todas"] + periodicidades)
    filtro_semaforo = st.sidebar.selectbox("Estado Semáforo", semaforos)
    filtro_tendencia = st.sidebar.selectbox("Tendencia", ["Todas"] + tendencias)
    filtro_busqueda = st.sidebar.text_input("🔍 Buscar indicador", "")
    
    # Aplicar filtros
    analisis_filtrados = filtrar_indicadores(
        analisis_list,
        filtro_periodicidad,
        filtro_semaforo,
        filtro_tendencia,
        filtro_busqueda
    )
    
    # Aplicar filtro de sector si aplica
    if filtro_sector != "Todos":
        analisis_filtrados = [a for a in analisis_filtrados if a.get('sector', '') == filtro_sector]
    
    indicadores_filtrados_idx = []
    
    # Obtener indicadores correspondientes
    indicadores_filtrados = []
    for anal in analisis_filtrados:
        idx = anal.get('indicador_id')
        for ind in indicadores_list:
            if ind.get('id') == idx:
                indicadores_filtrados.append(ind)
                break
    
    st.info(f"📋 Se encontraron **{len(indicadores_filtrados)}** indicadores que cumplen los criterios")
    
    # Lista de indicadores
    if indicadores_filtrados:
        nombres_indicadores = [ind['nombre'] for ind in indicadores_filtrados]
        indicador_seleccionado = st.selectbox(
            "Seleccione un indicador para ver detalles:",
            nombres_indicadores
        )
        
        # Encontrar el indicador y su análisis
        for ind, anal in zip(indicadores_filtrados, analisis_filtrados):
            if ind['nombre'] == indicador_seleccionado:
                st.markdown("---")
                mostrar_detalle_indicador(ind, anal)
                break
    else:
        st.warning("No se encontraron indicadores con los filtros aplicados")


def pagina_reportes(indicadores_list, analisis_list):
    """Página de generación de reportes."""
    st.title("📄 Generar Reportes")
    
    st.markdown("""
    Esta sección permite generar reportes automáticos en formato PDF con:
    - Resumen ejecutivo de indicadores
    - Gráficos de tendencias
    - Análisis estadísticos
    - Recomendaciones automáticas
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Opciones del Reporte")
        
        incluir_graficos = st.checkbox("Incluir gráficos", value=True)
        incluir_estadisticas = st.checkbox("Incluir estadísticas detalladas", value=True)
        incluir_anomalias = st.checkbox("Incluir análisis de anomalías", value=True)
        
        nombre_archivo = st.text_input("Nombre del archivo", "Informe_Indicadores_MIPG")
    
    with col2:
        st.subheader("Filtros del Reporte")
        
        semaforo_reporte = st.multiselect(
            "Estados de semáforo a incluir",
            ['Verde', 'Amarillo', 'Rojo', 'Gris'],
            default=['Verde', 'Amarillo', 'Rojo']
        )
        
        top_n_indicadores = st.slider("Número máximo de indicadores", 5, len(indicadores_list), 20)
    
    if st.button("🎯 Generar Reporte PDF", type="primary"):
        with st.spinner("Generando reporte..."):
            try:
                # Filtrar indicadores según criterios
                indicadores_reporte = []
                analisis_reporte = []
                
                for ind, anal in zip(indicadores_list, analisis_list):
                    if anal.get('semaforo') in semaforo_reporte:
                        indicadores_reporte.append(ind)
                        analisis_reporte.append(anal)
                
                # Limitar cantidad
                indicadores_reporte = indicadores_reporte[:top_n_indicadores]
                analisis_reporte = analisis_reporte[:top_n_indicadores]
                
                # Generar PDF en memoria
                from datetime import datetime
                pdf_buffer = generar_informe_pdf(
                    indicadores_reporte,
                    analisis_reporte,
                    titulo="Informe de Indicadores MIPG - Alcaldía de Filandia",
                    incluir_graficos=incluir_graficos,
                    incluir_estadisticas=incluir_estadisticas
                )
                
                # Crear nombre de archivo con fecha
                fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_descarga = f"{nombre_archivo}_{fecha_actual}.pdf"
                
                # Botón de descarga
                st.download_button(
                    label="📥 Descargar Reporte PDF",
                    data=pdf_buffer,
                    file_name=nombre_descarga,
                    mime="application/pdf",
                    type="primary"
                )
                
                st.success(f"✅ Reporte generado exitosamente")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error al generar reporte: {str(e)}")


def main():
    """Función principal del dashboard."""
    
    # Obtener la ruta absoluta al directorio raíz del proyecto
    directorio_raiz = Path(__file__).parent.parent
    
    # Definir archivos disponibles
    archivos_disponibles = {
        "Tablero MIPG 2025": directorio_raiz / "RE-SM-01 Tablero de Control de Indicadores 2025.xls",
        "Batería Indicadores Sectoriales": directorio_raiz / "63721_bateria-indicadores-sectoriales.xlsx"
    }
    
    # Selector de archivo en el sidebar (al inicio)
    st.sidebar.title("📂 Selección de Datos")
    archivo_seleccionado = st.sidebar.radio(
        "Seleccione el conjunto de datos:",
        list(archivos_disponibles.keys())
    )
    
    archivo_path = archivos_disponibles[archivo_seleccionado]
    
    # Verificar que existe
    if not archivo_path.exists():
        st.error(f"❌ No se encontró el archivo: {archivo_path.name}")
        st.info("Por favor, asegúrese de que el archivo Excel esté en el directorio raíz del proyecto.")
        return
    
    # Convertir a string
    archivo_excel = str(archivo_path)
    
    # Cargar datos según el tipo de archivo
    with st.spinner(f"Cargando {archivo_seleccionado}..."):
        if "Batería" in archivo_seleccionado:
            # Cargar batería de indicadores sectoriales
            sectores_df, indicadores_por_sector, resumen_bateria = cargar_datos_bateria(archivo_excel)
            
            if not sectores_df:
                st.error("No se pudieron cargar los datos de la batería")
                return
            
            # Convertir a formato compatible
            indicadores_list = []
            for sector, inds in indicadores_por_sector.items():
                indicadores_list.extend(inds)
            
            analisis_list = analizar_indicadores_bateria(indicadores_list)
            df = pd.DataFrame(indicadores_list)
            resumen = resumen_bateria
        else:
            # Cargar tablero MIPG
            df, indicadores_list, analisis_list, resumen = cargar_datos(archivo_excel)
    
    if df is None or indicadores_list is None:
        st.error("No se pudieron cargar los datos correctamente")
        return
    
    # Menú de navegación
    st.sidebar.title("🧭 Navegación")
    pagina = st.sidebar.radio(
        "Ir a:",
        ["🏠 Inicio", "🔍 Explorar Indicadores", "📄 Generar Reportes", "ℹ️ Acerca de"]
    )
    
    # Información en sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Información del Sistema")
    
    info_texto = f"**Total Indicadores:** {len(indicadores_list)}  \n"
    info_texto += f"**Última Actualización:** {resumen['metadata']['load_timestamp'].strftime('%Y-%m-%d %H:%M')}"
    
    if "Batería" in archivo_seleccionado:
        info_texto += f"\n\n**Sectores:** {resumen.get('total_sectores', 0)}"
    
    st.sidebar.info(info_texto)
    
    # Mostrar página seleccionada
    if pagina == "🏠 Inicio":
        pagina_inicio(df, indicadores_list, analisis_list)
    elif pagina == "🔍 Explorar Indicadores":
        pagina_indicadores(indicadores_list, analisis_list)
    elif pagina == "📄 Generar Reportes":
        pagina_reportes(indicadores_list, analisis_list)
    elif pagina == "ℹ️ Acerca de":
        st.title("ℹ️ Acerca del Sistema")
        st.markdown("""
        ## Sistema de Tablero de Control de Indicadores MIPG
        
        ### Secretaría de Planeación
        **Entidad Territorial - Sexta Categoría**
        
        ---
        
        ### Descripción
        
        Este sistema permite el análisis automatizado de indicadores institucionales bajo los lineamientos
        del Modelo Integrado de Planeación y Gestión (MIPG).
        
        ### Funcionalidades Principales
        
        - ✅ **Importación automática** de datos desde Excel
        - 📊 **Clasificación inteligente** de periodicidad de indicadores
        - 🎯 **Semaforización** según criterios de cumplimiento
        - 📈 **Análisis de tendencias** (crecimiento, estabilidad, retroceso)
        - ⚠️ **Detección de anomalías** estadísticas
        - 📄 **Generación automática** de reportes e informes
        - 🔍 **Exploración interactiva** con filtros avanzados
        
        ### Tecnologías Utilizadas
        
        - **Python 3.12** - Lenguaje de programación
        - **Streamlit** - Framework de visualización
        - **Pandas** - Procesamiento de datos
        - **Plotly** - Gráficos interactivos
        - **ReportLab** - Generación de PDFs
        
        ### Versión
        
        **v1.0.0** - Diciembre 2025
        
        ---
        
        ### Soporte
        
        Para soporte técnico o reportar problemas, contacte a la Secretaría de Planeación.
        """)


if __name__ == "__main__":
    main()
