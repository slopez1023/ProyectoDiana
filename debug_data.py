"""
Script de diagnóstico para verificar la carga de datos del Excel
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_processing.excel_loader import load_and_process_excel

# Ruta al archivo Excel
archivo_excel = r"C:\Users\santi\TableroIndicadores\RE-SM-01 Tablero de Control de Indicadores 2025.xls"

print(f"Cargando archivo: {archivo_excel}")
print("=" * 80)

try:
    # Cargar datos
    df, indicadores, resumen = load_and_process_excel(archivo_excel)
    
    print(f"\n✅ Archivo cargado exitosamente")
    print(f"\nDimensiones del DataFrame: {df.shape}")
    print(f"Total de indicadores: {len(indicadores)}")
    
    print("\n" + "=" * 80)
    print("COLUMNAS DETECTADAS:")
    print("=" * 80)
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")
    
    print("\n" + "=" * 80)
    print("PRIMEROS 3 INDICADORES:")
    print("=" * 80)
    for i, ind in enumerate(indicadores[:3], 1):
        print(f"\nIndicador {i}:")
        print(f"  Nombre: {ind['nombre']}")
        print(f"  Meta: {ind['meta']}")
        print(f"  Nivel Obtenido: {ind['nivel_obtenido']}")
        print(f"  Nivel Satisfactorio: {ind['nivel_satisfactorio']}")
        print(f"  Nivel Crítico: {ind['nivel_critico']}")
        print(f"  Valores mensuales: {len(ind['valores_mensuales'])} meses con datos")
        if ind['valores_mensuales']:
            print(f"  Ejemplo valores: {dict(list(ind['valores_mensuales'].items())[:3])}")
    
    print("\n" + "=" * 80)
    print("RESUMEN DE METADATOS:")
    print("=" * 80)
    print(f"Total indicadores: {resumen['metadata']['total_indicators']}")
    print(f"Indicadores válidos: {resumen['metadata']['valid_indicators']}")
    print(f"Indicadores inválidos: {resumen['metadata']['invalid_indicators']}")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
