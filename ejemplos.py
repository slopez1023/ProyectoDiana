"""
Script de ejemplo de uso del sistema.

Demuestra las principales funcionalidades del sistema de indicadores MIPG.
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_processing.excel_loader import load_and_process_excel
from analysis.indicator_analyzer import analizar_todos_indicadores, IndicatorAnalyzer
from visualization.chart_generator import ChartGenerator
from utils.helpers import format_percentage


def ejemplo_basico():
    """Ejemplo básico de carga y análisis."""
    print("=" * 80)
    print("EJEMPLO BÁSICO: Carga y Análisis de Indicadores")
    print("=" * 80)
    
    # 1. Cargar datos
    print("\n1. Cargando datos del Excel...")
    archivo = "RE-SM-01 Tablero de Control de Indicadores 2025.xls"
    df, indicadores, resumen = load_and_process_excel(archivo)
    
    print(f"   ✓ Indicadores cargados: {len(indicadores)}")
    print(f"   ✓ Dimensiones: {df.shape}")
    
    # 2. Analizar
    print("\n2. Analizando indicadores...")
    analisis = analizar_todos_indicadores(indicadores)
    
    print(f"   ✓ Análisis completados: {len(analisis)}")
    
    # 3. Mostrar resumen
    print("\n3. Resumen de Estados:")
    verdes = sum(1 for a in analisis if a.get('semaforo') == 'Verde')
    amarillos = sum(1 for a in analisis if a.get('semaforo') == 'Amarillo')
    rojos = sum(1 for a in analisis if a.get('semaforo') == 'Rojo')
    
    print(f"   🟢 Verde (Satisfactorio): {verdes}")
    print(f"   🟡 Amarillo (Alerta): {amarillos}")
    print(f"   🔴 Rojo (Crítico): {rojos}")
    
    return indicadores, analisis


def ejemplo_indicador_especifico(indicadores, analisis):
    """Ejemplo de análisis de un indicador específico."""
    print("\n" + "=" * 80)
    print("EJEMPLO: Análisis de Indicador Específico")
    print("=" * 80)
    
    # Tomar primer indicador como ejemplo
    indicador = indicadores[0]
    anal = analisis[0]
    
    print(f"\n📊 Indicador: {indicador['nombre']}")
    print(f"   Meta: {format_percentage(indicador.get('meta'))}")
    print(f"\n📈 Análisis:")
    print(f"   Periodicidad: {anal['periodicidad']}")
    print(f"   Tendencia: {anal['tendencia']}")
    print(f"   Semáforo: {anal['semaforo']}")
    
    stats = anal['estadisticas']
    print(f"\n📊 Estadísticas:")
    print(f"   Promedio: {format_percentage(stats['promedio'])}")
    print(f"   Mínimo: {format_percentage(stats['minimo'])}")
    print(f"   Máximo: {format_percentage(stats['maximo'])}")
    print(f"   Desviación Estándar: {stats['desviacion_estandar']:.2f}")
    
    if anal['anomalias']:
        print(f"\n⚠️ Anomalías detectadas: {len(anal['anomalias'])}")
        for anom in anal['anomalias'][:3]:  # Mostrar máximo 3
            print(f"   - {anom['mes']}: {anom['valor']:.2f}% (Z-score: {anom['z_score']:.2f})")
    
    print(f"\n💬 Interpretación:")
    print(f"   {anal['interpretacion']}")


def ejemplo_filtrado(indicadores, analisis):
    """Ejemplo de filtrado de indicadores."""
    print("\n" + "=" * 80)
    print("EJEMPLO: Filtrado de Indicadores")
    print("=" * 80)
    
    # Filtrar indicadores críticos
    print("\n🔴 Indicadores en Estado Crítico:")
    criticos = [(ind, anal) for ind, anal in zip(indicadores, analisis) 
                if anal['semaforo'] == 'Rojo']
    
    if criticos:
        for ind, anal in criticos[:5]:  # Mostrar máximo 5
            print(f"   - {ind['nombre']}")
            print(f"     Promedio: {format_percentage(anal['estadisticas']['promedio'])}")
            print(f"     Meta: {format_percentage(ind.get('meta'))}")
    else:
        print("   ✓ No hay indicadores en estado crítico")
    
    # Filtrar por tendencia
    print("\n📉 Indicadores en Retroceso:")
    retrocesos = [(ind, anal) for ind, anal in zip(indicadores, analisis) 
                  if anal['tendencia'] == 'Retroceso']
    
    if retrocesos:
        for ind, anal in retrocesos[:5]:
            print(f"   - {ind['nombre']}")
            print(f"     Pendiente: {anal['pendiente']:.2f}")
    else:
        print("   ✓ No hay indicadores en retroceso")


def ejemplo_generacion_grafico(indicadores, analisis):
    """Ejemplo de generación de gráfico."""
    print("\n" + "=" * 80)
    print("EJEMPLO: Generación de Gráficos")
    print("=" * 80)
    
    generator = ChartGenerator()
    
    print("\n1. Generando gráfico de tendencia individual...")
    fig = generator.grafico_tendencia_indicador(indicadores[0], analisis[0])
    
    # Guardar
    ruta_salida = "output/charts/ejemplo_tendencia.html"
    generator.guardar_grafico(fig, ruta_salida)
    print(f"   ✓ Gráfico guardado en: {ruta_salida}")
    
    print("\n2. Generando gráfico comparativo...")
    fig_comp = generator.grafico_comparativo_indicadores(
        indicadores[:10], 
        analisis[:10], 
        top_n=10
    )
    
    ruta_comp = "output/charts/ejemplo_comparativo.html"
    generator.guardar_grafico(fig_comp, ruta_comp)
    print(f"   ✓ Gráfico guardado en: {ruta_comp}")
    
    print("\n3. Generando gráfico de semaforización...")
    fig_sem = generator.grafico_semaforizacion_general(analisis)
    
    ruta_sem = "output/charts/ejemplo_semaforo.html"
    generator.guardar_grafico(fig_sem, ruta_sem)
    print(f"   ✓ Gráfico guardado en: {ruta_sem}")


def ejemplo_analisis_personalizado():
    """Ejemplo de análisis personalizado."""
    print("\n" + "=" * 80)
    print("EJEMPLO: Análisis Personalizado")
    print("=" * 80)
    
    analyzer = IndicatorAnalyzer()
    
    # Datos de ejemplo
    valores = {
        'Enero': 85.5,
        'Febrero': 87.2,
        'Marzo': 86.8,
        'Abril': 88.1,
        'Mayo': 89.5,
        'Junio': 88.7
    }
    
    print("\n📊 Valores de ejemplo:")
    for mes, val in valores.items():
        print(f"   {mes}: {val:.2f}%")
    
    # Clasificar periodicidad
    print("\n1. Clasificando periodicidad...")
    periodicidad = analyzer.clasificar_periodicidad(valores)
    print(f"   ✓ Periodicidad: {periodicidad.value}")
    
    # Analizar tendencia
    print("\n2. Analizando tendencia...")
    tendencia, pendiente = analyzer.analizar_tendencia(valores)
    print(f"   ✓ Tendencia: {tendencia.value}")
    print(f"   ✓ Pendiente: {pendiente:.2f}")
    
    # Calcular estadísticas
    print("\n3. Calculando estadísticas...")
    stats = analyzer.calcular_estadisticas(valores)
    print(f"   ✓ Promedio: {stats['promedio']:.2f}%")
    print(f"   ✓ Desviación: {stats['desviacion_estandar']:.2f}")
    print(f"   ✓ Coef. Variación: {stats['coeficiente_variacion']:.2f}%")
    
    # Calcular semáforo
    print("\n4. Calculando semáforo...")
    semaforo = analyzer.calcular_semaforo(
        valor_actual=88.7,
        meta=90.0,
        nivel_satisfactorio=90.0,
        nivel_critico=80.0
    )
    print(f"   ✓ Estado: {semaforo.value}")


def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "EJEMPLOS DE USO DEL SISTEMA" + " " * 31 + "║")
    print("║" + " " * 15 + "Tablero de Control de Indicadores MIPG" + " " * 25 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        # Ejemplo 1: Básico
        indicadores, analisis = ejemplo_basico()
        
        # Ejemplo 2: Indicador específico
        ejemplo_indicador_especifico(indicadores, analisis)
        
        # Ejemplo 3: Filtrado
        ejemplo_filtrado(indicadores, analisis)
        
        # Ejemplo 4: Generación de gráficos
        ejemplo_generacion_grafico(indicadores, analisis)
        
        # Ejemplo 5: Análisis personalizado
        ejemplo_analisis_personalizado()
        
        print("\n" + "=" * 80)
        print("✅ EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("=" * 80)
        print("\nRevise los archivos generados en:")
        print("  - output/charts/ejemplo_*.html")
        print("\nPara ver el dashboard interactivo, ejecute:")
        print("  streamlit run src/dashboard.py")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución de ejemplos: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
