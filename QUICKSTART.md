# ⚡ QUICK START - Bucle2D

**Estado**: ✅ LISTO | **Fecha**: 30 Dic 2025 | **Time**: ~5 min para todo

---

## 🎯 En 30 Segundos

**Bucle2D** = Proyecto académico con **dataset sintético** (500 laps), **análisis estadístico** completo, **7 figuras científicas** y **paper con 2 secciones completas**.

**¿Qué queda por hacer?** Compilar PDF (necesita pdflatex local) + ejecutar experimentos de latencia/diagnóstico/energía.

---

## 📂 3 Archivos Principales

| Archivo | Propósito | Lectura |
|---------|-----------|---------|
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | ¿Qué se hizo? + Estadísticas | 10 min |
| [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) | ¿Cómo reproducir? | 15 min |
| [VALIDATION_REPORT.txt](VALIDATION_REPORT.txt) | Detalles del dataset | 10 min |

---

## 🚀 Regenerar Todo (5 min)

```bash
cd /workspaces/Bucle2D

# 1. Dataset
python scripts/generate_aspar_synth_10k.py --num-laps 500  # 2m24s

# 2. Análisis
python scripts/analyze_dataset.py --generate-plots          # 1m

# 3. Figuras
python scripts/generate_figures.py                          # 1m

# 4. Reporte
python scripts/generate_validation_report.py                # 30s
```

---

## 📊 Lo Que Existe

```
✅ 500 laps con 3.8M telemetry samples
✅ 7 figuras científicas (PDF + PNG)
✅ Paper: Secciones 4-5 completas
✅ 4 visualizaciones de análisis
✅ 3 hipótesis documentadas (H1, H2, H3)
✅ Documentación exhaustiva
```

---

## 🧪 3 Escenarios Listos

| Escenario | Datos | Test |
|-----------|-------|------|
| **A** - Qualifying | 264 sunny laps | ≥40% latency ↓ |
| **B** - Anomalies | 27 faulty laps | >15% F1 ↑ |
| **C** - Weather | 94 rain laps | 35% energy ↓ |

---

## 📁 Ubicaciones Clave

| Qué | Dónde |
|-----|-------|
| Dataset | `/data/aspar_synth_10k/` |
| Figuras | `/paper/figures/` |
| Paper | `/paper/main.tex` |
| Análisis | `/scripts/analyze_dataset.py` |
| Docs | `INDEX.md` (navegación) |

---

## ✅ Checklist Rápido

- [ ] He visto [PROJECT_STATUS.md](PROJECT_STATUS.md)
- [ ] Conozco los 3 escenarios (A, B, C)
- [ ] Sé cómo regenerar (arriba)
- [ ] Sé dónde está el dataset

✔️ **Listo para experimentar**

---

**→ Lee [INDEX.md](INDEX.md) para más detalles**
