#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure project root is on path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from main_inference import RacingInferencePipeline  # noqa: E402


def run_simulation(results_path: Path, frames_per_sector: int = 30) -> Dict:
    pipeline = RacingInferencePipeline(
        config_path=str(ROOT / "data/aspar_circuit_config.json"),
        confidence_threshold=0.85,
        device="cpu",
    )
    results = pipeline.run_lap_simulation(
        num_sectors_per_lap=None, frames_per_sector=frames_per_sector, verbose=True
    )
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to {results_path}")
    return results


def build_dataframe(results: Dict) -> pd.DataFrame:
    rows: List[Dict] = []
    frame_counter = 0
    for s_idx, sector in enumerate(results["sector_telemetry"]):
        sector_id = sector["sector_id"]
        for t in sector["telemetry"]:
            rows.append(
                {
                    "global_frame": frame_counter,
                    "sector_index": s_idx + 1,
                    "sector_id": sector_id,
                    "frame": t["frame"],
                    "timestamp": t["timestamp"],
                    "speed_kmh": t["speed_kmh"],
                    "lean_angle": t["lean_angle"],
                    "throttle": t["throttle"],
                    "confidence": t["confidence"],
                    "tool": t["tool"],
                    "decision_time_ms": t["decision_time_ms"],
                }
            )
            frame_counter += 1
    df = pd.DataFrame(rows)
    return df


def save_plot(fig, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)
    print(f"Saved figure: {out_path}")


def plot_overall_speed_timeline(df: pd.DataFrame, out_dir: Path):
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(df["global_frame"], df["speed_kmh"], color="#1f77b4", lw=1.5)
    ax.set_title("Velocidad global a lo largo de la vuelta")
    ax.set_xlabel("Frame global")
    ax.set_ylabel("Velocidad (km/h)")
    # Sombrear sectores alternos
    sectors = df[["sector_index", "global_frame"]].groupby("sector_index").agg(["min", "max"])  # type: ignore
    for idx, row in sectors.iterrows():
        gmin = row["global_frame"]["min"]
        gmax = row["global_frame"]["max"]
        if idx % 2 == 0:
            ax.axvspan(gmin, gmax, color="gray", alpha=0.08)
    save_plot(fig, out_dir / "01_timeline_speed.png")


def plot_confidence_with_tool(df: pd.DataFrame, out_dir: Path):
    colors = {"CAG": "#2ca02c", "RAG": "#d62728"}
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(df["global_frame"], df["confidence"], color="#444", lw=1.2, label="Confianza")
    # Overlay puntos por herramienta
    for tool, dft in df.groupby("tool"):
        ax.scatter(dft["global_frame"], dft["confidence"], s=8, alpha=0.6, label=tool, c=colors.get(tool, "#999"))
    ax.set_title("Confianza por frame y herramienta usada")
    ax.set_xlabel("Frame global")
    ax.set_ylabel("Confianza [0-1]")
    ax.legend()
    save_plot(fig, out_dir / "02_confidence_tool.png")


def plot_avg_speed_per_sector(results: Dict, out_dir: Path):
    sectors = results["sector_telemetry"]
    labels = [s["sector_id"] for s in sectors]
    vals = [s["avg_speed_kmh"] for s in sectors]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(labels, vals, color="#1f77b4")
    ax.set_title("Velocidad media por sector")
    ax.set_xlabel("Sector")
    ax.set_ylabel("Velocidad media (km/h)")
    ax.set_xticklabels(labels, rotation=30, ha="right")
    save_plot(fig, out_dir / "03_avg_speed_per_sector.png")


def plot_tool_usage_pie(results: Dict, out_dir: Path):
    metrics = results.get("performance_metrics", {})
    cag = float(metrics.get("cag_usage_percent", 0.0))
    rag = float(metrics.get("rag_usage_percent", 0.0))
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie([cag, rag], labels=["CAG", "RAG"], colors=["#2ca02c", "#d62728"], autopct="%1.1f%%")
    ax.set_title("Uso de herramientas (CAG vs RAG)")
    save_plot(fig, out_dir / "04_tool_usage_pie.png")


def plot_decision_time_hist(df: pd.DataFrame, out_dir: Path):
    fig, ax = plt.subplots(figsize=(9, 4))
    for tool, dft in df.groupby("tool"):
        ax.hist(dft["decision_time_ms"], bins=20, alpha=0.6, label=tool)
    ax.set_title("Distribución de tiempos de decisión por herramienta")
    ax.set_xlabel("Tiempo (ms)")
    ax.set_ylabel("Frecuencia")
    ax.legend()
    save_plot(fig, out_dir / "05_decision_time_hist.png")


def plot_speed_vs_confidence(df: pd.DataFrame, out_dir: Path):
    colors = {"CAG": "#2ca02c", "RAG": "#d62728"}
    fig, ax = plt.subplots(figsize=(6, 5))
    for tool, dft in df.groupby("tool"):
        ax.scatter(dft["confidence"], dft["speed_kmh"], s=10, alpha=0.5, label=tool, c=colors.get(tool, "#999"))
    ax.set_title("Velocidad vs Confianza")
    ax.set_xlabel("Confianza")
    ax.set_ylabel("Velocidad (km/h)")
    ax.legend()
    save_plot(fig, out_dir / "06_speed_vs_confidence.png")


def generate_plots(results: Dict, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    df = build_dataframe(results)
    plot_overall_speed_timeline(df, out_dir)
    plot_confidence_with_tool(df, out_dir)
    plot_avg_speed_per_sector(results, out_dir)
    plot_tool_usage_pie(results, out_dir)
    plot_decision_time_hist(df, out_dir)
    plot_speed_vs_confidence(df, out_dir)


def main():
    results_path = ROOT / "results" / "lap_results.json"
    plots_dir = ROOT / "results" / "plots"

    # Run simulation
    results = run_simulation(results_path=results_path, frames_per_sector=30)

    # Generate plots
    generate_plots(results, plots_dir)

    # Print summary
    metrics = results.get("performance_metrics", {})
    print("\nResumen de rendimiento:")
    for k in [
        "total_lap_time_s",
        "fps",
        "avg_frame_time_ms",
        "cag_usage_percent",
        "rag_usage_percent",
        "avg_decision_time_ms",
        "latency_reduction_percent",
    ]:
        if k in metrics:
            print(f"  {k}: {metrics[k]:.2f}" if isinstance(metrics[k], (int, float)) else f"  {k}: {metrics[k]}")

    print(f"\nResultados: {results_path}")
    print(f"Gráficas: {plots_dir}")


if __name__ == "__main__":
    sys.exit(main())
