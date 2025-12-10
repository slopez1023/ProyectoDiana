"""
Módulo de generación de informes automáticos.

Genera reportes profesionales en formato PDF con:
- Resumen ejecutivo de indicadores
- Gráficos de tendencias y estadísticas
- Análisis automatizados
- Recomendaciones basadas en datos

Utiliza ReportLab para generación de PDFs estructurados.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.pdfgen import canvas
from datetime import datetime
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
import os

logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """
    Generador de reportes PDF para indicadores MIPG.
    
    Crea documentos profesionales siguiendo estándares de presentación
    para entidades públicas colombianas.
    """
    
    def __init__(self, output_path: str, page_size=letter):
        """
        Inicializa el generador de reportes.
        
        Args:
            output_path (str): Ruta donde guardar el PDF
            page_size: Tamaño de página (letter o A4)
        """
        self.output_path = output_path
        self.page_size = page_size
        self.width, self.height = page_size
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=page_size,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()
        
        logger.info(f"PDFReportGenerator inicializado: {output_path}")
    
    def _configurar_estilos(self):
        """Configura estilos personalizados para el documento."""
        
        # Estilo de título principal
        self.styles.add(ParagraphStyle(
            name='TituloCustom',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2E86AB'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo de subtítulo
        self.styles.add(ParagraphStyle(
            name='SubtituloCustom',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#555555'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Estilo de sección
        self.styles.add(ParagraphStyle(
            name='SeccionCustom',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2E86AB'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#2E86AB'),
            borderPadding=5,
            backColor=colors.HexColor('#E8F4F8')
        ))
        
        # Estilo de texto justificado
        self.styles.add(ParagraphStyle(
            name='JustificadoCustom',
            parent=self.styles['BodyText'],
            alignment=TA_JUSTIFY,
            fontSize=11,
            spaceAfter=10
        ))
    
    def agregar_portada(self, titulo: str, subtitulo: str, entidad: str, fecha: Optional[str] = None):
        """
        Agrega una portada al reporte.
        
        Args:
            titulo (str): Título principal
            subtitulo (str): Subtítulo
            entidad (str): Nombre de la entidad
            fecha (str, optional): Fecha del reporte
        """
        if fecha is None:
            fecha = datetime.now().strftime('%d de %B de %Y')
        
        # Espaciado superior
        self.story.append(Spacer(1, 2*inch))
        
        # Título principal
        titulo_p = Paragraph(titulo, self.styles['TituloCustom'])
        self.story.append(titulo_p)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Subtítulo
        subtitulo_p = Paragraph(subtitulo, self.styles['SubtituloCustom'])
        self.story.append(subtitulo_p)
        self.story.append(Spacer(1, 1.5*inch))
        
        # Información de la entidad
        entidad_p = Paragraph(f"<b>{entidad}</b>", self.styles['SubtituloCustom'])
        self.story.append(entidad_p)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Fecha
        fecha_p = Paragraph(fecha, self.styles['SubtituloCustom'])
        self.story.append(fecha_p)
        
        # Salto de página
        self.story.append(PageBreak())
    
    def agregar_seccion(self, titulo: str, contenido: str):
        """
        Agrega una sección con título y contenido.
        
        Args:
            titulo (str): Título de la sección
            contenido (str): Contenido en formato texto o HTML
        """
        titulo_p = Paragraph(titulo, self.styles['SeccionCustom'])
        self.story.append(titulo_p)
        
        contenido_p = Paragraph(contenido, self.styles['JustificadoCustom'])
        self.story.append(contenido_p)
        self.story.append(Spacer(1, 0.2*inch))
    
    def agregar_resumen_ejecutivo(self, analisis_list: List[Dict]):
        """
        Agrega un resumen ejecutivo con métricas principales.
        
        Args:
            analisis_list (List[Dict]): Lista de análisis de indicadores
        """
        self.agregar_seccion(
            "1. RESUMEN EJECUTIVO",
            "Este informe presenta el análisis integral de los indicadores institucionales bajo "
            "el marco del Modelo Integrado de Planeación y Gestión (MIPG). Se evaluaron los "
            "indicadores correspondientes al período vigente, analizando su comportamiento, "
            "tendencias y niveles de cumplimiento."
        )
        
        # Calcular métricas
        total = len(analisis_list)
        verdes = sum(1 for a in analisis_list if a.get('semaforo') == 'Verde')
        amarillos = sum(1 for a in analisis_list if a.get('semaforo') == 'Amarillo')
        rojos = sum(1 for a in analisis_list if a.get('semaforo') == 'Rojo')
        
        pct_verde = (verdes / total * 100) if total > 0 else 0
        pct_amarillo = (amarillos / total * 100) if total > 0 else 0
        pct_rojo = (rojos / total * 100) if total > 0 else 0
        
        # Tabla de resumen
        datos_tabla = [
            ['MÉTRICA', 'VALOR', 'PORCENTAJE'],
            ['Total de Indicadores Evaluados', str(total), '100%'],
            ['Indicadores en Estado Satisfactorio (Verde)', str(verdes), f'{pct_verde:.1f}%'],
            ['Indicadores en Estado Alerta (Amarillo)', str(amarillos), f'{pct_amarillo:.1f}%'],
            ['Indicadores en Estado Crítico (Rojo)', str(rojos), f'{pct_rojo:.1f}%']
        ]
        
        tabla = Table(datos_tabla, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        self.story.append(tabla)
        self.story.append(Spacer(1, 0.3*inch))
    
    def agregar_analisis_por_periodicidad(self, analisis_list: List[Dict]):
        """
        Agrega análisis de indicadores por periodicidad.
        
        Args:
            analisis_list (List[Dict]): Lista de análisis
        """
        self.agregar_seccion(
            "2. ANÁLISIS POR PERIODICIDAD",
            "Los indicadores se clasifican según su frecuencia de medición, lo que permite "
            "identificar patrones de seguimiento y control institucional."
        )
        
        # Contar por periodicidad
        periodicidades = {}
        for anal in analisis_list:
            per = anal.get('periodicidad', 'Indeterminada')
            periodicidades[per] = periodicidades.get(per, 0) + 1
        
        # Crear tabla
        datos_tabla = [['PERIODICIDAD', 'CANTIDAD', 'PORCENTAJE']]
        
        total = len(analisis_list)
        for per, cant in sorted(periodicidades.items(), key=lambda x: x[1], reverse=True):
            pct = (cant / total * 100) if total > 0 else 0
            datos_tabla.append([per, str(cant), f'{pct:.1f}%'])
        
        tabla = Table(datos_tabla, colWidths=[3*inch, 2*inch, 2*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        self.story.append(tabla)
        self.story.append(Spacer(1, 0.3*inch))
    
    def agregar_analisis_tendencias(self, analisis_list: List[Dict]):
        """
        Agrega análisis de tendencias de los indicadores.
        
        Args:
            analisis_list (List[Dict]): Lista de análisis
        """
        self.agregar_seccion(
            "3. ANÁLISIS DE TENDENCIAS",
            "El análisis de tendencias permite identificar el comportamiento de los indicadores "
            "a lo largo del tiempo, detectando patrones de crecimiento, estabilidad o retroceso."
        )
        
        # Contar por tendencia
        tendencias = {}
        for anal in analisis_list:
            tend = anal.get('tendencia', 'Insuficiente')
            tendencias[tend] = tendencias.get(tend, 0) + 1
        
        # Crear tabla
        datos_tabla = [['TENDENCIA', 'CANTIDAD', 'INTERPRETACIÓN']]
        
        interpretaciones = {
            'Crecimiento': 'Mejora sostenida en el indicador',
            'Estabilidad': 'Comportamiento constante',
            'Retroceso': 'Deterioro que requiere atención',
            'Volátil': 'Alta variabilidad',
            'Datos Insuficientes': 'Requiere más períodos de medición'
        }
        
        for tend, cant in sorted(tendencias.items(), key=lambda x: x[1], reverse=True):
            interp = interpretaciones.get(tend, 'N/A')
            datos_tabla.append([tend, str(cant), interp])
        
        tabla = Table(datos_tabla, colWidths=[2*inch, 1.5*inch, 3.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        self.story.append(tabla)
        self.story.append(Spacer(1, 0.3*inch))
    
    def agregar_indicadores_criticos(self, indicadores_list: List[Dict], analisis_list: List[Dict]):
        """
        Agrega sección de indicadores en estado crítico.
        
        Args:
            indicadores_list (List[Dict]): Lista de indicadores
            analisis_list (List[Dict]): Lista de análisis
        """
        # Filtrar indicadores críticos
        criticos = []
        for ind, anal in zip(indicadores_list, analisis_list):
            if anal.get('semaforo') == 'Rojo':
                criticos.append((ind, anal))
        
        if not criticos:
            self.agregar_seccion(
                "4. INDICADORES CRÍTICOS",
                "No se identificaron indicadores en estado crítico durante el período evaluado. "
                "Esto representa un desempeño satisfactorio general de la gestión institucional."
            )
            return
        
        self.agregar_seccion(
            "4. INDICADORES CRÍTICOS",
            f"Se identificaron {len(criticos)} indicador(es) en estado crítico que requieren "
            "atención inmediata y acciones correctivas por parte de las áreas responsables."
        )
        
        # Tabla de indicadores críticos
        datos_tabla = [['INDICADOR', 'PROMEDIO', 'META', 'BRECHA']]
        
        for ind, anal in criticos[:10]:  # Máximo 10
            nombre = ind.get('nombre', 'Sin nombre')[:50]
            stats = anal.get('estadisticas', {})
            promedio = stats.get('promedio', 0)
            meta = ind.get('meta', 0)
            brecha = meta - promedio if pd.notna(meta) and pd.notna(promedio) else 0
            
            datos_tabla.append([
                nombre,
                f"{promedio:.2f}%",
                f"{meta:.2f}%" if pd.notna(meta) else "N/A",
                f"{brecha:.2f}%"
            ])
        
        tabla = Table(datos_tabla, colWidths=[3.5*inch, 1.2*inch, 1.2*inch, 1.1*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc3545')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8d7da')])
        ]))
        
        self.story.append(tabla)
        self.story.append(Spacer(1, 0.3*inch))
    
    def agregar_recomendaciones(self, analisis_list: List[Dict]):
        """
        Agrega sección de recomendaciones automáticas.
        
        Args:
            analisis_list (List[Dict]): Lista de análisis
        """
        self.agregar_seccion(
            "5. RECOMENDACIONES",
            "Con base en el análisis realizado, se presentan las siguientes recomendaciones:"
        )
        
        # Generar recomendaciones basadas en datos
        recomendaciones = []
        
        # Contar estados
        rojos = sum(1 for a in analisis_list if a.get('semaforo') == 'Rojo')
        amarillos = sum(1 for a in analisis_list if a.get('semaforo') == 'Amarillo')
        retrocesos = sum(1 for a in analisis_list if a.get('tendencia') == 'Retroceso')
        
        if rojos > 0:
            recomendaciones.append(
                f"• <b>Atención prioritaria:</b> Se requiere implementar planes de acción "
                f"inmediatos para los {rojos} indicador(es) en estado crítico."
            )
        
        if amarillos > 0:
            recomendaciones.append(
                f"• <b>Seguimiento reforzado:</b> Establecer monitoreo continuo de los "
                f"{amarillos} indicador(es) en estado de alerta para prevenir deterioro."
            )
        
        if retrocesos > 0:
            recomendaciones.append(
                f"• <b>Análisis de causas:</b> Identificar factores que generan el retroceso "
                f"observado en {retrocesos} indicador(es) y definir acciones correctivas."
            )
        
        recomendaciones.append(
            "• <b>Actualización periódica:</b> Mantener la captura de datos actualizada "
            "para garantizar el seguimiento efectivo de los indicadores."
        )
        
        recomendaciones.append(
            "• <b>Socialización de resultados:</b> Compartir este análisis con las áreas "
            "responsables para promover la toma de decisiones basada en datos."
        )
        
        for rec in recomendaciones:
            rec_p = Paragraph(rec, self.styles['JustificadoCustom'])
            self.story.append(rec_p)
            self.story.append(Spacer(1, 0.1*inch))
    
    def generar_pdf(
        self,
        indicadores_list: List[Dict],
        analisis_list: List[Dict],
        titulo: str = "Informe de Indicadores MIPG",
        entidad: str = "Secretaría de Planeación"
    ):
        """
        Genera el documento PDF completo.
        
        Args:
            indicadores_list (List[Dict]): Lista de indicadores
            analisis_list (List[Dict]): Lista de análisis
            titulo (str): Título del informe
            entidad (str): Nombre de la entidad
        """
        try:
            logger.info("Iniciando generación de PDF...")
            
            # Portada
            self.agregar_portada(
                titulo=titulo,
                subtitulo="Análisis Institucional de Indicadores",
                entidad=entidad
            )
            
            # Contenido
            self.agregar_resumen_ejecutivo(analisis_list)
            self.agregar_analisis_por_periodicidad(analisis_list)
            self.agregar_analisis_tendencias(analisis_list)
            self.agregar_indicadores_criticos(indicadores_list, analisis_list)
            self.agregar_recomendaciones(analisis_list)
            
            # Construir PDF
            self.doc.build(self.story)
            
            logger.info(f"PDF generado exitosamente: {self.output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al generar PDF: {str(e)}")
            return False


def generar_informe_pdf(
    indicadores_list: List[Dict],
    analisis_list: List[Dict],
    output_path: str,
    titulo: Optional[str] = None,
    entidad: str = "Secretaría de Planeación"
) -> bool:
    """
    Función de conveniencia para generar un informe PDF completo.
    
    Args:
        indicadores_list (List[Dict]): Lista de indicadores
        analisis_list (List[Dict]): Lista de análisis
        output_path (str): Ruta de salida del PDF
        titulo (str, optional): Título personalizado
        entidad (str): Nombre de la entidad
        
    Returns:
        bool: True si se generó exitosamente, False en caso contrario
    """
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if titulo is None:
        titulo = f"Informe de Indicadores MIPG - {datetime.now().strftime('%B %Y')}"
    
    generator = PDFReportGenerator(output_path)
    return generator.generar_pdf(indicadores_list, analisis_list, titulo, entidad)
