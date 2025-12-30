# Aspar-Synth-10K Dataset

## Overview

**Aspar-Synth-10K** is a high-fidelity synthetic motorsport dataset designed for AI research in racing perception and telemetry analysis. The dataset simulates 10,000 racing laps on the Aspar Circuit (Valencia, Spain) with realistic physics based on Assetto Corsa Pro simulation engine.

### Key Features

- ✅ **10,000 racing laps** with complete telemetry
- ✅ **100Hz synchronized telemetry** (speed, acceleration, lean angle, suspension, temperatures, etc.)
- ✅ **4K video metadata** (3840x2160 @ 60 FPS)
- ✅ **Stochastic weather variations** (sunny, cloudy, light rain, heavy rain)
- ✅ **Mechanical anomaly injection** for testing diagnostic algorithms
- ✅ **High Sim-to-Real fidelity** inspired by Assetto Corsa Pro physics

---

## Dataset Structure

```
aspar_synth_10k/
├── dataset_metadata.json           # Complete dataset metadata
├── summaries/
│   └── dataset_summary.json        # Statistical summary
├── telemetry/
│   ├── telemetry_chunk_0000.json   # Laps 1-100
│   ├── telemetry_chunk_0001.json   # Laps 101-200
│   └── ...                         # (100 chunks total)
└── video_metadata/
    ├── video_lap_00001.json        # Video metadata for lap 1
    ├── video_lap_00002.json        # Video metadata for lap 2
    └── ...                         # (10,000 files total)
```

---

## Circuit Specification

### Aspar Circuit (Valencia, Spain)

| Property | Value |
|----------|-------|
| **Name** | Aspar Circuit |
| **Location** | Valencia, Spain |
| **Length** | 3.2 km |
| **Sectors** | 8 |
| **Track Type** | Mixed (straights + technical corners) |

### Sector Details

| Sector | Name | Length (m) | Avg Speed (km/h) | Max Lean Angle (°) | Type |
|--------|------|------------|------------------|-------------------|------|
| 1 | Main Straight | 600 | 240 | 5 | Straight |
| 2 | Turn 1 Braking | 180 | 95 | 45 | Heavy Braking |
| 3 | Turn 2 Apex | 220 | 120 | 62 | Technical |
| 4 | Turn 4 Banking | 450 | 210 | 48 | Fast Corner |
| 5 | Secondary Straight | 500 | 230 | 8 | Straight |
| 6 | Turn 6 Tight | 150 | 85 | 64 | Hairpin |
| 7 | Turn 8 Banking | 400 | 190 | 50 | Fast Corner |
| 8 | Final Straight | 700 | 260 | 3 | Straight |

---

## Telemetry Specification

### Sampling Rate
- **Frequency**: 100 Hz (10ms intervals)
- **Average samples per lap**: ~7,600 data points

### Telemetry Channels (22 channels)

| Channel | Unit | Description |
|---------|------|-------------|
| `timestamp` | seconds | Time since lap start |
| `distance_m` | meters | Distance traveled in lap |
| `sector_id` | int [1-8] | Current sector |
| `speed_kmh` | km/h | Vehicle speed |
| `speed_ms` | m/s | Vehicle speed |
| `lean_angle_deg` | degrees | Motorcycle lean angle |
| `accel_long_g` | G | Longitudinal acceleration |
| `accel_lat_g` | G | Lateral acceleration |
| `throttle_pct` | % [0-100] | Throttle position |
| `brake_pct` | % [0-100] | Brake pressure |
| `rpm` | RPM | Engine revolutions per minute |
| `tire_temp_fl_c` | °C | Front-left tire temperature |
| `tire_temp_fr_c` | °C | Front-right tire temperature |
| `tire_temp_rl_c` | °C | Rear-left tire temperature |
| `tire_temp_rr_c` | °C | Rear-right tire temperature |
| `suspension_fl_mm` | mm | Front-left suspension travel |
| `suspension_fr_mm` | mm | Front-right suspension travel |
| `suspension_rl_mm` | mm | Rear-left suspension travel |
| `suspension_rr_mm` | mm | Rear-right suspension travel |
| `gps_lat` | degrees | GPS latitude |
| `gps_lon` | degrees | GPS longitude |

---

## Video Metadata

Each lap includes video metadata (actual video files not included due to storage constraints):

| Property | Value |
|----------|-------|
| **Resolution** | 3840x2160 (4K UHD) |
| **Frame Rate** | 60 FPS |
| **Codec** | H.265/HEVC |
| **Bitrate** | 50 Mbps |
| **Avg Duration** | ~76 seconds per lap |
| **Avg Frames** | ~4,560 frames per lap |

---

## Weather Conditions

Stochastic weather variations based on realistic probabilities:

| Weather | Probability | Lap Time Impact |
|---------|-------------|-----------------|
| **Sunny** | 50% | Baseline (0s penalty) |
| **Cloudy** | 30% | +1.5s penalty |
| **Light Rain** | 15% | +5.0s penalty |
| **Heavy Rain** | 5% | +12.0s penalty |

---

## Anomaly Injection

### Injection Rate
- **Probability**: 5% of laps contain anomalies
- **Expected anomalies**: ~500 laps (out of 10,000)

### Anomaly Types

| Type | Description | Telemetry Signature |
|------|-------------|---------------------|
| `suspension_chatter` | High-frequency oscillations (15-20 Hz) | Suspension travel spikes |
| `tire_blistering` | Overheating tires | Elevated tire temperatures (>120°C) |
| `brake_fade` | Reduced braking performance | Lower brake efficiency |
| `oil_debris` | Slippery track section | Reduced grip, lower speeds |
| `electrical_glitch` | Sensor noise/dropout | Missing or corrupted samples |

---

## Dataset Statistics (Full 10K)

### Expected Statistics for Full Dataset

| Metric | Value |
|--------|-------|
| **Total Laps** | 10,000 |
| **Total Telemetry Samples** | ~76,000,000 (76M samples) |
| **Total Video Frames** | ~45,600,000 (45.6M frames) |
| **Avg Lap Time** | 76.4 seconds |
| **Lap Time Range** | 71-89 seconds |
| **Total Duration** | ~212 hours of racing |
| **Storage Size (Telemetry)** | ~15 GB (JSON format) |
| **Storage Size (Video Metadata)** | ~200 MB |

---

## Usage Examples

### 1. Load Dataset Metadata

```python
import json

# Load complete dataset metadata
with open('data/aspar_synth_10k/dataset_metadata.json') as f:
    metadata = json.load(f)

print(f"Total laps: {metadata['total_laps']}")
print(f"Circuit: {metadata['circuit']['name']}")
```

### 2. Access Telemetry Data

```python
import json

# Load telemetry chunk (laps 1-100)
with open('data/aspar_synth_10k/telemetry/telemetry_chunk_0000.json') as f:
    telemetry = json.load(f)

# Access specific lap data
lap_data = telemetry['data_points']
print(f"Telemetry samples: {len(lap_data)}")

# Analyze speed profile
speeds = [point['speed_kmh'] for point in lap_data]
print(f"Max speed: {max(speeds):.1f} km/h")
```

### 3. Filter Anomalies

```python
import json
import pandas as pd

with open('data/aspar_synth_10k/dataset_metadata.json') as f:
    metadata = json.load(f)

laps_df = pd.DataFrame(metadata['laps'])

# Get all laps with suspension anomalies
suspension_anomalies = laps_df[
    (laps_df['has_anomaly'] == True) & 
    (laps_df['anomaly_type'] == 'suspension_chatter')
]

print(f"Suspension chatter cases: {len(suspension_anomalies)}")
print(suspension_anomalies[['lap_id', 'weather', 'anomaly_sector']])
```

### 4. Weather Analysis

```python
import json
import pandas as pd

with open('data/aspar_synth_10k/dataset_metadata.json') as f:
    metadata = json.load(f)

laps_df = pd.DataFrame(metadata['laps'])

# Analyze lap times by weather
weather_stats = laps_df.groupby('weather')['lap_time_s'].agg(['mean', 'std', 'min', 'max'])
print(weather_stats)
```

---

## Generation

### Quick Test (100 laps)

```bash
python scripts/generate_aspar_synth_10k.py --quick-test
```

### Full Dataset (10,000 laps)

```bash
python scripts/generate_aspar_synth_10k.py --num-laps 10000
```

**Note**: Full generation takes approximately 45-60 minutes on standard hardware.

### Custom Configuration

```bash
python scripts/generate_aspar_synth_10k.py \
    --num-laps 5000 \
    --output-dir /path/to/custom/dir \
    --seed 123
```

---

## Data Format

### Telemetry Chunk Format

```json
{
  "lap_id": 1,
  "data_points": [
    {
      "timestamp": 0.000,
      "distance_m": 0.0,
      "sector_id": 1,
      "speed_kmh": 240.3,
      "speed_ms": 66.75,
      "lean_angle_deg": 3.2,
      "accel_long_g": 0.15,
      "accel_lat_g": 0.05,
      "throttle_pct": 98.5,
      "brake_pct": 0.0,
      "rpm": 12450,
      "tire_temp_fl_c": 102.3,
      "tire_temp_fr_c": 103.1,
      "tire_temp_rl_c": 98.7,
      "tire_temp_rr_c": 99.4,
      "suspension_fl_mm": 45.2,
      "suspension_fr_mm": 46.8,
      "suspension_rl_mm": 52.1,
      "suspension_rr_mm": 51.3,
      "gps_lat": 39.489901,
      "gps_lon": -0.376301
    },
    ...
  ]
}
```

### Video Metadata Format

```json
{
  "lap_id": 1,
  "resolution": "3840x2160",
  "fps": 60,
  "duration_s": 76.42,
  "total_frames": 4585,
  "codec": "H.265/HEVC",
  "bitrate_mbps": 50,
  "filename": "aspar_lap_00001.mp4",
  "file_size_mb": 477,
  "checksum": "a3d5e8f2c1b9..."
}
```

---

## Applications

This dataset is designed for research in:

1. **Real-time Perception Systems**
   - Vision encoder training and validation
   - Sensor fusion algorithms
   - Edge computing inference

2. **Anomaly Detection**
   - Mechanical failure prediction
   - Diagnostic systems
   - Predictive maintenance

3. **Hybrid RAG-CAG Architectures**
   - Cache vs retrieval decision-making
   - Latency-accuracy trade-offs
   - Energy-efficient inference

4. **Motorsport AI**
   - Lap time prediction
   - Optimal racing line computation
   - Driver assistance systems

5. **MotoE / Electric Racing**
   - Energy efficiency analysis
   - Thermal management strategies
   - Battery constraint optimization

---

## Validation

The dataset has been designed to match the validation scenarios described in the paper:

- **Scenario A (Qualifying Lap)**: Clean laps without anomalies
- **Scenario B (Mechanical Stress)**: Laps with suspension/brake failures
- **Scenario C (Environmental Shift)**: Laps with changing weather conditions

---

## Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{aspar_synth_10k_2025,
  title={Aspar-Synth-10K: A High-Fidelity Synthetic Motorsport Dataset},
  author={[Your Name]},
  year={2025},
  publisher={GitHub},
  url={https://github.com/rubences/Bucle2D}
}
```

---

## License

This dataset is released under the MIT License. See LICENSE.txt for details.

---

## Acknowledgments

- **Physics Engine**: Inspired by Assetto Corsa Pro simulation
- **Circuit**: Based on Aspar Circuit layout (Valencia, Spain)
- **Framework**: Generated using Python with NumPy, Pandas, and custom simulation code

---

## Contact

For questions, issues, or contributions:
- **GitHub**: [github.com/rubences/Bucle2D](https://github.com/rubences/Bucle2D)
- **Issues**: [github.com/rubences/Bucle2D/issues](https://github.com/rubences/Bucle2D/issues)

---

**Dataset Version**: 1.0.0  
**Last Updated**: December 30, 2025
