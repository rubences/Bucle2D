# 🚀 Guía de Ejecución del Proyecto Bucle2D

## Overview

Este proyecto contiene:
- 📄 **Artículo académico** sobre Agentic-Racing-Vision (secciones 4-5: Validación Experimental)
- 📊 **Dataset sintético Aspar-Synth-10K** (500 laps generadas)
- 📈 **7 figuras científicas** (PDF + PNG)
- 📉 **Análisis estadístico** completo
- ✅ **Reporte de validación** de hipótesis

---

## 📋 Requisitos Previos

```bash
# Python 3.9+
python --version

# Dependencias (ya instaladas):
pip list | grep -E "numpy|pandas|matplotlib|seaborn"
```

### Paquetes Requeridos
```
numpy
pandas
matplotlib
seaborn
tqdm
```

---

## 🎮 Quick Start: Regenerar Todo en 5 Minutos

```bash
cd /workspaces/Bucle2D

# 1. Limpiar datos anteriores (opcional)
rm -rf data/aspar_synth_10k/*

# 2. Generar dataset (500 laps, ~2.5 min)
python scripts/generate_aspar_synth_10k.py --num-laps 500

# 3. Analizar y visualizar (1 min)
python scripts/analyze_dataset.py --generate-plots

# 4. Generar figuras para el paper (1 min)
python scripts/generate_figures.py

# 5. Crear reporte de validación (30 seg)
python scripts/generate_validation_report.py > VALIDATION_REPORT.txt
```

**Total**: ~5 minutos para todo

---

## 📊 Detalle de Scripts

### 1. Generador de Dataset: `generate_aspar_synth_10k.py`

**Uso Básico:**
```bash
# 100 laps (quick test)
python scripts/generate_aspar_synth_10k.py --num-laps 100

# 500 laps (standard)
python scripts/generate_aspar_synth_10k.py --num-laps 500

# 10,000 laps (full dataset, ~45 min)
python scripts/generate_aspar_synth_10k.py --num-laps 10000
```

**Salida:**
```
data/aspar_synth_10k/
├── dataset_metadata.json          # Metadata de todas las laps
├── dataset_summary.json           # Estadísticas agregadas
├── telemetry/
│   ├── lap_001-100.json          # Telemetría: 100Hz, 22 canales
│   ├── lap_101-200.json
│   └── ...
├── video_metadata/
│   ├── lap_001_video.json        # Metadata de video: 4K 60FPS
│   ├── lap_002_video.json
│   └── ...
```

**Formato de Datos:**
- **Telemetría**: 100Hz, 22 canales (velocidad, aceleración, temps, suspension, etc.)
- **Video**: 3840x2160 (4K), 60 FPS, H.265/HEVC

---

### 2. Análisis del Dataset: `analyze_dataset.py`

**Uso:**
```bash
# Solo estadísticas (console output)
python scripts/analyze_dataset.py

# Con visualizaciones (genera 4 PNG)
python scripts/analyze_dataset.py --generate-plots
```

**Salida:**
```
Console Output:
- Dataset Summary (total laps, samples, frames)
- Weather Distribution (sunny/cloudy/rain)
- Lap Time Statistics (mean, std, min, max)
- Anomaly Distribution (tipos y conteos)
- Telemetry Channels (descripción de 22 canales)

Visualizaciones (en data/aspar_synth_10k/visualizations/):
├── lap_time_distribution.png      # Histograma + desglose por clima
├── weather_impact.png             # Box plots
├── anomaly_distribution.png       # Barras por tipo/sector
└── telemetry_sample_lap1.png      # 6 subplots detallados
```

---

### 3. Generador de Figuras: `generate_figures.py`

**Uso:**
```bash
python scripts/generate_figures.py
```

**Salida (en paper/figures/):**
```
├── fig8_entropy_track_map.pdf     # Track entropy (CAG/RAG zones)
├── fig8_entropy_track_map.png
├── fig9_latency_density.pdf       # Latency PDF (bimodal)
├── fig9_latency_density.png
├── fig10_latency_comparison.pdf   # Bar chart (escenarios A, B, C)
├── fig10_latency_comparison.png
├── fig11_f1_comparison.pdf        # F1-scores
├── fig11_f1_comparison.png
├── fig12_confusion_matrix.pdf     # Matriz de confusión
├── fig12_confusion_matrix.png
├── fig13_agent_trace.pdf          # Agent orchestration (dual-axis)
├── fig13_agent_trace.png
├── fig14_power_trace.pdf          # Power profiling (dual-axis)
└── fig14_power_trace.png
```

---

### 4. Validación de Hipótesis: `generate_validation_report.py`

**Uso:**
```bash
python scripts/generate_validation_report.py
```

**Salida:**
```
VALIDATION_REPORT.txt (10 secciones):

1. Dataset Overview
2. Weather Conditions Analysis
3. Anomaly Injection Analysis
4. Telemetry Specifications
5. Video Specifications
6. Lap Time Statistics
7. Circuit Sectors
8. Test Scenarios Mapping (A, B, C)
9. Data Availability
10. Hypothesis Validation Status (H1, H2, H3)
```

---

## 🧪 Escenarios de Prueba

### Escenario A: Qualifying Lap (H1 - Latency Optimization)
```bash
# 264 sunny laps disponibles
# Métrica: ≥40% latencia reduction con CAG
# Target: L_total < 50ms
```

### Escenario B: Mechanical Stress (H2 - Diagnostic Precision)
```bash
# 27 laps con anomalías (5 tipos)
# Métrica: >15% F1-score improvement con RAG
# Target: Detección superior de fallos
```

### Escenario C: Environmental Shift (H3 - Energy Viability)
```bash
# 94 laps con variación de clima
# Métrica: 35% reducción energética vs Always-On RAG
# Target: <50W thermal envelope
```

---

## 📈 Estadísticas del Dataset Actual

```
Total Laps:                500
Telemetry Samples:         3,829,839 @ 100Hz
Video Frames:              2,297,805 @ 60FPS 4K
Anomalies Injected:        27 (5.4%)

Weather Distribution:
  ☀️  Sunny:      264 laps (52.8%)  [74.92 ± 1.52s]
  ☁️  Cloudy:     142 laps (28.4%)  [76.57 ± 1.48s]
  🌧️  Light Rain: 73 laps  (14.6%)  [79.66 ± 1.31s]
  ⛈️  Heavy Rain: 21 laps  (4.2%)   [87.33 ± 1.54s]

Circuit:                   Aspar Circuit, Valencia (3.2 km, 8 sectors)
Lap Time Average:          76.60 ± 3.15 seconds
```

---

## 🔧 Customización

### Generar Dataset Más Grande

```bash
# 1,000 laps (10 min)
python scripts/generate_aspar_synth_10k.py --num-laps 1000

# 5,000 laps (50 min)
python scripts/generate_aspar_synth_10k.py --num-laps 5000

# 10,000 laps (full, 90 min)
python scripts/generate_aspar_synth_10k.py --num-laps 10000
```

### Modificar Parámetros de Generación

Editar `scripts/generate_aspar_synth_10k.py`:
- `ANOMALY_INJECTION_RATE`: Cambiar % de anomalías (default: 0.05 = 5%)
- `WEATHER_WEIGHTS`: Modificar distribución de clima
- `ANOMALY_TYPES`: Agregar nuevos tipos de anomalías

---

## 📄 Artículo Académico

**Archivo**: `paper/main.tex`

**Secciones Principales:**
- **Section 4**: Experimental Validation
  - 4.1 Hypotheses (H1, H2, H3)
  - 4.2 Experimental Setup (Hardware specs)
  - 4.3 Evaluation Metrics
  - 4.4 Test Scenarios

- **Section 5**: Results and Analysis
  - 5.1 Scenario A Results (Qualifying)
  - 5.2 Scenario B Results (Anomalies)
  - 5.3 Scenario C Results (Environmental)

**11 Ecuaciones Matemáticas**
**4 Tablas de Datos**
**7 Referencias de Figuras** (ya generadas)

### Compilar a PDF (requiere LaTeX local)

```bash
# Opción 1: Usar pdflatex (si está instalado)
cd paper
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex  # 2da pasada

# Opción 2: Usar Overleaf (recomendado)
1. Copiar contenido de main.tex a Overleaf
2. Subir figuras (figures/*.pdf)
3. Compilar online

# Opción 3: Usar TeXLive/MiKTeX local
# (Ver instalación en tu sistema operativo)
```

---

## ✅ Verificación de Éxito

```bash
# 1. Verificar dataset generado
ls -lh data/aspar_synth_10k/dataset_metadata.json
# Esperado: archivo > 1MB

# 2. Verificar figuras creadas
ls -lh paper/figures/
# Esperado: 14 archivos (7 PDF + 7 PNG)

# 3. Verificar análisis completado
ls -lh data/aspar_synth_10k/visualizations/
# Esperado: 4 PNG files

# 4. Verificar reporte de validación
cat VALIDATION_REPORT.txt | head -20
# Esperado: 10 secciones de análisis
```

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'seaborn'`
```bash
pip install seaborn -q
```

### Error: `FileNotFoundError: data/aspar_synth_10k/dataset_metadata.json`
```bash
# Primero generar dataset
python scripts/generate_aspar_synth_10k.py --num-laps 100
```

### Problema: Los gráficos no se ven
```bash
# Verificar que matplotlib está configurado correctamente
python -c "import matplotlib; matplotlib.use('Agg'); print('OK')"
```

### Lentitud en generación grande
```bash
# Usar subset más pequeño para testing
python scripts/generate_aspar_synth_10k.py --num-laps 10
```

---

## 📊 Pipeline Completo

```
┌─────────────────────────────────┐
│   1. GENERATE DATASET           │
│  (generate_aspar_synth_10k.py)  │
│   500 laps, 3.8M samples        │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   2. ANALYZE DATASET            │
│    (analyze_dataset.py)         │
│   Statistics + 4 plots          │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   3. GENERATE FIGURES           │
│   (generate_figures.py)         │
│   7 scientific figures          │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   4. VALIDATION REPORT          │
│ (generate_validation_report.py) │
│   10-section analysis           │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   5. COMPILE PAPER (OPTIONAL)   │
│   (main.tex → main.pdf)         │
│   Complete academic paper       │
└─────────────────────────────────┘
```

---

## 📚 Referencias

- **Dataset**: 500 laps en circuito Aspar (Valencia, España)
- **Telemetría**: 100Hz, 22 canales (inspirado en Assetto Corsa Pro)
- **Anomalías**: 5 tipos (tire blistering, electrical glitch, suspension chatter, brake fade, oil debris)
- **Clima**: 4 condiciones (sunny, cloudy, light rain, heavy rain)

---

## 🎯 Próximas Fases Sugeridas

1. **Ejecutar Experimentos** usando H1, H2, H3 validation
2. **Comparar CAG vs RAG** en los 3 escenarios
3. **Medir Latencia** (L_detect, L_classify, L_plan, L_execute)
4. **Evaluar F1-scores** en detección de anomalías
5. **Perfilar Energía** en Jetson Orin (watts, térmica)

---

## ❓ Soporte

- **Paper**: Refer to `paper/main.tex` sections 4-5
- **Data**: Refer to `data/aspar_synth_10k/README.md`
- **Validation**: Read `VALIDATION_REPORT.txt`
- **Summary**: Check `EXECUTIVE_SUMMARY.md`

---

**¡Listo para experimentación!** 🚀
