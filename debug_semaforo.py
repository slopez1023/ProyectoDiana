"""
Script para diagnosticar el problema de semaforización
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_processing.excel_loader import load_and_process_excel
from analysis.indicator_analyzer import analizar_todos_indicadores

archivo_excel = r"C:\Users\santi\TableroIndicadores\RE-SM-01 Tablero de Control de Indicadores 2025.xls"

print("Cargando y analizando indicadores...")
print("=" * 80)

df, indicadores, resumen = load_and_process_excel(archivo_excel)
analisis_list = analizar_todos_indicadores(indicadores)

print(f"\nTotal de indicadores: {len(indicadores)}")
print("\n" + "=" * 80)
print("ANÁLISIS DE SEMAFORIZACIÓN:")
print("=" * 80)

# Contar por color
conteo = {'Verde': 0, 'Amarillo': 0, 'Rojo': 0, 'Gris': 0}
for anal in analisis_list:
    conteo[anal['semaforo']] += 1

print(f"\nDistribución de semáforos:")
for color, cantidad in conteo.items():
    porcentaje = (cantidad / len(analisis_list) * 100) if analisis_list else 0
    print(f"  {color}: {cantidad} ({porcentaje:.1f}%)")

print("\n" + "=" * 80)
print("DETALLES DE PRIMEROS 5 INDICADORES:")
print("=" * 80)

for i in range(min(5, len(indicadores))):
    ind = indicadores[i]
    anal = analisis_list[i]
    
    print(f"\n{i+1}. {ind['nombre'][:60]}")
    print(f"   Meta: {ind.get('meta', 'N/A')}")
    print(f"   Nivel Obtenido: {ind.get('nivel_obtenido', 'N/A')}")
    print(f"   Nivel Satisfactorio: {ind.get('nivel_satisfactorio', 'N/A')}")
    print(f"   Nivel Crítico: {ind.get('nivel_critico', 'N/A')}")
    print(f"   Promedio valores: {ind.get('promedio', 'N/A')}")
    print(f"   Valores mensuales: {len(ind.get('valores_mensuales', {}))}")
    
    # Último valor
    valores_mensuales = ind.get('valores_mensuales', {})
    ultimo_valor = None
    if valores_mensuales:
        meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        for mes in reversed(meses_orden):
            if mes in valores_mensuales:
                ultimo_valor = valores_mensuales[mes]
                print(f"   Último valor ({mes}): {ultimo_valor}")
                break
    
    print(f"   → SEMÁFORO: {anal['semaforo']}")
