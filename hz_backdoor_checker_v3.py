import os
import re
import sys
import json
import time
import html
import hashlib
import threading
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

class HZBackdoorCheckerV3:
    def __init__(self, config_file=None):
        self.version = "3.0"
        self.mostrar_banner()
        
        # Configuración mejorada
        self.config = self.cargar_configuracion(config_file)
        
        # Inicializar resultados
        self.resultados_escaneo = []
        self.total_archivos = 0
        
        # Estadísticas mejoradas
        self.estadisticas = {
            'archivos_escaneados': 0,
            'archivos_omitidos': 0,
            'tiempo_inicio': None,
            'tiempo_fin': None,
            'errores': [],
            'archivos_con_detecciones': set(),
            'detecciones_por_categoria': {},
            'hash_archivos': {}
        }
        
        # Lock para threading
        self.lock = threading.Lock()
        
        # Inicializar patrones mejorados
        self._inicializar_patrones_mejorados()
        
    def mostrar_banner(self):
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🛡️  HZ BACKDOOR CHECKER PARA FIVEM v{self.version}  🛡️        ║
║                                                              ║
║              🌟 Desarrollado por: hazteunsitio.net 🌟        ║
║                   Versión Optimizada Anti-FP                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
        
    def cargar_configuracion(self, config_file):
        """Carga configuración optimizada"""
        config_default = {
            'max_workers': 4,
            'mostrar_progreso': True,
            'guardar_json': True,
            'verificar_hashes': True,
            'nivel_sensibilidad': 'MEDIO',  # BAJO, MEDIO, ALTO
            'excluir_frameworks': True,
            'solo_alto_riesgo': False
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_usuario = json.load(f)
                    config_default.update(config_usuario)
            except Exception as e:
                print(f"⚠️  Error cargando configuración: {e}")
        
        return config_default
    
    def _inicializar_patrones_mejorados(self):
        """Patrones optimizados para reducir falsos positivos"""
        
        # Dominios confiables expandidos para FiveM
        self.dominios_confiables = {
            'github.com', 'raw.githubusercontent.com', 'gist.githubusercontent.com',
            'discord.com', 'discordapp.com', 'cdn.discordapp.com',
            'fivemanager.com', 'api.fivemanager.com',
            'cfx.re', 'forum.cfx.re', 'docs.fivem.net', 'runtime.fivem.net',
            'keymaster.fivem.net', 'policy.fivem.net',
            'localhost', '127.0.0.1', '0.0.0.0',
            'pastebin.com', 'hastebin.com', 'paste.ee',
            'googleapis.com', 'google.com', 'microsoft.com',
            'api.github.com', 'avatars.githubusercontent.com'
        }
        
        # Lista blanca expandida para FiveM
        self.patrones_lista_blanca = [
            # Comentarios y documentación
            r'--.*?backdoor', r'//.*?backdoor', r'/\*.*?backdoor.*?\*/',
            r'print\s*\(\s*["\'].*?backdoor.*?["\']',
            
            # Funciones legítimas de FiveM/ESX
            r'exports\[.*?\]', r'exports\..*?\(',
            r'ESX\.|esx\.|ESX:', r'QBCore\.|qb-',
            r'RegisterServerEvent', r'RegisterNetEvent', r'RegisterCommand',
            r'TriggerEvent\s*\(\s*["\']esx:', r'TriggerServerEvent\s*\(\s*["\']esx:',
            
            # Frameworks comunes
            r'ox_lib', r'ox_inventory', r'ox_target',
            r'qtarget', r'qb-target', r'bt-target',
            
            # Funciones de desarrollo
            r'debug\.', r'-- Example:', r'-- Test:', r'-- TODO:',
            r'console\.log', r'print\s*\(\s*["\']DEBUG',
            
            # Patrones de configuración
            r'Config\.|config\.|cfg\.',
            r'shared\.|client\.|server\.',
            
            # Funciones de carga legítimas
            r'LoadResourceFile\s*\(\s*GetCurrentResourceName\(\)',
            r'load\s*\(\s*LoadResourceFile\s*\(\s*GetCurrentResourceName\(\)',
            
            # Patrones de template engines
            r'template\s*=\s*load\s*\(',
            r'assert\s*\(\s*load\s*\(.*?template.*?\)',
        ]
        
        # Patrones más específicos y menos agresivos
        self.patrones_backdoor = {
            'ejecucion_remota_critica': [
                # Solo patrones realmente sospechosos
                r'loadstring\s*\(\s*PerformHttpRequest\s*\(',
                r'load\s*\(\s*PerformHttpRequest\s*\(',
                r'dofile\s*\(\s*["\']https?://(?!(?:' + '|'.join(self.dominios_confiables) + '))',
                r'require\s*\(\s*["\']https?://(?!(?:' + '|'.join(self.dominios_confiables) + '))',
                r'RunString\s*\(\s*http\.',
                r'CompileString\s*\(\s*http\.',
            ],
            
            'conexiones_http_sospechosas': [
                # Solo URLs realmente sospechosas
                r'PerformHttpRequest\s*\(\s*["\']https?://(?!(?:' + '|'.join(self.dominios_confiables) + r'))[^"\'\/]*\.[a-z]{2,}(?:\/[^"\']*)?\/[^"\'\/]*\.(?:php|asp|jsp|py)(?:\?[^"\']*)?\/[^"\']',
                r'http\.(?:post|get)\s*\(\s*["\']https?://(?!(?:' + '|'.join(self.dominios_confiables) + r'))[^"\']*/(?:admin|panel|backdoor|shell)',
            ],
            
            'comandos_administrativos_sospechosos': [
                # Solo comandos realmente peligrosos
                r'ExecuteCommand\s*\(\s*["\'](?:restart|stop|quit)\s+[^"\']',
                r'TriggerServerEvent\s*\(\s*["\']__cfx_internal:.*?rcon',
                r'rconPassword\s*=\s*["\'][^"\']',
                r'ExecuteCommand\s*\(\s*["\']ban\s+\d+\s+0\s+',  # Ban permanente
            ],
            
            'acceso_archivos_critico': [
                # Solo acceso realmente sospechoso
                r'io\.open\s*\(\s*["\'].*?\.(?:exe|bat|cmd|ps1)',
                r'os\.execute\s*\(\s*["\'](?:del|rm|format|shutdown)',
                r'io\.popen\s*\(\s*["\'](?:cmd|powershell|bash)',
                r'file\.Delete\s*\(\s*["\'].*?\.(?:lua|js|cfg)',
            ],
            
            'codigo_altamente_ofuscado': [
                # Solo ofuscación extrema
                r'string\.char\s*\(\s*\d+(?:\s*,\s*\d+){20,}',  # Más de 20 caracteres
                r'\\x[0-9a-fA-F]{2}(?:\\x[0-9a-fA-F]{2}){10,}',  # Más de 10 hex chars
                r'_G\[.*?string\.char.*?\]\s*\(',
            ]
        }
        
        # Ajustar sensibilidad según configuración
        if self.config.get('nivel_sensibilidad') == 'BAJO':
            # Solo patrones críticos
            self.patrones_backdoor = {
                k: v for k, v in self.patrones_backdoor.items() 
                if 'critica' in k or 'critico' in k
            }
        elif self.config.get('nivel_sensibilidad') == 'ALTO':
            # Agregar patrones adicionales
            self.patrones_backdoor['acceso_archivos_medio'] = [
                r'LoadResourceFile\s*\(\s*[^,]+,\s*["\'](?!(?:config|shared|client|server))',
            ]
        
        self.patron_url = re.compile(r'https?://([^/\s\'"]+)', re.IGNORECASE)
        self.archivos_escaneados = 0
        
    def esta_en_lista_blanca(self, linea):
        """Verificación mejorada de lista blanca"""
        linea_limpia = linea.strip().lower()
        
        # Saltar líneas vacías y comentarios
        if not linea_limpia or linea_limpia.startswith('--') or linea_limpia.startswith('//'):
            return True
            
        # Verificar patrones de lista blanca
        for patron in self.patrones_lista_blanca:
            if re.search(patron, linea, re.IGNORECASE):
                return True
                
        # Verificar si es parte de un framework conocido
        if self.config.get('excluir_frameworks', True):
            frameworks = ['esx', 'qbcore', 'ox_lib', 'qtarget', 'mythic_']
            if any(fw in linea_limpia for fw in frameworks):
                return True
                
        return False
    
    def url_es_segura(self, url):
        """Verificación mejorada de URLs"""
        try:
            parsed = urlparse(url.lower())
            domain = parsed.netloc
            
            if ':' in domain:
                domain = domain.split(':')[0]
            
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Verificar dominios confiables
            if domain in self.dominios_confiables:
                return True
                
            # Verificar subdominios de dominios confiables
            for dominio_confiable in self.dominios_confiables:
                if domain.endswith('.' + dominio_confiable):
                    return True
                    
            return False
        except:
            return False
    
    def escanear_archivo(self, ruta_archivo):
        """Escaneo optimizado con menos falsos positivos"""
        try:
            # Verificar tamaño del archivo
            tamaño_archivo = os.path.getsize(ruta_archivo)
            if tamaño_archivo > 5 * 1024 * 1024:  # 5MB límite
                return []
            
            with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
                lineas = contenido.split('\n')
                
            detecciones = []
            detecciones_unicas = set()  # Para evitar duplicados
            
            for num_linea, linea in enumerate(lineas, 1):
                if self.esta_en_lista_blanca(linea):
                    continue
                
                linea_limpia = linea.strip()
                if not linea_limpia:
                    continue
                
                for categoria, patrones in self.patrones_backdoor.items():
                    for patron in patrones:
                        try:
                            match = re.search(patron, linea, re.IGNORECASE)
                            if match:
                                # Verificación adicional para reducir falsos positivos
                                if self._es_deteccion_valida(categoria, linea, match):
                                    # Crear clave única para evitar duplicados
                                    clave_unica = f"{ruta_archivo}:{categoria}:{match.group(0)}"
                                    
                                    if clave_unica not in detecciones_unicas:
                                        detecciones_unicas.add(clave_unica)
                                        
                                        deteccion = {
                                            'archivo': os.path.abspath(ruta_archivo),  # Ruta completa absoluta
                                            'numero_linea': num_linea,
                                            'contenido_linea': linea.strip(),
                                            'categoria': categoria,
                                            'patron': patron,
                                            'match_texto': match.group(0),
                                            'nivel_riesgo': self.determinar_nivel_riesgo(categoria),
                                            'contexto': self._obtener_contexto(lineas, num_linea),
                                            'timestamp': datetime.now().isoformat()
                                        }
                                        detecciones.append(deteccion)
                        except re.error:
                            continue
            
            return detecciones
            
        except Exception as e:
            with self.lock:
                self.estadisticas['errores'].append(f"Error leyendo {ruta_archivo}: {str(e)}")
            return []
    
    def _es_deteccion_valida(self, categoria, linea, match):
        """Validación adicional para reducir falsos positivos"""
        linea_lower = linea.lower()
        
        # Verificaciones específicas por categoría
        if 'http' in categoria:
            # Verificar si la URL es realmente sospechosa
            urls = self.patron_url.findall(linea)
            return any(not self.url_es_segura('http://' + url) for url in urls)
            
        if 'ejecucion_remota' in categoria:
            # Verificar que no sea una función de template legítima
            if 'template' in linea_lower or 'view' in linea_lower:
                return False
                
        if 'acceso_archivos' in categoria:
            # Verificar que no sea acceso a archivos de configuración legítimos
            if any(cfg in linea_lower for cfg in ['config', 'shared', 'client', 'server']):
                return False
                
        return True
    
    def _obtener_contexto(self, lineas, num_linea, contexto_lineas=2):
        """Obtiene el contexto alrededor de la línea detectada"""
        inicio = max(0, num_linea - contexto_lineas - 1)
        fin = min(len(lineas), num_linea + contexto_lineas)
        
        contexto = []
        for i in range(inicio, fin):
            prefijo = ">>> " if i == num_linea - 1 else "    "
            contexto.append(f"{prefijo}{i+1}: {lineas[i].strip()}")
            
        return "\n".join(contexto)
    
    def determinar_nivel_riesgo(self, categoria):
        """Determinación mejorada de nivel de riesgo"""
        niveles_riesgo = {
            'CRITICO': ['ejecucion_remota_critica', 'inyeccion_dll', 'manipulacion_memoria'],
            'ALTO': ['conexiones_http_sospechosas', 'acceso_archivos_critico', 'comandos_administrativos_sospechosos'],
            'MEDIO': ['codigo_altamente_ofuscado', 'acceso_archivos_medio'],
            'BAJO': ['comandos_sospechosos_menores'],
            'INFO': ['debug_info', 'comentarios_sospechosos']
        }
        
        for nivel, categorias in niveles_riesgo.items():
            if any(cat in categoria for cat in categorias):
                return nivel
        
        return 'MEDIO'
    
    def mostrar_progreso(self, actual, total, archivo_actual=""):
        """Barra de progreso mejorada"""
        if not self.config.get('mostrar_progreso', True):
            return
            
        porcentaje = (actual / total) * 100 if total > 0 else 0
        barra_longitud = 50
        relleno = int(barra_longitud * actual // total) if total > 0 else 0
        barra = '█' * relleno + '░' * (barra_longitud - relleno)
        
        archivo_mostrar = archivo_actual[:40] + "..." if len(archivo_actual) > 40 else archivo_actual
        
        print(f"\r🔍 [{barra}] {porcentaje:.1f}% ({actual}/{total}) - {archivo_mostrar}", end='', flush=True)
        
        if actual == total:
            print()
    
    def escanear_carpeta(self, ruta_carpeta):
        """Escaneo optimizado de carpeta"""
        print(f"\n🔍 Iniciando escaneo optimizado: {ruta_carpeta}")
        print(f"⚙️  Nivel de sensibilidad: {self.config.get('nivel_sensibilidad', 'MEDIO')}")
        
        # Buscar archivos
        archivos_encontrados = []
        extensiones = ['.lua', '.js', '.ts']
        
        for root, dirs, files in os.walk(ruta_carpeta):
            # Excluir directorios innecesarios
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
                'node_modules', '__pycache__', '.git', 'cache', 'logs'
            ]]
            
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensiones):
                    archivos_encontrados.append(os.path.join(root, file))
        
        self.total_archivos = len(archivos_encontrados)
        print(f"📁 Archivos encontrados: {self.total_archivos}")
        
        if self.total_archivos == 0:
            print("⚠️ No se encontraron archivos para escanear")
            return
        
        # Inicializar estadísticas
        self.estadisticas['tiempo_inicio'] = datetime.now()
        
        # Procesamiento con threading
        max_workers = min(self.config.get('max_workers', 4), self.total_archivos)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.procesar_archivo_con_progreso, archivo, i): archivo 
                      for i, archivo in enumerate(archivos_encontrados)}
            
            for future in as_completed(futures):
                try:
                    detecciones = future.result()
                    if detecciones:
                        with self.lock:
                            # Filtrar por nivel de riesgo si está configurado
                            if self.config.get('solo_alto_riesgo', False):
                                detecciones = [d for d in detecciones if d['nivel_riesgo'] in ['CRITICO', 'ALTO']]
                            
                            self.resultados_escaneo.extend(detecciones)
                            
                            for deteccion in detecciones:
                                categoria = deteccion['categoria']
                                self.estadisticas['detecciones_por_categoria'][categoria] = \
                                    self.estadisticas['detecciones_por_categoria'].get(categoria, 0) + 1
                except Exception as e:
                    archivo = futures[future]
                    with self.lock:
                        self.estadisticas['errores'].append(f"Error procesando {archivo}: {str(e)}")
        
        self.mostrar_progreso(self.total_archivos, self.total_archivos, "Completado")
        self.mostrar_estadisticas_finales()
    
    def procesar_archivo_con_progreso(self, archivo, indice):
        """Procesa archivo individual con progreso"""
        detecciones = self.escanear_archivo(archivo)
        
        with self.lock:
            self.archivos_escaneados += 1
            self.estadisticas['archivos_escaneados'] += 1
            if detecciones:
                self.estadisticas['archivos_con_detecciones'].add(str(archivo))
            self.mostrar_progreso(self.archivos_escaneados, self.total_archivos, 
                                os.path.basename(archivo))
        
        return detecciones
    
    def mostrar_estadisticas_finales(self):
        """Estadísticas finales mejoradas"""
        tiempo_transcurrido = datetime.now() - self.estadisticas['tiempo_inicio']
        
        print("\n" + "="*70)
        print("📊 ESTADÍSTICAS DEL ESCANEO OPTIMIZADO")
        print("="*70)
        print(f"⏱️  Tiempo transcurrido: {tiempo_transcurrido}")
        print(f"📁 Archivos escaneados: {self.estadisticas['archivos_escaneados']}")
        print(f"🚨 Archivos con detecciones: {len(self.estadisticas['archivos_con_detecciones'])}")
        print(f"⚠️  Total de detecciones: {len(self.resultados_escaneo)}")
        print(f"🎯 Nivel de sensibilidad: {self.config.get('nivel_sensibilidad', 'MEDIO')}")
        
        if self.estadisticas['detecciones_por_categoria']:
            print("\n🏷️  Detecciones por categoría:")
            for categoria, cantidad in sorted(self.estadisticas['detecciones_por_categoria'].items()):
                print(f"   • {categoria}: {cantidad}")
        
        # Mostrar resumen de riesgo
        niveles_riesgo = {}
        for deteccion in self.resultados_escaneo:
            nivel = deteccion['nivel_riesgo']
            niveles_riesgo[nivel] = niveles_riesgo.get(nivel, 0) + 1
        
        if niveles_riesgo:
            print("\n🎯 Detecciones por nivel de riesgo:")
            for nivel in ['CRITICO', 'ALTO', 'MEDIO', 'BAJO', 'INFO']:
                if nivel in niveles_riesgo:
                    print(f"   • {nivel}: {niveles_riesgo[nivel]}")
        
        print("="*70)
    
    def exportar_json(self, archivo_salida='hz-backdoor-resultados-v3.json'):
        """Exporta resultados a JSON"""
        if not self.config.get('guardar_json', True):
            return
            
        datos_exportacion = {
            'version': self.version,
            'timestamp': datetime.now().isoformat(),
            'configuracion': self.config,
            'estadisticas': {
                **self.estadisticas,
                'archivos_con_detecciones': list(self.estadisticas['archivos_con_detecciones']),
                'tiempo_inicio': self.estadisticas['tiempo_inicio'].isoformat() if self.estadisticas['tiempo_inicio'] else None
            },
            'detecciones': self.resultados_escaneo
        }
        
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(datos_exportacion, f, indent=2, ensure_ascii=False)
            print(f"✅ Resultados exportados a: {archivo_salida}")
        except Exception as e:
            print(f"❌ Error exportando JSON: {e}")
    
    def mostrar_resumen_consola(self):
        """Resumen final en consola"""
        total_detecciones = len(self.resultados_escaneo)
        
        if total_detecciones == 0:
            print("\n✅ ¡Excelente! No se detectaron códigos sospechosos.")
            return
        
        print(f"\n🚨 SE DETECTARON {total_detecciones} CÓDIGOS SOSPECHOSOS")
        
        # Contar por nivel de riesgo
        criticos = sum(1 for d in self.resultados_escaneo if d['nivel_riesgo'] == 'CRITICO')
        altos = sum(1 for d in self.resultados_escaneo if d['nivel_riesgo'] == 'ALTO')
        medios = sum(1 for d in self.resultados_escaneo if d['nivel_riesgo'] == 'MEDIO')
        
        if criticos > 0:
            print(f"🔴 {criticos} detecciones CRÍTICAS - Revisar inmediatamente")
        if altos > 0:
            print(f"🟠 {altos} detecciones de ALTO riesgo")
        if medios > 0:
            print(f"🟡 {medios} detecciones de riesgo MEDIO")
        
        print("\n📄 Revisa el reporte HTML para más detalles")

def main():
    """Función principal mejorada"""
    print("\n" + "="*80)
    print("🛡️  HZ BACKDOOR CHECKER v3.0 - DETECTOR OPTIMIZADO FIVEM")
    print("🌟 echo por hazteunsitio.net - Versión Anti-Falsos Positivos")
    print("="*80)
    
    if len(sys.argv) < 2:
        print("\n📁 Introduce la ruta de tu carpeta de resources:")
        print("💡 Ejemplo: C:/FXServer/resources")
        carpeta_objetivo = input("\n🔍 Ruta a escanear: ").strip()
        
        if not carpeta_objetivo:
            print("\n❌ Error: Debes especificar una carpeta")
            sys.exit(1)
    else:
        carpeta_objetivo = sys.argv[1]
    
    if not os.path.exists(carpeta_objetivo):
        print(f"\n❌ Error: La carpeta '{carpeta_objetivo}' no existe")
        sys.exit(1)
    
    # Crear instancia del checker optimizado
    checker = HZBackdoorCheckerV3()
    
    # Escanear carpeta
    checker.escanear_carpeta(carpeta_objetivo)
    
    # Generar reporte HTML mejorado
    print("\n📄 Generando reporte HTML avanzado...")
    from hz_advanced_report import generar_reporte_avanzado
    generar_reporte_avanzado(checker.resultados_escaneo, checker.estadisticas)
    
    # Exportar JSON
    checker.exportar_json()
    
    # Mostrar resumen
    checker.mostrar_resumen_consola()
    
    print("\n🎯 ¡Escaneo optimizado completado!")
    print("🌟 echo por hazteunsitio.net - Mantén tu servidor seguro")

if __name__ == "__main__":
    main()