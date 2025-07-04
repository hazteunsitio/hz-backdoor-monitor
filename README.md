# 🛡️ HZ Backdoor Checker v3.0

**Herramienta avanzada de detección de backdoors para servidores FiveM**

*Desarrollado por hazteunsitio.net*

---

## 📋 Descripción

HZ Backdoor Checker v3.0 es una herramienta profesional diseñada específicamente para detectar códigos maliciosos, backdoors y vulnerabilidades de seguridad en servidores FiveM. La herramienta analiza archivos Lua, JavaScript y TypeScript en busca de patrones sospechosos que podrían comprometer la seguridad de tu servidor.

## ✨ Características Principales

### 🔍 Detección Avanzada
- **Análisis de patrones específicos**: Detección de ejecución remota, conexiones HTTP sospechosas, comandos administrativos peligrosos
- **Eliminación de duplicados**: Los patrones repetidos se muestran solo una vez en el reporte
- **Rutas completas**: Muestra la ruta absoluta completa de cada archivo detectado
- **Contexto de código**: Proporciona el contexto alrededor de cada detección
- **Niveles de riesgo**: Clasificación automática (Crítico, Alto, Medio, Bajo, Info)

### 📊 Reportes Profesionales
- **Reporte HTML avanzado**: Interfaz moderna y responsive con filtros dinámicos
- **Estadísticas detalladas**: Análisis por categorías y niveles de riesgo
- **Búsqueda en tiempo real**: Filtrado por archivo, código o categoría
- **Exportación JSON**: Datos estructurados para análisis adicional
- **Gráficos interactivos**: Visualización de estadísticas de seguridad

### ⚡ Rendimiento Optimizado
- **Procesamiento multihilo**: Escaneo rápido de grandes directorios
- **Filtrado inteligente**: Exclusión automática de archivos irrelevantes
- **Whitelist configurable**: Reducción de falsos positivos
- **Límites de tamaño**: Control de memoria y rendimiento

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior
- Módulos estándar de Python (incluidos por defecto)

### Instalación Rápida
```bash
# Clonar el repositorio
git clone https://github.com/hazteunsitio/hz-backdoor-checker.git
cd hz-backdoor-checker

# Ejecutar directamente (no requiere instalación adicional)
python hz_backdoor_checker_v3.py "ruta/a/tu/servidor/fivem"
```

## 📖 Uso

### Comando Básico
```bash
python hz_backdoor_checker_v3.py "C:\tu\servidor\fivem\resources"
```

### Ejemplos de Uso
```bash
# Escanear recursos de FiveM
python hz_backdoor_checker_v3.py "C:\FXServer\resources"

# Escanear con configuración personalizada
python hz_backdoor_checker_v3.py "C:\FXServer\resources" --config config.json
```

## 📁 Estructura del Proyecto

```
hz-backdoor-checker/
├── hz_backdoor_checker_v3.py    # Script principal v3.0
├── hz_advanced_report.py         # Generador de reportes HTML
├── config.json                   # Configuración del escáner
├── README.md                     # Este archivo
└── reportes/                     # Carpeta de reportes generados
    ├── hz-backdoor-reporte-avanzado.html
    └── hz-backdoor-resultados.json
```

## ⚙️ Configuración

El archivo `config.json` permite personalizar el comportamiento del escáner:

```json
{
  "performance": {
    "max_workers": 4,
    "max_file_size": 10485760
  },
  "detection": {
    "custom_patterns": [],
    "trusted_domains": [
      "github.com",
      "cfx.re",
      "fivem.net"
    ]
  },
  "reporting": {
    "html_report_name": "hz-backdoor-reporte-avanzado.html",
    "json_report_name": "hz-backdoor-resultados.json"
  }
}
```

## 🎯 Tipos de Detección

### 🔴 Crítico
- Ejecución remota de código
- Funciones eval() y Function() sospechosas
- Conexiones a dominios no confiables
- Comandos de sistema peligrosos

### 🟠 Alto
- Acceso a archivos del sistema
- Manipulación de procesos
- Conexiones HTTP no cifradas
- Patrones de ofuscación

### 🟡 Medio
- Uso de librerías de red
- Acceso a variables de entorno
- Patrones de codificación sospechosos

### 🟢 Bajo
- Comentarios sospechosos
- Nombres de variables inusuales
- Patrones de desarrollo cuestionables

## 📊 Interpretación de Resultados

### Reporte HTML
El reporte HTML incluye:
- **Dashboard de estadísticas**: Resumen visual del escaneo
- **Filtros dinámicos**: Por riesgo, categoría y búsqueda de texto
- **Detalles de detección**: Código, contexto y ubicación exacta
- **Exportación de datos**: Descarga de resultados en JSON

### Reporte JSON
Estructura de datos para integración con otras herramientas:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "estadisticas": {
    "archivos_escaneados": 150,
    "detecciones_encontradas": 5,
    "archivos_afectados": 3
  },
  "detecciones": [...]
}
```

## 🛠️ Solución de Problemas

### Falsos Positivos
- **Problema**: Detección de código legítimo
- **Solución**: Agregar dominios/patrones a la whitelist en `config.json`

### Rendimiento Lento
- **Problema**: Escaneo tarda mucho tiempo
- **Solución**: Reducir `max_workers` o aumentar `max_file_size` en configuración

### Errores de Codificación
- **Problema**: Caracteres especiales no se muestran correctamente
- **Solución**: Verificar que los archivos estén en UTF-8

## 🔄 Changelog

### v3.0 (Actual)
- ✅ Eliminación de detecciones duplicadas
- ✅ Rutas completas en reportes
- ✅ Interfaz HTML mejorada y profesional
- ✅ Filtros avanzados por categoría
- ✅ Estadísticas detalladas por riesgo
- ✅ Optimización de rendimiento
- ✅ Mejor detección de falsos positivos

### v2.0
- Reporte HTML básico
- Detección por categorías
- Configuración JSON

### v1.0
- Detección básica de patrones
- Salida en consola

## 🤝 Contribuir

¿Encontraste un bug o tienes una sugerencia? 

1. **Reporta issues**: Describe el problema detalladamente
2. **Sugiere mejoras**: Nuevos patrones de detección o características
3. **Contribuye código**: Fork, mejora y envía pull requests

## 📞 Soporte

- **Website**: [hazteunsitio.net](https://hazteunsitio.net)
- **Discord**: Únete a nuestro servidor de Discord
- **GitHub**: Reporta issues en el repositorio oficial

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## ⚠️ Disclaimer

Esta herramienta está diseñada para ayudar a identificar posibles vulnerabilidades de seguridad. Los resultados deben ser revisados manualmente por un profesional de seguridad. No nos hacemos responsables por falsos positivos o negativos.

---

**🛡️ Mantén tu servidor FiveM seguro con HZ Backdoor Checker v3.0**

*Desarrollado con ❤️ por hazteunsitio.net*