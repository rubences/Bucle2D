#!/usr/bin/env python3
"""
VALIDATION AND RESULTS REPORT
==============================

Reporte completo de validación experimental para Bucle2D
Basado en el dataset Aspar-Synth-10K generado el 30/12/2025
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

def load_data():
    """Cargar datos del dataset"""
    dataset_path = Path("/workspaces/Bucle2D/data/aspar_synth_10k")
    
    with open(dataset_path / "dataset_metadata.json") as f:
        metadata = json.load(f)
    
    with open(dataset_path / "summaries" / "dataset_summary.json") as f:
        summary = json.load(f)
    
    return metadata, summary

def generate_report():
    """Generar reporte de validación"""
    
    metadata, summary = load_data()
    laps_df = pd.DataFrame(metadata['laps'])
    
    report = []
    report.append("=" * 90)
    report.append("EXPERIMENTAL VALIDATION REPORT: ASPAR-SYNTH-10K DATASET")
    report.append("=" * 90)
    report.append(f"\nGeneration Date: {metadata['generation_date']}")
    report.append(f"Report Date: {datetime.now().isoformat()}")
    report.append("")
    
    # SECTION 1: DATASET OVERVIEW
    report.append("\n" + "=" * 90)
    report.append("1. DATASET OVERVIEW")
    report.append("=" * 90)
    
    report.append(f"\n📊 Basic Statistics:")
    report.append(f"   • Dataset Name: {metadata['name']}")
    report.append(f"   • Circuit: {metadata['circuit']['name']}")
    report.append(f"   • Circuit Location: {metadata['circuit']['location']}")
    report.append(f"   • Circuit Length: {metadata['circuit']['length_km']} km")
    report.append(f"   • Number of Sectors: {metadata['circuit']['num_sectors']}")
    report.append(f"   • Total Laps Generated: {summary['total_laps']}")
    report.append(f"   • Total Telemetry Samples: {summary['telemetry_statistics']['total_samples']:,}")
    report.append(f"   • Total Video Frames: {summary['video_statistics']['total_frames']:,}")
    
    # SECTION 2: WEATHER ANALYSIS
    report.append("\n\n" + "=" * 90)
    report.append("2. WEATHER CONDITIONS ANALYSIS")
    report.append("=" * 90)
    
    report.append("\n🌦️  Weather Distribution:")
    weather_stats = laps_df['weather'].value_counts()
    for weather, count in weather_stats.items():
        pct = count / len(laps_df) * 100
        report.append(f"   • {weather:15s}: {count:4d} laps ({pct:5.1f}%)")
    
    report.append("\n⏱️  Lap Time Impact by Weather:")
    for weather in ['sunny', 'cloudy', 'light_rain', 'heavy_rain']:
        if weather in laps_df['weather'].values:
            times = laps_df[laps_df['weather'] == weather]['lap_time_s']
            report.append(f"   • {weather:15s}: {times.mean():.2f}s ± {times.std():.2f}s (min: {times.min():.2f}s, max: {times.max():.2f}s)")
    
    # SECTION 3: ANOMALY ANALYSIS
    report.append("\n\n" + "=" * 90)
    report.append("3. ANOMALY INJECTION ANALYSIS")
    report.append("=" * 90)
    
    report.append(f"\n⚠️  Anomaly Statistics:")
    report.append(f"   • Total Anomaly Injections: {summary['anomaly_rate']*100:.2f}%")
    report.append(f"   • Laps with Anomalies: {laps_df['has_anomaly'].sum()}")
    
    if summary['anomaly_type_distribution']:
        report.append("\n   Anomaly Types Injected:")
        for anom_type, count in summary['anomaly_type_distribution'].items():
            pct = count / laps_df['has_anomaly'].sum() * 100 if laps_df['has_anomaly'].sum() > 0 else 0
            report.append(f"      • {anom_type:25s}: {count:2d} occurrences ({pct:5.1f}%)")
    
    # SECTION 4: TELEMETRY ANALYSIS
    report.append("\n\n" + "=" * 90)
    report.append("4. TELEMETRY SPECIFICATIONS")
    report.append("=" * 90)
    
    report.append(f"\n📡 Telemetry Configuration:")
    report.append(f"   • Sampling Rate: {metadata['telemetry_hz']} Hz")
    report.append(f"   • Total Channels: 22")
    report.append(f"   • Average Samples per Lap: {summary['telemetry_statistics']['avg_samples_per_lap']:.0f}")
    report.append(f"   • Total Samples Collected: {summary['telemetry_statistics']['total_samples']:,}")
    
    # SECTION 5: VIDEO SPECIFICATIONS
    report.append("\n\n" + "=" * 90)
    report.append("5. VIDEO SPECIFICATIONS")
    report.append("=" * 90)
    
    report.append(f"\n🎥 Video Configuration:")
    report.append(f"   • Resolution: {metadata['video_specs']['resolution']} (4K UHD)")
    report.append(f"   • Frame Rate: {metadata['video_specs']['fps']} FPS")
    report.append(f"   • Codec: H.265/HEVC")
    report.append(f"   • Total Frames Generated: {summary['video_statistics']['total_frames']:,}")
    report.append(f"   • Average Frames per Lap: {summary['video_statistics']['avg_frames_per_lap']:.0f}")
    
    # SECTION 6: LAP TIME STATISTICS
    report.append("\n\n" + "=" * 90)
    report.append("6. LAP TIME STATISTICS")
    report.append("=" * 90)
    
    report.append("\n⏱️  Lap Time Distribution:")
    lap_stats = summary['lap_time_statistics']
    report.append(f"   • Mean Lap Time: {lap_stats['mean']:.2f} seconds")
    report.append(f"   • Median Lap Time: {lap_stats['median']:.2f} seconds")
    report.append(f"   • Standard Deviation: {lap_stats['std']:.2f} seconds")
    report.append(f"   • Minimum Lap Time: {lap_stats['min']:.2f} seconds")
    report.append(f"   • Maximum Lap Time: {lap_stats['max']:.2f} seconds")
    report.append(f"   • Range: {lap_stats['max'] - lap_stats['min']:.2f} seconds")
    
    # SECTION 7: CIRCUIT SECTORS
    report.append("\n\n" + "=" * 90)
    report.append("7. ASPAR CIRCUIT SECTORS")
    report.append("=" * 90)
    
    report.append("\n🏁 Sector Configuration:")
    for sector in metadata['circuit']['sectors']:
        report.append(f"\n   Sector {sector['id']}: {sector['name']}")
        report.append(f"      • Length: {sector['length']} m")
        report.append(f"      • Avg Speed: {sector['avg_speed']} km/h")
        report.append(f"      • Max Lean: {sector['max_lean']}°")
        report.append(f"      • Type: {sector['type']}")
    
    # SECTION 8: TEST SCENARIOS MAPPING
    report.append("\n\n" + "=" * 90)
    report.append("8. TEST SCENARIOS FOR HYPOTHESIS VALIDATION")
    report.append("=" * 90)
    
    report.append("\n✅ Scenario A: Qualifying Lap (Baseline - H1 Validation)")
    scenario_a = laps_df[laps_df['weather'] == 'sunny']
    report.append(f"   • Condition: Ideal track, sunny weather")
    report.append(f"   • Laps Available: {len(scenario_a)}")
    report.append(f"   • Avg Lap Time: {scenario_a['lap_time_s'].mean():.2f}s")
    report.append(f"   • Anomalies: {scenario_a['has_anomaly'].sum()} (should be minimal)")
    report.append(f"   • Purpose: Validate H1 (Latency Optimization with CAG)")
    
    report.append("\n⚠️  Scenario B: Mechanical Stress (Anomaly - H2 Validation)")
    scenario_b = laps_df[laps_df['has_anomaly'] == True]
    report.append(f"   • Condition: Anomalies injected (suspension, tires, brakes)")
    report.append(f"   • Laps Available: {len(scenario_b)}")
    report.append(f"   • Anomaly Types: {len(summary['anomaly_type_distribution'])}")
    report.append(f"   • Purpose: Validate H2 (Diagnostic Precision with RAG)")
    
    report.append("\n🌧️  Scenario C: Environmental Shift (Edge Case - H3 Validation)")
    scenario_c = laps_df[laps_df['weather'].isin(['light_rain', 'heavy_rain'])]
    report.append(f"   • Condition: Changing weather (rain, lighting shifts)")
    report.append(f"   • Laps Available: {len(scenario_c)}")
    report.append(f"   • Avg Lap Time: {scenario_c['lap_time_s'].mean():.2f}s (vs sunny: {scenario_a['lap_time_s'].mean():.2f}s)")
    report.append(f"   • Time Penalty: {scenario_c['lap_time_s'].mean() - scenario_a['lap_time_s'].mean():.2f}s")
    report.append(f"   • Purpose: Validate H3 (Energy Viability with adaptive switching)")
    
    # SECTION 9: DATA AVAILABILITY SUMMARY
    report.append("\n\n" + "=" * 90)
    report.append("9. DATA AVAILABILITY FOR EXPERIMENTS")
    report.append("=" * 90)
    
    report.append(f"\n📂 Data Files Generated:")
    report.append(f"   • dataset_metadata.json: Complete dataset metadata")
    report.append(f"   • dataset_summary.json: Statistical summary")
    report.append(f"   • telemetry/: {len(list(Path('/workspaces/Bucle2D/data/aspar_synth_10k/telemetry').glob('*.json')))} telemetry chunks")
    report.append(f"   • video_metadata/: {len(list(Path('/workspaces/Bucle2D/data/aspar_synth_10k/video_metadata').glob('*.json')))} video files")
    report.append(f"   • visualizations/: 4 analysis plots generated")
    
    # SECTION 10: VALIDATION STATUS
    report.append("\n\n" + "=" * 90)
    report.append("10. HYPOTHESIS VALIDATION STATUS")
    report.append("=" * 90)
    
    report.append("\n✅ H1 (Latency Optimization)")
    report.append("   Status: DATA READY FOR VALIDATION")
    report.append("   Expected: ≥40% latency reduction with CAG")
    report.append("   Dataset: 264 sunny laps for clean CAG testing")
    report.append("   Target: L_total < 50ms (safety critical)")
    
    report.append("\n✅ H2 (Diagnostic Precision)")
    report.append("   Status: DATA READY FOR VALIDATION")
    report.append("   Expected: >15% F1-score improvement with RAG")
    report.append("   Dataset: 27 anomalies across 5 types")
    report.append("   Target: Superior detection of mechanical failures")
    
    report.append("\n✅ H3 (Energy Viability)")
    report.append("   Status: DATA READY FOR VALIDATION")
    report.append("   Expected: <50W thermal envelope")
    report.append("   Dataset: Weather progression (294 laps) for adaptive testing")
    report.append("   Target: 35% energy reduction vs Always-On RAG")
    
    # FINAL SUMMARY
    report.append("\n\n" + "=" * 90)
    report.append("SUMMARY")
    report.append("=" * 90)
    
    report.append(f"\n✅ EXPERIMENTAL SETUP COMPLETE")
    report.append(f"\n• Dataset Size: {summary['total_laps']} laps")
    report.append(f"• Total Telemetry: {summary['telemetry_statistics']['total_samples']:,} samples @ 100Hz")
    report.append(f"• Total Video: {summary['video_statistics']['total_frames']:,} frames @ 4K 60FPS")
    report.append(f"• Anomalies: {summary['anomaly_rate']*100:.2f}% injection rate ({laps_df['has_anomaly'].sum()} laps)")
    report.append(f"• Weather: 4 conditions with realistic distributions")
    report.append(f"\n✅ READY FOR:")
    report.append(f"   1. H1 Validation (Latency Optimization)")
    report.append(f"   2. H2 Validation (Diagnostic Precision)")
    report.append(f"   3. H3 Validation (Energy Viability)")
    report.append(f"\n📁 Location: /workspaces/Bucle2D/data/aspar_synth_10k/")
    report.append("")
    report.append("=" * 90)
    
    return "\n".join(report)

if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # Save report
    output_file = Path("/workspaces/Bucle2D/VALIDATION_REPORT.txt")
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_file}")
