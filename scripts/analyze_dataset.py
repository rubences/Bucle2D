"""
Dataset Analysis and Visualization Tool for Aspar-Synth-10K
============================================================

This script provides analysis and visualization capabilities for the
Aspar-Synth-10K dataset.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 10

class AsparDatasetAnalyzer:
    """Analyzer for Aspar-Synth-10K dataset"""
    
    def __init__(self, dataset_path: str = "/workspaces/Bucle2D/data/aspar_synth_10k"):
        self.dataset_path = Path(dataset_path)
        self.metadata = None
        self.laps_df = None
        self.summary = None
        
        self._load_metadata()
    
    def _load_metadata(self):
        """Load dataset metadata"""
        with open(self.dataset_path / "dataset_metadata.json") as f:
            self.metadata = json.load(f)
        
        self.laps_df = pd.DataFrame(self.metadata['laps'])
        
        with open(self.dataset_path / "summaries" / "dataset_summary.json") as f:
            self.summary = json.load(f)
        
        print(f"✅ Loaded dataset: {self.metadata['name']}")
        print(f"   Total laps: {len(self.laps_df)}")
        print(f"   Generation date: {self.metadata['generation_date']}")
    
    def print_summary(self):
        """Print dataset summary statistics"""
        print("\n" + "=" * 80)
        print("DATASET SUMMARY STATISTICS")
        print("=" * 80)
        
        print(f"\n📊 General Info:")
        print(f"   Dataset Name: {self.metadata['name']}")
        print(f"   Circuit: {self.metadata['circuit']['name']}")
        print(f"   Circuit Length: {self.metadata['circuit']['length_km']} km")
        print(f"   Total Laps: {self.summary['total_laps']}")
        
        print(f"\n🌦️  Weather Distribution:")
        for weather, count in self.summary['weather_distribution'].items():
            pct = count / self.summary['total_laps'] * 100
            print(f"   {weather:15s}: {count:5d} laps ({pct:5.1f}%)")
        
        print(f"\n⚠️  Anomalies:")
        print(f"   Injection Rate: {self.summary['anomaly_rate']*100:.2f}%")
        if self.summary['anomaly_type_distribution']:
            for anom_type, count in self.summary['anomaly_type_distribution'].items():
                print(f"   {anom_type:25s}: {count:3d} occurrences")
        
        print(f"\n⏱️  Lap Time Statistics:")
        lap_stats = self.summary['lap_time_statistics']
        print(f"   Mean:   {lap_stats['mean']:.2f}s")
        print(f"   Median: {lap_stats['median']:.2f}s")
        print(f"   Std:    {lap_stats['std']:.2f}s")
        print(f"   Range:  {lap_stats['min']:.2f}s - {lap_stats['max']:.2f}s")
        
        print(f"\n📡 Telemetry:")
        print(f"   Sampling Rate: {self.metadata['telemetry_hz']} Hz")
        print(f"   Total Samples: {self.summary['telemetry_statistics']['total_samples']:,}")
        print(f"   Avg per Lap:   {self.summary['telemetry_statistics']['avg_samples_per_lap']:.0f}")
        
        print(f"\n🎥 Video:")
        print(f"   Resolution: {self.metadata['video_specs']['resolution']}")
        print(f"   FPS:        {self.metadata['video_specs']['fps']}")
        print(f"   Total Frames: {self.summary['video_statistics']['total_frames']:,}")
        print(f"   Avg per Lap:  {self.summary['video_statistics']['avg_frames_per_lap']:.0f}")
        
        print("\n" + "=" * 80)
    
    def plot_lap_time_distribution(self, save_path: str = None):
        """Plot lap time distribution by weather"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Overall distribution
        axes[0].hist(self.laps_df['lap_time_s'], bins=30, edgecolor='black', alpha=0.7)
        axes[0].axvline(self.laps_df['lap_time_s'].mean(), color='red', 
                       linestyle='--', linewidth=2, label=f'Mean: {self.laps_df["lap_time_s"].mean():.2f}s')
        axes[0].set_xlabel('Lap Time (seconds)', fontweight='bold')
        axes[0].set_ylabel('Frequency', fontweight='bold')
        axes[0].set_title('Lap Time Distribution', fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Distribution by weather
        weather_order = ['sunny', 'cloudy', 'light_rain', 'heavy_rain']
        weather_colors = {'sunny': '#FDB462', 'cloudy': '#BEBADA', 
                         'light_rain': '#80B1D3', 'heavy_rain': '#377EB8'}
        
        for weather in weather_order:
            if weather in self.laps_df['weather'].values:
                data = self.laps_df[self.laps_df['weather'] == weather]['lap_time_s']
                axes[1].hist(data, bins=20, alpha=0.6, label=weather, 
                           color=weather_colors.get(weather, 'gray'), edgecolor='black')
        
        axes[1].set_xlabel('Lap Time (seconds)', fontweight='bold')
        axes[1].set_ylabel('Frequency', fontweight='bold')
        axes[1].set_title('Lap Time Distribution by Weather', fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Saved: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_weather_impact(self, save_path: str = None):
        """Plot weather impact on lap times"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        weather_order = ['sunny', 'cloudy', 'light_rain', 'heavy_rain']
        weather_data = []
        
        for weather in weather_order:
            if weather in self.laps_df['weather'].values:
                data = self.laps_df[self.laps_df['weather'] == weather]['lap_time_s']
                weather_data.append(data)
        
        bp = ax.boxplot(weather_data, labels=[w for w in weather_order if w in self.laps_df['weather'].values],
                       patch_artist=True, showmeans=True)
        
        # Color boxes
        colors = ['#FDB462', '#BEBADA', '#80B1D3', '#377EB8']
        for patch, color in zip(bp['boxes'], colors[:len(weather_data)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_xlabel('Weather Condition', fontweight='bold', fontsize=12)
        ax.set_ylabel('Lap Time (seconds)', fontweight='bold', fontsize=12)
        ax.set_title('Weather Impact on Lap Times', fontweight='bold', fontsize=13)
        ax.grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Saved: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_anomaly_distribution(self, save_path: str = None):
        """Plot anomaly type and sector distribution"""
        anomalies_df = self.laps_df[self.laps_df['has_anomaly'] == True]
        
        if len(anomalies_df) == 0:
            print("⚠️  No anomalies found in dataset")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Anomaly type distribution
        anomaly_counts = anomalies_df['anomaly_type'].value_counts()
        axes[0].barh(range(len(anomaly_counts)), anomaly_counts.values, 
                    color='#E74C3C', alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[0].set_yticks(range(len(anomaly_counts)))
        axes[0].set_yticklabels(anomaly_counts.index)
        axes[0].set_xlabel('Number of Occurrences', fontweight='bold')
        axes[0].set_title('Anomaly Type Distribution', fontweight='bold')
        axes[0].grid(True, axis='x', alpha=0.3)
        
        # Add counts on bars
        for i, v in enumerate(anomaly_counts.values):
            axes[0].text(v + 0.1, i, str(v), va='center', fontweight='bold')
        
        # Anomaly sector distribution
        sector_counts = anomalies_df['anomaly_sector'].value_counts().sort_index()
        axes[1].bar(sector_counts.index, sector_counts.values, 
                   color='#3498DB', alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[1].set_xlabel('Sector ID', fontweight='bold')
        axes[1].set_ylabel('Number of Anomalies', fontweight='bold')
        axes[1].set_title('Anomaly Distribution by Sector', fontweight='bold')
        axes[1].set_xticks(range(1, 9))
        axes[1].grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Saved: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_telemetry_sample(self, lap_id: int = 1, save_path: str = None):
        """Plot sample telemetry data for a specific lap"""
        # Find which chunk contains this lap
        chunk_id = (lap_id - 1) // 100
        telemetry_file = self.dataset_path / "telemetry" / f"telemetry_chunk_{chunk_id:04d}.json"
        
        if not telemetry_file.exists():
            print(f"❌ Telemetry file not found for lap {lap_id}")
            return
        
        with open(telemetry_file) as f:
            telemetry_data = json.load(f)
        
        data_points = telemetry_data['data_points']
        
        # Create dataframe
        df = pd.DataFrame(data_points)
        
        # Plot multiple channels
        fig, axes = plt.subplots(3, 2, figsize=(14, 10))
        fig.suptitle(f'Telemetry Sample - Lap {lap_id}', fontsize=14, fontweight='bold')
        
        # Speed
        axes[0, 0].plot(df['timestamp'], df['speed_kmh'], linewidth=2, color='#2ECC71')
        axes[0, 0].set_ylabel('Speed (km/h)', fontweight='bold')
        axes[0, 0].set_title('Speed Profile')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Lean Angle
        axes[0, 1].plot(df['timestamp'], df['lean_angle_deg'], linewidth=2, color='#E74C3C')
        axes[0, 1].set_ylabel('Lean Angle (°)', fontweight='bold')
        axes[0, 1].set_title('Lean Angle')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Throttle & Brake
        axes[1, 0].plot(df['timestamp'], df['throttle_pct'], linewidth=2, label='Throttle', color='#2ECC71')
        axes[1, 0].plot(df['timestamp'], df['brake_pct'], linewidth=2, label='Brake', color='#E74C3C')
        axes[1, 0].set_ylabel('% [0-100]', fontweight='bold')
        axes[1, 0].set_title('Throttle & Brake')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Accelerations
        axes[1, 1].plot(df['timestamp'], df['accel_long_g'], linewidth=2, label='Longitudinal', color='#3498DB')
        axes[1, 1].plot(df['timestamp'], df['accel_lat_g'], linewidth=2, label='Lateral', color='#9B59B6')
        axes[1, 1].set_ylabel('Acceleration (G)', fontweight='bold')
        axes[1, 1].set_title('Accelerations')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        # Tire Temperatures
        axes[2, 0].plot(df['timestamp'], df['tire_temp_fl_c'], linewidth=2, label='FL', alpha=0.7)
        axes[2, 0].plot(df['timestamp'], df['tire_temp_fr_c'], linewidth=2, label='FR', alpha=0.7)
        axes[2, 0].plot(df['timestamp'], df['tire_temp_rl_c'], linewidth=2, label='RL', alpha=0.7)
        axes[2, 0].plot(df['timestamp'], df['tire_temp_rr_c'], linewidth=2, label='RR', alpha=0.7)
        axes[2, 0].set_ylabel('Temperature (°C)', fontweight='bold')
        axes[2, 0].set_xlabel('Time (s)', fontweight='bold')
        axes[2, 0].set_title('Tire Temperatures')
        axes[2, 0].legend(ncol=4)
        axes[2, 0].grid(True, alpha=0.3)
        
        # Suspension Travel
        axes[2, 1].plot(df['timestamp'], df['suspension_fl_mm'], linewidth=2, label='FL', alpha=0.7)
        axes[2, 1].plot(df['timestamp'], df['suspension_fr_mm'], linewidth=2, label='FR', alpha=0.7)
        axes[2, 1].plot(df['timestamp'], df['suspension_rl_mm'], linewidth=2, label='RL', alpha=0.7)
        axes[2, 1].plot(df['timestamp'], df['suspension_rr_mm'], linewidth=2, label='RR', alpha=0.7)
        axes[2, 1].set_ylabel('Travel (mm)', fontweight='bold')
        axes[2, 1].set_xlabel('Time (s)', fontweight='bold')
        axes[2, 1].set_title('Suspension Travel')
        axes[2, 1].legend(ncol=4)
        axes[2, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Saved: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def generate_all_visualizations(self, output_dir: str = None):
        """Generate all visualization plots"""
        if output_dir is None:
            output_dir = self.dataset_path / "visualizations"
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        print("\n🎨 Generating visualizations...")
        
        self.plot_lap_time_distribution(output_dir / "lap_time_distribution.png")
        self.plot_weather_impact(output_dir / "weather_impact.png")
        self.plot_anomaly_distribution(output_dir / "anomaly_distribution.png")
        self.plot_telemetry_sample(lap_id=1, save_path=output_dir / "telemetry_sample_lap1.png")
        
        print(f"\n✅ All visualizations saved to: {output_dir}")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze Aspar-Synth-10K dataset")
    parser.add_argument("--dataset-path", type=str, 
                       default="/workspaces/Bucle2D/data/aspar_synth_10k",
                       help="Path to dataset directory")
    parser.add_argument("--generate-plots", action="store_true",
                       help="Generate all visualization plots")
    parser.add_argument("--plot-lap", type=int, default=None,
                       help="Plot telemetry for specific lap")
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = AsparDatasetAnalyzer(args.dataset_path)
    
    # Print summary
    analyzer.print_summary()
    
    # Generate plots if requested
    if args.generate_plots:
        analyzer.generate_all_visualizations()
    
    # Plot specific lap if requested
    if args.plot_lap is not None:
        print(f"\n📊 Plotting telemetry for lap {args.plot_lap}...")
        analyzer.plot_telemetry_sample(lap_id=args.plot_lap)
