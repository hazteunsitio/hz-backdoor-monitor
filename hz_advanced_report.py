#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HZ Advanced Report Generator
Generador de reportes HTML avanzado con filtros y búsqueda
echo por hazteunsitio.net
"""

import json
import html
from datetime import datetime

def generar_reporte_avanzado(resultados_escaneo, estadisticas, archivo_salida='hz-backdoor-reporte-avanzado.html'):
    """Genera un reporte HTML avanzado con filtros, búsqueda y código completo"""
    
    # Calcular estadísticas
    if estadisticas.get('tiempo_inicio'):
        tiempo_transcurrido = datetime.now() - estadisticas['tiempo_inicio']
        tiempo_escaneo = str(tiempo_transcurrido).split('.')[0]
    else:
        tiempo_escaneo = "N/A"
    
    total_archivos = estadisticas['archivos_escaneados']
    total_detecciones = len(resultados_escaneo)
    archivos_infectados = len(estadisticas['archivos_con_detecciones'])
    fecha_escaneo = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    # Agrupar detecciones por archivo para evitar duplicados
    detecciones_agrupadas = {}
    for deteccion in resultados_escaneo:
        archivo = deteccion['archivo']
        if archivo not in detecciones_agrupadas:
            detecciones_agrupadas[archivo] = {
                'archivo': archivo,
                'detecciones': [],
                'nivel_riesgo_max': 'INFO',
                'categorias': set()
            }
        
        detecciones_agrupadas[archivo]['detecciones'].append(deteccion)
        detecciones_agrupadas[archivo]['categorias'].add(deteccion['categoria'])
        
        # Determinar el nivel de riesgo más alto
        orden_riesgo = {'CRITICO': 5, 'ALTO': 4, 'MEDIO': 3, 'BAJO': 2, 'INFO': 1}
        if orden_riesgo.get(deteccion['nivel_riesgo'], 0) > orden_riesgo.get(detecciones_agrupadas[archivo]['nivel_riesgo_max'], 0):
            detecciones_agrupadas[archivo]['nivel_riesgo_max'] = deteccion['nivel_riesgo']
    
    # Preparar datos para JavaScript
    detecciones_json = json.dumps(resultados_escaneo, ensure_ascii=False, indent=2)
    
    # Contar por niveles de riesgo
    niveles_riesgo = {}
    categorias = {}
    for deteccion in resultados_escaneo:
        nivel = deteccion['nivel_riesgo']
        categoria = deteccion['categoria']
        niveles_riesgo[nivel] = niveles_riesgo.get(nivel, 0) + 1
        categorias[categoria] = categorias.get(categoria, 0) + 1
    
    html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HZ Backdoor Checker v3.0 - Reporte Avanzado de Seguridad</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
            --critical-color: #8e44ad;
            --info-color: #17a2b8;
            --dark-bg: #1a1a1a;
            --light-bg: #f8f9fa;
            --card-shadow: 0 10px 30px rgba(0,0,0,0.1);
            --border-radius: 12px;
            --transition: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--card-shadow);
            overflow: hidden;
            animation: fadeInUp 0.6s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary-color) 0%, #34495e 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        }
        
        .header .subtitle {
            font-size: 1.3em;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }
        
        .version-badge {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--accent-color);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        
        .stats-section {
            background: var(--light-bg);
            padding: 40px 30px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .risk-stats, .category-stats {
            margin-top: 30px;
            background: white;
            padding: 25px;
            border-radius: var(--border-radius);
            box-shadow: var(--card-shadow);
        }
        
        .risk-stats h3, .category-stats h3 {
            color: var(--primary-color);
            margin-bottom: 20px;
            font-size: 1.3em;
        }
        
        .risk-grid, .category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .risk-stat, .category-stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 15px;
            background: var(--light-bg);
            border-radius: 8px;
            transition: var(--transition);
        }
        
        .risk-stat:hover, .category-stat:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .risk-count, .category-count {
            font-weight: bold;
            font-size: 1.2em;
            color: var(--primary-color);
        }
        
        .category-name {
            font-weight: 600;
            color: var(--primary-color);
        }
        
        .stat-card {
            background: white;
            padding: 30px 25px;
            border-radius: var(--border-radius);
            text-align: center;
            box-shadow: var(--card-shadow);
            transition: var(--transition);
            border-left: 5px solid var(--secondary-color);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        
        .stat-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
            color: var(--secondary-color);
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 10px;
        }
        
        .stat-label {
            font-size: 1.1em;
            color: #666;
            font-weight: 500;
        }
        
        .controls-section {
            background: white;
            padding: 30px;
            border-bottom: 1px solid #eee;
        }
        
        .controls-grid {
            display: grid;
            grid-template-columns: 2fr auto auto auto auto;
            gap: 15px;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .results-info {
            text-align: center;
            padding: 10px;
            background: var(--light-bg);
            border-radius: 8px;
            font-weight: 600;
            color: var(--primary-color);
        }
        
        .clear-btn {
            background: var(--warning-color);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .clear-btn:hover {
            background: #e67e22;
            transform: translateY(-2px);
        }
        
        .search-box {
            position: relative;
        }
        
        .search-input {
            width: 100%;
            padding: 12px 45px 12px 15px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            transition: var(--transition);
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--secondary-color);
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }
        
        .search-icon {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #666;
        }
        
        .filter-select {
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            background: white;
            cursor: pointer;
            transition: var(--transition);
        }
        
        .filter-select:focus {
            outline: none;
            border-color: var(--secondary-color);
        }
        
        .export-btn {
            background: var(--success-color);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .export-btn:hover {
            background: #219a52;
            transform: translateY(-2px);
        }
        
        .content {
            padding: 30px;
        }
        
        .detection-grid {
            display: grid;
            gap: 20px;
        }
        
        .detection-card {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--card-shadow);
            overflow: hidden;
            transition: var(--transition);
            border-left: 5px solid #ddd;
        }
        
        .detection-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }
        
        .detection-header {
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #eee;
            display: grid;
            grid-template-columns: 1fr auto auto;
            gap: 15px;
            align-items: center;
        }
        
        .file-info {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .file-path {
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: var(--primary-color);
            font-weight: 600;
        }
        
        .line-number {
            font-size: 12px;
            color: #666;
        }
        
        .risk-badge {
            padding: 6px 12px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 12px;
            text-transform: uppercase;
        }
        
        .risk-CRITICO { background: var(--critical-color); border-color: var(--critical-color); }
        .risk-ALTO { background: var(--danger-color); border-color: var(--danger-color); }
        .risk-MEDIO { background: var(--warning-color); border-color: var(--warning-color); }
        .risk-BAJO { background: var(--success-color); border-color: var(--success-color); }
        .risk-INFO { background: var(--info-color); border-color: var(--info-color); }
        
        .category-badge {
            padding: 4px 8px;
            background: var(--light-bg);
            border-radius: 4px;
            font-size: 11px;
            color: #666;
            text-transform: capitalize;
        }
        
        .detection-body {
            padding: 20px;
        }
        
        .code-section {
            margin-bottom: 15px;
        }
        
        .code-label {
            font-size: 12px;
            color: #666;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .code-block {
            background: #2d3748;
            border-radius: 8px;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.5;
        }
        
        .code-context {
            color: #a0aec0;
        }
        
        .code-highlight {
            background: rgba(229, 62, 62, 0.2);
            color: #fed7d7;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        .match-info {
            background: var(--light-bg);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        
        .match-text {
            font-family: 'Courier New', monospace;
            background: white;
            padding: 8px 12px;
            border-radius: 4px;
            border-left: 4px solid var(--accent-color);
            margin-top: 8px;
            font-size: 13px;
        }
        
        .no-detections {
            text-align: center;
            padding: 60px 20px;
            color: var(--success-color);
            font-size: 1.3em;
        }
        
        .no-detections i {
            font-size: 4em;
            margin-bottom: 20px;
            display: block;
        }
        
        .footer {
            background: var(--primary-color);
            color: white;
            text-align: center;
            padding: 30px;
        }
        
        .footer-links {
            margin-top: 15px;
        }
        
        .footer-links a {
            color: #bdc3c7;
            text-decoration: none;
            margin: 0 10px;
            transition: var(--transition);
        }
        
        .footer-links a:hover {
            color: white;
        }
        
        .hidden {
            display: none !important;
        }
        
        /* Estilos para alertas agrupadas */
        .alerts-summary {
            margin-top: 10px;
        }
        
        .alerts-list {
            margin-top: 15px;
        }
        
        .alert-item {
            background: var(--light-bg);
            border-radius: 8px;
            margin-bottom: 15px;
            padding: 15px;
            border-left: 4px solid var(--accent-color);
            transition: var(--transition);
        }
        
        .alert-item:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .alert-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .alert-line {
            font-weight: bold;
            color: var(--primary-color);
            font-size: 14px;
        }
        
        .alert-category {
            background: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            color: #666;
            text-transform: capitalize;
        }
        
        .alert-content {
            margin-top: 10px;
        }
        
        .code-preview {
            background: #2d3748;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 10px;
            overflow-x: auto;
        }
        
        .code-preview pre {
            color: #a0aec0;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
            margin: 0;
            white-space: pre-wrap;
            word-break: break-all;
        }
        
        .match-highlight {
            background: rgba(231, 76, 60, 0.1);
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 13px;
            color: var(--danger-color);
        }
        
        .match-highlight strong {
            color: var(--primary-color);
        }
        
        @media (max-width: 768px) {
            .controls-grid {
                grid-template-columns: 1fr;
                gap: 15px;
            }
            
            .detection-header {
                grid-template-columns: 1fr;
                gap: 10px;
            }
            
            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }
            
            .alert-header {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="version-badge">v3.0</div>
            <h1><i class="fas fa-shield-alt"></i> HZ Backdoor Checker</h1>
            <p class="subtitle">🔍 Análisis Avanzado de Seguridad para FiveM</p>
            <p>echo por hazteunsitio.net</p>
        </div>
        
        <div class="stats-section">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-file-code"></i></div>
                    <div class="stat-number">''' + str(total_archivos) + '''</div>
                    <div class="stat-label">Archivos Escaneados</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-exclamation-triangle"></i></div>
                    <div class="stat-number">''' + str(total_detecciones) + '''</div>
                    <div class="stat-label">Detecciones Encontradas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-bug"></i></div>
                    <div class="stat-number">''' + str(archivos_infectados) + '''</div>
                    <div class="stat-label">Archivos Afectados</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-clock"></i></div>
                    <div class="stat-number">''' + tiempo_escaneo + '''</div>
                    <div class="stat-label">Tiempo de Escaneo</div>
                </div>
            </div>
            
            <!-- Estadísticas por nivel de riesgo -->
            <div class="risk-stats">
                <h3><i class="fas fa-chart-bar"></i> Distribución por Nivel de Riesgo</h3>
                <div class="risk-grid">
                    ''' + ''.join([f'<div class="risk-stat"><span class="risk-badge risk-{nivel}">{nivel}</span><span class="risk-count">{count}</span></div>' for nivel, count in niveles_riesgo.items()]) + '''
                </div>
            </div>
            
            <!-- Estadísticas por categoría -->
            <div class="category-stats">
                <h3><i class="fas fa-tags"></i> Detecciones por Categoría</h3>
                <div class="category-grid">
                    ''' + ''.join([f'<div class="category-stat"><span class="category-name">{cat.replace("_", " ").title()}</span><span class="category-count">{count}</span></div>' for cat, count in categorias.items()]) + '''
                </div>
            </div>
        </div>
        
        <div class="controls-section">
            <div class="controls-grid">
                <div class="search-box">
                    <input type="text" id="searchInput" class="search-input" placeholder="Buscar en archivos, código o categorías...">
                    <i class="fas fa-search search-icon"></i>
                </div>
                <select id="riskFilter" class="filter-select">
                    <option value="">Todos los riesgos</option>
                    <option value="CRITICO">Crítico</option>
                    <option value="ALTO">Alto</option>
                    <option value="MEDIO">Medio</option>
                    <option value="BAJO">Bajo</option>
                    <option value="INFO">Info</option>
                </select>
                <select id="categoryFilter" class="filter-select">
                    <option value="">Todas las categorías</option>
                    ''' + ''.join([f'<option value="{cat.lower()}">{cat.replace("_", " ").title()}</option>' for cat in categorias.keys()]) + '''
                </select>
                <button class="clear-btn" onclick="limpiarFiltros()">
                    <i class="fas fa-eraser"></i>
                    Limpiar
                </button>
                <button class="export-btn" onclick="exportarResultados()">
                    <i class="fas fa-download"></i>
                    Exportar JSON
                </button>
            </div>
            <div class="results-info">
                <span id="resultsCount">Mostrando ''' + str(total_detecciones) + ''' detecciones</span>
            </div>
        </div>
        
        <div class="content">
            <h2><i class="fas fa-list"></i> Detecciones Encontradas</h2>
            <div id="detectionsContainer" class="detection-grid">
'''
    
    if not resultados_escaneo:
        html_content += '''
                <div class="no-detections">
                    <i class="fas fa-check-circle"></i>
                    <div>¡Excelente! No se detectaron códigos sospechosos en el escaneo.</div>
                    <p>Tu servidor FiveM parece estar libre de backdoors conocidos.</p>
                </div>
'''
    else:
        # Ordenar archivos agrupados por nivel de riesgo
        orden_riesgo = {'CRITICO': 0, 'ALTO': 1, 'MEDIO': 2, 'BAJO': 3, 'INFO': 4}
        archivos_ordenados = sorted(detecciones_agrupadas.values(), 
                                   key=lambda x: orden_riesgo.get(x['nivel_riesgo_max'], 5))
        
        for archivo_grupo in archivos_ordenados:
            archivo = html.escape(archivo_grupo['archivo'])
            riesgo_max = archivo_grupo['nivel_riesgo_max']
            detecciones = archivo_grupo['detecciones']
            categorias_archivo = list(archivo_grupo['categorias'])
            num_detecciones = len(detecciones)
            
            # Mostrar ruta completa del archivo
            ruta_mostrar = archivo.replace('\\', '/')
            nombre_archivo = archivo.split('\\')[-1] if '\\' in archivo else archivo.split('/')[-1]
            
            # Crear lista de categorías únicas
            categorias_str = ', '.join([cat.replace('_', ' ').title() for cat in categorias_archivo])
            
            html_content += f'''
                <div class="detection-card" data-risk="{riesgo_max}" data-category="{categorias_str.lower()}" data-file="{archivo.lower()}" data-code="">
                    <div class="detection-header">
                        <div class="file-info">
                            <div class="file-path"><i class="fas fa-file-code"></i> {ruta_mostrar}</div>
                            <div class="line-number"><i class="fas fa-exclamation-triangle"></i> {num_detecciones} alertas encontradas</div>
                        </div>
                        <div class="risk-badge risk-{riesgo_max}">{riesgo_max}</div>
                        <div class="category-badge">{categorias_str}</div>
                    </div>
                    <div class="detection-body">
                        <div class="alerts-summary">
                            <div class="code-label">Resumen de Alertas:</div>
                            <div class="alerts-list">
'''
            
            # Mostrar cada detección como un elemento de lista
            for i, deteccion in enumerate(detecciones):
                linea = deteccion.get('numero_linea', deteccion.get('linea', 'N/A'))
                categoria = deteccion['categoria'].replace('_', ' ').title()
                match_texto = html.escape(deteccion.get('match_texto', ''))
                codigo_linea = html.escape(deteccion.get('contenido_linea', ''))
                contexto = html.escape(deteccion.get('contexto', ''))
                
                html_content += f'''
                                <div class="alert-item">
                                    <div class="alert-header">
                                        <span class="alert-line">Línea {linea}</span>
                                        <span class="alert-category">{categoria}</span>
                                        <span class="risk-badge risk-{deteccion['nivel_riesgo']}">{deteccion['nivel_riesgo']}</span>
                                    </div>
                                    <div class="alert-content">
                                        <div class="code-preview">
                                            <pre>{contexto if contexto else codigo_linea}</pre>
                                        </div>
                                        <div class="match-highlight">
                                            <strong>Patrón:</strong> {match_texto}
                                        </div>
                                    </div>
                                </div>
'''
            
            html_content += '''
                            </div>
                        </div>
                    </div>
                </div>
'''
    
    html_content += '''
            </div>
        </div>
        
        <div class="footer">
            <p><i class="fas fa-shield-alt"></i> Generado por HZ Backdoor Checker v3.0</p>
            <p>❤️ echo por hazteunsitio.net - Mantén tu servidor FiveM seguro</p>
            <p><i class="fas fa-calendar"></i> Reporte generado el ''' + fecha_escaneo + '''</p>
            <div class="footer-links">
                <a href="#"><i class="fas fa-globe"></i> hazteunsitio.net</a>
                <a href="#"><i class="fab fa-github"></i> GitHub</a>
                <a href="#"><i class="fab fa-discord"></i> Discord</a>
            </div>
        </div>
    </div>
    
    <script>
        // Datos de detecciones para JavaScript
        const detecciones = ''' + detecciones_json + ''';
        
        // Funcionalidad de búsqueda y filtrado
        const searchInput = document.getElementById('searchInput');
        const riskFilter = document.getElementById('riskFilter');
        const categoryFilter = document.getElementById('categoryFilter');
        const detectionCards = document.querySelectorAll('.detection-card');
        const resultsCount = document.getElementById('resultsCount');
        
        function filtrarDetecciones() {
            const searchTerm = searchInput.value.toLowerCase();
            const riskLevel = riskFilter.value;
            const categoryLevel = categoryFilter.value;
            
            let visibleCount = 0;
            
            detectionCards.forEach(card => {
                const matchesSearch = !searchTerm || 
                    card.dataset.file.includes(searchTerm) ||
                    card.dataset.code.includes(searchTerm) ||
                    card.dataset.category.includes(searchTerm);
                    
                const matchesRisk = !riskLevel || card.dataset.risk === riskLevel;
                const matchesCategory = !categoryLevel || card.dataset.category === categoryLevel;
                
                if (matchesSearch && matchesRisk && matchesCategory) {
                    card.classList.remove('hidden');
                    visibleCount++;
                } else {
                    card.classList.add('hidden');
                }
            });
            
            // Actualizar contador
            resultsCount.textContent = `Mostrando $''' + '''{visibleCount} de $''' + '''{detectionCards.length} detecciones`;
        }
        
        function limpiarFiltros() {
            searchInput.value = '';
            riskFilter.value = '';
            categoryFilter.value = '';
            filtrarDetecciones();
        }
        
        searchInput.addEventListener('input', filtrarDetecciones);
        riskFilter.addEventListener('change', filtrarDetecciones);
        categoryFilter.addEventListener('change', filtrarDetecciones);
        
        // Función de exportación
        function exportarResultados() {
            const dataStr = JSON.stringify({
                timestamp: '''' + fecha_escaneo + '''',
                estadisticas: {
                    archivos_escaneados: ''' + str(total_archivos) + ''',
                    detecciones_encontradas: ''' + str(total_detecciones) + ''',
                    archivos_afectados: ''' + str(archivos_infectados) + ''',
                    tiempo_escaneo: '''' + tiempo_escaneo + ''''
                },
                detecciones: detecciones
            }, null, 2);
            
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'hz-backdoor-resultados-' + new Date().toISOString().split('T')[0] + '.json';
            link.click();
            URL.revokeObjectURL(url);
        }
        
        // Animaciones de entrada
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.detection-card');
            cards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
        
        // Estadísticas en tiempo real
        function actualizarEstadisticas() {
            const visibleCards = document.querySelectorAll('.detection-card:not(.hidden)');
            const riskCounts = {
                'CRITICO': 0,
                'ALTO': 0,
                'MEDIO': 0,
                'BAJO': 0,
                'INFO': 0
            };
            
            visibleCards.forEach(card => {
                const risk = card.dataset.risk;
                if (riskCounts.hasOwnProperty(risk)) {
                    riskCounts[risk]++;
                }
            });
            
            console.log('Estadísticas de riesgo:', riskCounts);
        }
        
        // Llamar a actualizar estadísticas cuando se filtre
        searchInput.addEventListener('input', actualizarEstadisticas);
        riskFilter.addEventListener('change', actualizarEstadisticas);
    </script>
</body>
</html>
'''
    
    # Guardar archivo
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Reporte HTML avanzado generado: {archivo_salida}")
        return archivo_salida
    except Exception as e:
        print(f"❌ Error generando reporte HTML: {e}")
        return None

if __name__ == "__main__":
    print("HZ Advanced Report Generator - echo por hazteunsitio.net")