# 📑 ÍNDICE DE DOCUMENTACIÓN - Bucle2D

**Versión**: 1.0  
**Fecha**: 30 de Diciembre de 2025  
**Estado**: ✅ LISTO PARA EXPERIMENTACIÓN

---

## 🚀 COMIENZA AQUÍ (Quick Start - 5 min)

Si es la primera vez trabajando en Bucle2D:

1. **Leer**: [PROJECT_STATUS.md](PROJECT_STATUS.md) (5 min) - Overview del proyecto
2. **Ejecutar**: [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) (5 min) - Cómo regenerar todo
3. **Revisar**: [VALIDATION_REPORT.txt](VALIDATION_REPORT.txt) (5 min) - Estadísticas

---

## 📚 DOCUMENTACIÓN COMPLETA

### 1. **ESTADO DEL PROYECTO**

| Documento | Propósito | Tiempo de Lectura |
|-----------|-----------|-------------------|
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Estado actual, estadísticas, próximos pasos | 10 min |
| [REGENERATION_SUMMARY.md](REGENERATION_SUMMARY.md) | Resumen de la regeneración completa | 8 min |
| [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | Resumen ejecutivo para stakeholders | 10 min |

### 2. **GUÍAS DE EJECUCIÓN**

| Documento | Propósito | Tiempo de Lectura |
|-----------|-----------|-------------------|
| [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) | Cómo ejecutar scripts, troubleshooting | 15 min |
| [VALIDATION_REPORT.txt](VALIDATION_REPORT.txt) | Estadísticas detalladas del dataset | 15 min |

### 3. **INVESTIGACIÓN & PAPER**

| Documento | Propósito | Ubicación |
|-----------|-----------|-----------|
| Artículo Académico | Secciones 4-5: Experimental Validation & Results | [paper/main.tex](paper/main.tex) |
| Referencias BibTeX | Bibliografía del paper | [paper/references.bib](paper/references.bib) |
| Instrucciones Paper | README del paper | [paper/README.md](paper/README.md) |

### 4. **DATOS & ANÁLISIS**

| Documento | Propósito | Ubicación |
|-----------|-----------|-----------|
| Dataset Documentation | Detalles del dataset Aspar-Synth-10K | [data/aspar_synth_10k/README.md](data/aspar_synth_10k/README.md) |
| Metadata Ejemplo | Estructura JSON del dataset | [data/aspar_synth_10k/dataset_metadata.json](data/aspar_synth_10k/dataset_metadata.json) |

### 5. **SCRIPTS & CÓDIGO**

#### Generadores
```python
# Generar dataset sintético
scripts/generate_aspar_synth_10k.py
  ├── AsparCircuitConfig         - Configuración del circuito
  ├── TelemetryGenerator         - Genera telemetría 100Hz
  ├── VideoMetadataGenerator     - Genera metadata 4K 60FPS
  └── AsparSynth10KGenerator     - Orquestador principal

# Análisis del dataset
scripts/analyze_dataset.py
  ├── print_summary()            - Estadísticas en consola
  ├── plot_lap_times()           - Visualización de tiempos
  ├── plot_weather_impact()      - Impacto del clima
  ├── plot_anomalies()           - Distribución de anomalías
  └── plot_telemetry()           - Muestra de telemetría

# Validación
scripts/generate_validation_report.py
  └── Genera VALIDATION_REPORT.txt de 10 secciones
```

#### Papel
```python
# Generar figuras científicas
paper/generate_figures.py
  ├── Fig 8: Track entropy map (CAG/RAG zones)
  ├── Fig 9: Latency PDF (bimodal distribution)
  ├── Fig 10: Latency comparison (scenarios A,B,C)
  ├── Fig 11: F1-Score comparison
  ├── Fig 12: Confusion matrix heatmap
  ├── Fig 13: Agent orchestration trace
  └── Fig 14: Power profiling trace
```

---

## 🗂️ ESTRUCTURA DE ARCHIVOS

```
/workspaces/Bucle2D/
│
├── 📊 DOCUMENTACIÓN (Este índice)
│   ├── PROJECT_STATUS.md                    ⭐ LEER PRIMERO
│   ├── REGENERATION_SUMMARY.md
│   ├── EXECUTIVE_SUMMARY.md
│   ├── EXECUTION_GUIDE.md
│   ├── VALIDATION_REPORT.txt
│   ├── INDEX.md                             (Este archivo)
│   └── README.md                            (Project overview)
│
├── 📄 PAPER & FIGURAS
│   ├── paper/main.tex                       ✅ Secciones 4-5 completas
│   ├── paper/references.bib                 ✅ Bibliografía
│   ├── paper/generate_figures.py            ✅ Script para 7 figuras
│   └── paper/figures/                       ✅ 14 archivos (7 PDF + 7 PNG)
│       ├── fig8_entropy_track_map.{pdf,png}
│       ├── fig9_latency_density.{pdf,png}
│       ├── fig10_latency_comparison.{pdf,png}
│       ├── fig11_f1_comparison.{pdf,png}
│       ├── fig12_confusion_matrix.{pdf,png}
│       ├── fig13_agent_trace.{pdf,png}
│       └── fig14_power_trace.{pdf,png}
│
├── 📊 DATASET (500 LAPS)
│   ├── data/aspar_synth_10k/README.md       ✅ Dataset docs
│   ├── data/aspar_synth_10k/dataset_metadata.json
│   ├── data/aspar_synth_10k/dataset_summary.json
│   ├── data/aspar_synth_10k/telemetry/      ✅ 5 chunks JSON
│   ├── data/aspar_synth_10k/video_metadata/ ✅ 500 archivos JSON
│   └── data/aspar_synth_10k/visualizations/ ✅ 4 PNG plots
│
├── 🔧 SCRIPTS
│   ├── scripts/generate_aspar_synth_10k.py  ✅ 470 líneas
│   ├── scripts/analyze_dataset.py           ✅ 355 líneas
│   └── scripts/generate_validation_report.py ✅ 200 líneas
│
└── 📦 CÓDIGO FUENTE
    ├── src/agent_orchestrator.py            (Sistema CAG/RAG)
    ├── src/memory_systems.py
    ├── src/vision_encoder.py
    └── src/main_inference.py
```

---

## 🎯 NAVEGACIÓN POR CASO DE USO

### "Quiero entender el proyecto en 10 minutos"
1. Lee [PROJECT_STATUS.md](PROJECT_STATUS.md) - Overview completo
2. Mira las tablas de estadísticas
3. Revisa los escenarios de prueba (A, B, C)

### "Quiero regenerar el dataset"
1. Lee [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) - Instrucciones paso a paso
2. Ejecuta los 4 comandos (5 minutos total)
3. Verifica resultados en [VALIDATION_REPORT.txt](VALIDATION_REPORT.txt)

### "Quiero escalarlo a 10,000 laps"
1. Consulta [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) - Sección "Customización"
2. Ejecuta: `python scripts/generate_aspar_synth_10k.py --num-laps 10000`
3. Espera ~90 minutos
4. Rerun análisis y figuras

### "Quiero leer el artículo académico"
1. Abre [paper/main.tex](paper/main.tex)
2. Enfócate en Secciones 4-5 (Experimental Validation & Results)
3. Revisa las figuras en [paper/figures/](paper/figures/)

### "Quiero validar las hipótesis H1, H2, H3"
1. Lee "Validación de Hipótesis" en [VALIDATION_REPORT.txt](VALIDATION_REPORT.txt)
2. Accede a los datos en [data/aspar_synth_10k/](data/aspar_synth_10k/)
3. Usa los escenarios de prueba (A, B, C)

### "Quiero entender el dataset"
1. Lee [data/aspar_synth_10k/README.md](data/aspar_synth_10k/README.md)
2. Revisa la Sección 4 del paper (main.tex) - "Experimental Setup"
3. Inspecciona `dataset_metadata.json` y `dataset_summary.json`

### "Quiero compilar el paper a PDF"
1. Consulta [paper/README.md](paper/README.md) - Instrucciones de compilación
2. Opción A: Compilar localmente (necesita pdflatex)
3. Opción B: Copiar a Overleaf y compilar online
4. Las figuras ya están generadas en [paper/figures/](paper/figures/)

---

## 📊 ESTADÍSTICAS RÁPIDAS

### Dataset Aspar-Synth-10K
- **Total Laps**: 500
- **Telemetry Samples**: 3,829,839 @ 100Hz
- **Video Frames**: 2,297,805 @ 4K 60FPS
- **Anomalies**: 27 (5.4%)
- **Lap Time**: 76.60 ± 3.15s

### Artículo Académico
- **Secciones**: 4-5 (completas)
- **Ecuaciones**: 11
- **Tablas**: 4
- **Figuras**: 7
- **Líneas de código**: 500+

### Documentación
- **Archivos**: 5 principales
- **Total de palabras**: 15,000+
- **Tablas**: 20+
- **Secciones**: 50+

---

## ✅ LISTA DE VERIFICACIÓN

### Para comenzar a experimentar:
- [ ] He leído [PROJECT_STATUS.md](PROJECT_STATUS.md)
- [ ] He entendido los 3 escenarios (A, B, C)
- [ ] He ubicado los datos en [data/aspar_synth_10k/](data/aspar_synth_10k/)
- [ ] He revisado las figuras en [paper/figures/](paper/figures/)
- [ ] He leído [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md)

### Para regenerar:
- [ ] He ejecutado `generate_aspar_synth_10k.py`
- [ ] He ejecutado `analyze_dataset.py --generate-plots`
- [ ] He ejecutado `generate_figures.py`
- [ ] He ejecutado `generate_validation_report.py`
- [ ] He verificado todos los outputs

### Para publicar:
- [ ] He compilado el paper a PDF (localmente o Overleaf)
- [ ] He incluido todas las figuras (ya están en [paper/figures/](paper/figures/))
- [ ] He revisado las referencias en references.bib
- [ ] He validado las hipótesis con datos reales

---

## 🔗 ENLACES RÁPIDOS

### Documentación
- [📊 PROJECT_STATUS.md](PROJECT_STATUS.md) - Estado actual
- [🎯 EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) - Cómo ejecutar
- [✅ VALIDATION_REPORT.txt](VALIDATION_REPORT.txt) - Estadísticas
- [📋 REGENERATION_SUMMARY.md](REGENERATION_SUMMARY.md) - Resumen

### Datos & Análisis
- [📁 Dataset](data/aspar_synth_10k/) - 500 laps
- [📊 Visualizaciones](data/aspar_synth_10k/visualizations/) - 4 plots
- [📈 Metadata](data/aspar_synth_10k/dataset_metadata.json) - Estructura

### Paper
- [📄 main.tex](paper/main.tex) - Artículo completo
- [🖼️ Figuras](paper/figures/) - 7 figuras científicas
- [📚 Referencias](paper/references.bib) - Bibliografía

### Scripts
- [🔧 generate_aspar_synth_10k.py](scripts/generate_aspar_synth_10k.py) - Dataset
- [📊 analyze_dataset.py](scripts/analyze_dataset.py) - Análisis
- [✅ generate_validation_report.py](scripts/generate_validation_report.py) - Reporte

---

## 📞 SOPORTE RÁPIDO

| Pregunta | Respuesta | Enlace |
|----------|-----------|--------|
| ¿Por dónde empiezo? | Lee PROJECT_STATUS | [Link](PROJECT_STATUS.md) |
| ¿Cómo regenero todo? | Sigue EXECUTION_GUIDE | [Link](EXECUTION_GUIDE.md) |
| ¿Cuáles son los resultados? | Consulta VALIDATION_REPORT | [Link](VALIDATION_REPORT.txt) |
| ¿Dónde está el dataset? | En data/aspar_synth_10k/ | [Link](data/aspar_synth_10k/) |
| ¿Dónde está el paper? | En paper/main.tex | [Link](paper/main.tex) |

---

## 🎓 INFORMACIÓN DE REFERENCIA

### Tecnologías Utilizadas
- Python 3.9+ (NumPy, Pandas, Matplotlib, Seaborn)
- LaTeX (IEEEtran, TikZ)
- JSON (serialización de datos)
- Git (control de versiones)

### Hardware Objetivo
- **Training**: NVIDIA RTX 4090 (FP32, server-side)
- **Inference**: NVIDIA Jetson AGX Orin (INT8, edge-side)

### Métricas de Validación
- **H1**: Latency < 50ms
- **H2**: F1-score > 80%
- **H3**: Power < 50W

---

## 📝 NOTAS FINALES

Este proyecto está **completamente documentado** y **listo para experimentación**.

Todos los componentes han sido regenerados:
- ✅ Dataset: 500 laps (3.8M samples)
- ✅ Análisis: Estadísticas completas
- ✅ Visualizaciones: 11 figuras
- ✅ Paper: Secciones 4-5 completas
- ✅ Documentación: 5 archivos principales

**Para cualquier pregunta**: Consulta el documento relevante en este índice.

---

**Última actualización**: 30 de Diciembre de 2025  
**Estado**: ✅ PRODUCCIÓN LISTA

🚀 **¡LISTO PARA EXPERIMENTAR!**
