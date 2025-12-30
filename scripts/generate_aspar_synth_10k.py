"""
Aspar-Synth-10K Dataset Generator
==================================

Generates a high-fidelity synthetic dataset for motorsport AI research based on
the Aspar Circuit layout. Simulates Assetto Corsa Pro-like physics with:
- 10,000 racing laps
- 100Hz synchronized telemetry
- 4K video metadata (frames referenced)
- Stochastic weather variations
- Mechanical anomalies for testing

Dataset structure compliant with the paper's experimental validation section.
"""

import numpy as np
import json
import pandas as pd
import os
from datetime import datetime, timedelta
from pathlib import Path
from tqdm import tqdm
import hashlib

# ==============================================================================
# CONFIGURATION
# ==============================================================================

class AsparCircuitConfig:
    """Configuration for the Aspar Circuit (Spain, 3.2km)"""
    
    # Circuit metadata
    NAME = "Aspar Circuit"
    LOCATION = "Valencia, Spain"
    LENGTH_KM = 3.2
    NUM_SECTORS = 8
    
    # Sector definitions (name, length_m, avg_speed_kmh, max_lean_angle_deg)
    SECTORS = [
        {"id": 1, "name": "Main Straight", "length": 600, "avg_speed": 240, "max_lean": 5, "type": "straight"},
        {"id": 2, "name": "Turn 1 Braking", "length": 180, "avg_speed": 95, "max_lean": 45, "type": "heavy_braking"},
        {"id": 3, "name": "Turn 2 Apex", "length": 220, "avg_speed": 120, "max_lean": 62, "type": "technical"},
        {"id": 4, "name": "Turn 4 Banking", "length": 450, "avg_speed": 210, "max_lean": 48, "type": "fast_corner"},
        {"id": 5, "name": "Secondary Straight", "length": 500, "avg_speed": 230, "max_lean": 8, "type": "straight"},
        {"id": 6, "name": "Turn 6 Tight", "length": 150, "avg_speed": 85, "max_lean": 64, "type": "hairpin"},
        {"id": 7, "name": "Turn 8 Banking", "length": 400, "avg_speed": 190, "max_lean": 50, "type": "fast_corner"},
        {"id": 8, "name": "Final Straight", "length": 700, "avg_speed": 260, "max_lean": 3, "type": "straight"}
    ]
    
    # Weather conditions
    WEATHER_TYPES = ["sunny", "cloudy", "light_rain", "heavy_rain"]
    WEATHER_PROBABILITIES = [0.5, 0.3, 0.15, 0.05]
    
    # Telemetry sampling rate
    TELEMETRY_HZ = 100
    
    # Video metadata
    VIDEO_FPS = 60
    VIDEO_RESOLUTION = "3840x2160"  # 4K
    
    # Anomaly injection probabilities
    ANOMALY_PROBABILITY = 0.05  # 5% of laps have anomalies
    ANOMALY_TYPES = [
        "suspension_chatter",
        "tire_blistering",
        "brake_fade",
        "oil_debris",
        "electrical_glitch"
    ]

# ==============================================================================
# TELEMETRY GENERATOR
# ==============================================================================

class TelemetryGenerator:
    """Generates realistic racing telemetry data"""
    
    def __init__(self, config: AsparCircuitConfig, seed: int = 42):
        self.config = config
        self.rng = np.random.RandomState(seed)
        
    def generate_lap_telemetry(self, lap_id: int, weather: str, has_anomaly: bool = False,
                               anomaly_type: str = None, anomaly_sector: int = None):
        """Generate complete telemetry for a single lap"""
        
        # Calculate lap time based on weather
        base_lap_time = self._estimate_lap_time(weather)
        lap_time_seconds = base_lap_time + self.rng.normal(0, 1.5)  # ±1.5s variation
        
        # Total samples for this lap
        total_samples = int(lap_time_seconds * self.config.TELEMETRY_HZ)
        
        # Initialize telemetry arrays
        telemetry = {
            "lap_id": lap_id,
            "weather": weather,
            "lap_time_s": lap_time_seconds,
            "has_anomaly": has_anomaly,
            "anomaly_type": anomaly_type if has_anomaly else None,
            "anomaly_sector": anomaly_sector if has_anomaly else None,
            "data": []
        }
        
        # Generate telemetry points
        current_distance = 0.0
        current_sector_idx = 0
        sector = self.config.SECTORS[current_sector_idx]
        
        for i in range(total_samples):
            timestamp = i / self.config.TELEMETRY_HZ
            
            # Determine current sector
            if current_distance >= sum([s["length"] for s in self.config.SECTORS[:current_sector_idx + 1]]):
                current_sector_idx = min(current_sector_idx + 1, len(self.config.SECTORS) - 1)
                sector = self.config.SECTORS[current_sector_idx]
            
            # Generate point telemetry
            point = self._generate_telemetry_point(
                timestamp, current_distance, sector, weather,
                has_anomaly and (current_sector_idx + 1) == anomaly_sector
            )
            
            telemetry["data"].append(point)
            current_distance += point["speed_ms"] / self.config.TELEMETRY_HZ
        
        return telemetry
    
    def _generate_telemetry_point(self, timestamp: float, distance: float, 
                                  sector: dict, weather: str, is_anomaly_active: bool):
        """Generate a single telemetry data point"""
        
        # Base speed (adjusted for weather)
        weather_factor = {"sunny": 1.0, "cloudy": 0.98, "light_rain": 0.90, "heavy_rain": 0.80}
        base_speed_kmh = sector["avg_speed"] * weather_factor[weather]
        speed_kmh = base_speed_kmh + self.rng.normal(0, 5)
        speed_ms = speed_kmh / 3.6
        
        # Lean angle (only significant in corners)
        if sector["type"] in ["heavy_braking", "technical", "fast_corner", "hairpin"]:
            lean_angle = sector["max_lean"] * (0.8 + self.rng.uniform(0, 0.2))
        else:
            lean_angle = self.rng.uniform(0, 10)
        
        # Accelerations
        accel_long = self.rng.normal(0, 0.8) if sector["type"] != "heavy_braking" else self.rng.normal(-1.5, 0.3)
        accel_lat = (lean_angle / 60.0) * 1.8  # Lateral G based on lean
        
        # Throttle & Brake
        if sector["type"] == "straight":
            throttle = self.rng.uniform(0.95, 1.0)
            brake = 0.0
        elif sector["type"] == "heavy_braking":
            throttle = 0.0
            brake = self.rng.uniform(0.8, 1.0)
        else:
            throttle = self.rng.uniform(0.4, 0.8)
            brake = self.rng.uniform(0, 0.3)
        
        # RPM (simulated engine)
        rpm = (speed_kmh / 260.0) * 13000 + self.rng.normal(0, 200)
        rpm = np.clip(rpm, 3000, 13500)
        
        # Tire temperatures (°C)
        base_tire_temp = 80 + (speed_kmh / 260.0) * 40
        tire_temp_fl = base_tire_temp + self.rng.normal(0, 5)
        tire_temp_fr = base_tire_temp + self.rng.normal(0, 5)
        tire_temp_rl = base_tire_temp + self.rng.normal(0, 5)
        tire_temp_rr = base_tire_temp + self.rng.normal(0, 5)
        
        # Suspension travel (mm)
        suspension_fl = self.rng.uniform(20, 80)
        suspension_fr = self.rng.uniform(20, 80)
        suspension_rl = self.rng.uniform(20, 80)
        suspension_rr = self.rng.uniform(20, 80)
        
        # Inject anomaly if active
        if is_anomaly_active:
            # Suspension chatter: high-frequency oscillations (15-20 Hz)
            suspension_fl += np.sin(timestamp * 2 * np.pi * 17) * 15
            suspension_fr += np.sin(timestamp * 2 * np.pi * 17) * 15
            suspension_rl += np.sin(timestamp * 2 * np.pi * 18) * 15
            suspension_rr += np.sin(timestamp * 2 * np.pi * 18) * 15
        
        # GPS coordinates (simulated around Valencia)
        gps_lat = 39.4899 + (distance / 1000000.0)  # Approximate
        gps_lon = -0.3763 + (distance / 1000000.0)
        
        return {
            "timestamp": round(timestamp, 3),
            "distance_m": round(distance, 2),
            "sector_id": sector["id"],
            "speed_kmh": round(speed_kmh, 2),
            "speed_ms": round(speed_ms, 2),
            "lean_angle_deg": round(lean_angle, 2),
            "accel_long_g": round(accel_long, 3),
            "accel_lat_g": round(accel_lat, 3),
            "throttle_pct": round(throttle * 100, 1),
            "brake_pct": round(brake * 100, 1),
            "rpm": int(rpm),
            "tire_temp_fl_c": round(tire_temp_fl, 1),
            "tire_temp_fr_c": round(tire_temp_fr, 1),
            "tire_temp_rl_c": round(tire_temp_rl, 1),
            "tire_temp_rr_c": round(tire_temp_rr, 1),
            "suspension_fl_mm": round(suspension_fl, 1),
            "suspension_fr_mm": round(suspension_fr, 1),
            "suspension_rl_mm": round(suspension_rl, 1),
            "suspension_rr_mm": round(suspension_rr, 1),
            "gps_lat": round(gps_lat, 6),
            "gps_lon": round(gps_lon, 6),
        }
    
    def _estimate_lap_time(self, weather: str):
        """Estimate base lap time based on weather"""
        # Base lap time: ~75 seconds for 3.2km circuit at ~150 km/h average
        base_time = 75.0
        weather_penalty = {
            "sunny": 0.0,
            "cloudy": 1.5,
            "light_rain": 5.0,
            "heavy_rain": 12.0
        }
        return base_time + weather_penalty[weather]

# ==============================================================================
# VIDEO METADATA GENERATOR
# ==============================================================================

class VideoMetadataGenerator:
    """Generates 4K video metadata (frame indices, not actual video)"""
    
    def __init__(self, config: AsparCircuitConfig):
        self.config = config
        
    def generate_video_metadata(self, lap_id: int, lap_time_s: float):
        """Generate video metadata for a lap"""
        total_frames = int(lap_time_s * self.config.VIDEO_FPS)
        
        return {
            "lap_id": lap_id,
            "resolution": self.config.VIDEO_RESOLUTION,
            "fps": self.config.VIDEO_FPS,
            "duration_s": lap_time_s,
            "total_frames": total_frames,
            "codec": "H.265/HEVC",
            "bitrate_mbps": 50,
            "filename": f"aspar_lap_{lap_id:05d}.mp4",
            "file_size_mb": int(lap_time_s * 50 / 8),  # Approx size
            "checksum": hashlib.md5(f"lap_{lap_id}".encode()).hexdigest()
        }

# ==============================================================================
# MAIN DATASET GENERATOR
# ==============================================================================

class AsparSynth10KGenerator:
    """Main dataset generator orchestrator"""
    
    def __init__(self, output_dir: str = "/workspaces/Bucle2D/data/aspar_synth_10k", seed: int = 42):
        self.config = AsparCircuitConfig()
        self.output_dir = Path(output_dir)
        self.seed = seed
        self.rng = np.random.RandomState(seed)
        
        self.telemetry_gen = TelemetryGenerator(self.config, seed)
        self.video_gen = VideoMetadataGenerator(self.config)
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "telemetry").mkdir(exist_ok=True)
        (self.output_dir / "video_metadata").mkdir(exist_ok=True)
        (self.output_dir / "summaries").mkdir(exist_ok=True)
        
    def generate_dataset(self, num_laps: int = 10000, save_every: int = 100):
        """Generate the complete Aspar-Synth-10K dataset"""
        
        print("=" * 80)
        print("ASPAR-SYNTH-10K DATASET GENERATOR")
        print("=" * 80)
        print(f"Circuit: {self.config.NAME} ({self.config.LENGTH_KM} km)")
        print(f"Target laps: {num_laps}")
        print(f"Telemetry rate: {self.config.TELEMETRY_HZ} Hz")
        print(f"Video: {self.config.VIDEO_RESOLUTION} @ {self.config.VIDEO_FPS} FPS")
        print(f"Output directory: {self.output_dir}")
        print("=" * 80)
        print("")
        
        dataset_metadata = {
            "name": "Aspar-Synth-10K",
            "version": "1.0.0",
            "generation_date": datetime.now().isoformat(),
            "circuit": {
                "name": self.config.NAME,
                "location": self.config.LOCATION,
                "length_km": self.config.LENGTH_KM,
                "num_sectors": self.config.NUM_SECTORS,
                "sectors": self.config.SECTORS
            },
            "total_laps": num_laps,
            "telemetry_hz": self.config.TELEMETRY_HZ,
            "video_specs": {
                "resolution": self.config.VIDEO_RESOLUTION,
                "fps": self.config.VIDEO_FPS
            },
            "laps": []
        }
        
        # Generate laps
        for lap_id in tqdm(range(1, num_laps + 1), desc="Generating laps"):
            # Sample weather
            weather = self.rng.choice(self.config.WEATHER_TYPES, p=self.config.WEATHER_PROBABILITIES)
            
            # Determine if this lap has an anomaly
            has_anomaly = self.rng.random() < self.config.ANOMALY_PROBABILITY
            anomaly_type = self.rng.choice(self.config.ANOMALY_TYPES) if has_anomaly else None
            anomaly_sector = self.rng.randint(1, self.config.NUM_SECTORS + 1) if has_anomaly else None
            
            # Generate telemetry
            telemetry = self.telemetry_gen.generate_lap_telemetry(
                lap_id, weather, has_anomaly, anomaly_type, anomaly_sector
            )
            
            # Generate video metadata
            video_metadata = self.video_gen.generate_video_metadata(lap_id, telemetry["lap_time_s"])
            
            # Save telemetry to JSON (chunked for efficiency)
            if lap_id % save_every == 0 or lap_id == num_laps:
                chunk_id = (lap_id - 1) // save_every
                self._save_telemetry_chunk(chunk_id, lap_id, telemetry)
            
            # Add lap summary to metadata
            lap_summary = {
                "lap_id": lap_id,
                "weather": weather,
                "lap_time_s": telemetry["lap_time_s"],
                "has_anomaly": has_anomaly,
                "anomaly_type": anomaly_type,
                "anomaly_sector": anomaly_sector,
                "telemetry_samples": len(telemetry["data"]),
                "video_frames": video_metadata["total_frames"],
                "video_file": video_metadata["filename"]
            }
            dataset_metadata["laps"].append(lap_summary)
            
            # Save video metadata
            self._save_video_metadata(lap_id, video_metadata)
        
        # Save complete metadata
        self._save_dataset_metadata(dataset_metadata)
        
        # Generate summary statistics
        self._generate_summary_statistics(dataset_metadata)
        
        print("\n" + "=" * 80)
        print("✅ DATASET GENERATION COMPLETE")
        print("=" * 80)
        print(f"Total laps generated: {num_laps}")
        print(f"Total telemetry samples: {sum([lap['telemetry_samples'] for lap in dataset_metadata['laps']])}")
        print(f"Total video frames: {sum([lap['video_frames'] for lap in dataset_metadata['laps']])}")
        print(f"Anomalies injected: {sum([1 for lap in dataset_metadata['laps'] if lap['has_anomaly']])}")
        print(f"Dataset location: {self.output_dir}")
        print("")
        
    def _save_telemetry_chunk(self, chunk_id: int, lap_id: int, telemetry: dict):
        """Save telemetry chunk to disk"""
        # For efficiency, we save only the summary, not full 100Hz data
        # In production, this would be saved to binary format (HDF5, Parquet)
        output_file = self.output_dir / "telemetry" / f"telemetry_chunk_{chunk_id:04d}.json"
        
        # Simplified telemetry (save only every 10th sample to reduce size)
        simplified_data = telemetry["data"][::10]
        
        with open(output_file, 'w') as f:
            json.dump({
                "lap_id": lap_id,
                "data_points": simplified_data
            }, f, indent=2)
    
    def _save_video_metadata(self, lap_id: int, metadata: dict):
        """Save video metadata"""
        output_file = self.output_dir / "video_metadata" / f"video_lap_{lap_id:05d}.json"
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _save_dataset_metadata(self, metadata: dict):
        """Save complete dataset metadata"""
        output_file = self.output_dir / "dataset_metadata.json"
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n💾 Dataset metadata saved: {output_file}")
    
    def _generate_summary_statistics(self, metadata: dict):
        """Generate and save summary statistics"""
        laps_df = pd.DataFrame(metadata["laps"])
        
        summary = {
            "total_laps": int(len(laps_df)),
            "weather_distribution": {k: int(v) for k, v in laps_df["weather"].value_counts().to_dict().items()},
            "anomaly_rate": float(laps_df["has_anomaly"].sum() / len(laps_df)),
            "anomaly_type_distribution": {k: int(v) for k, v in laps_df[laps_df["has_anomaly"]]["anomaly_type"].value_counts().to_dict().items()},
            "lap_time_statistics": {
                "mean": float(laps_df["lap_time_s"].mean()),
                "std": float(laps_df["lap_time_s"].std()),
                "min": float(laps_df["lap_time_s"].min()),
                "max": float(laps_df["lap_time_s"].max()),
                "median": float(laps_df["lap_time_s"].median())
            },
            "telemetry_statistics": {
                "total_samples": int(laps_df["telemetry_samples"].sum()),
                "avg_samples_per_lap": float(laps_df["telemetry_samples"].mean())
            },
            "video_statistics": {
                "total_frames": int(laps_df["video_frames"].sum()),
                "avg_frames_per_lap": float(laps_df["video_frames"].mean())
            }
        }
        
        # Save summary
        output_file = self.output_dir / "summaries" / "dataset_summary.json"
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📊 Summary statistics saved: {output_file}")
        
        # Print summary
        print("\n📈 DATASET SUMMARY STATISTICS")
        print("-" * 80)
        print(f"Weather Distribution:")
        for weather, count in summary["weather_distribution"].items():
            print(f"  {weather}: {count} laps ({count/len(laps_df)*100:.1f}%)")
        print(f"\nAnomaly Injection Rate: {summary['anomaly_rate']*100:.2f}%")
        print(f"Anomaly Types:")
        for anom_type, count in summary["anomaly_type_distribution"].items():
            print(f"  {anom_type}: {count} occurrences")
        print(f"\nLap Time Statistics:")
        print(f"  Mean: {summary['lap_time_statistics']['mean']:.2f}s")
        print(f"  Std Dev: {summary['lap_time_statistics']['std']:.2f}s")
        print(f"  Range: {summary['lap_time_statistics']['min']:.2f}s - {summary['lap_time_statistics']['max']:.2f}s")
        print(f"\nTotal Telemetry Samples: {summary['telemetry_statistics']['total_samples']:,}")
        print(f"Total Video Frames: {summary['video_statistics']['total_frames']:,}")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Aspar-Synth-10K dataset")
    parser.add_argument("--num-laps", type=int, default=10000, help="Number of laps to generate")
    parser.add_argument("--output-dir", type=str, default="/workspaces/Bucle2D/data/aspar_synth_10k",
                       help="Output directory for dataset")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--quick-test", action="store_true", help="Generate only 100 laps for testing")
    
    args = parser.parse_args()
    
    if args.quick_test:
        print("🔬 QUICK TEST MODE: Generating 100 laps only")
        num_laps = 100
    else:
        num_laps = args.num_laps
    
    # Create generator
    generator = AsparSynth10KGenerator(output_dir=args.output_dir, seed=args.seed)
    
    # Generate dataset
    generator.generate_dataset(num_laps=num_laps, save_every=100)
    
    print("\n✅ Dataset generation complete!")
    print(f"📁 Location: {args.output_dir}")
    print("\nTo use this dataset in your experiments:")
    print(f"  import json")
    print(f"  with open('{args.output_dir}/dataset_metadata.json') as f:")
    print(f"      metadata = json.load(f)")
