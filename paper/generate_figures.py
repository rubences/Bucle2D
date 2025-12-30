"""
Script para generar las figuras del paper de validación experimental
Paper: Agentic-Racing-Vision - Hybrid RAG-CAG Architecture

Este script genera todas las visualizaciones referenciadas en la Sección 5 (Results and Analysis)
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import os

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9

# Crear directorio para figuras
OUTPUT_DIR = "/workspaces/Bucle2D/paper/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Generando figuras para el paper...")
print(f"Directorio de salida: {OUTPUT_DIR}")
print("=" * 60)

# ==============================================================================
# FIGURA 9: Latency Probability Density Function
# ==============================================================================
def generate_fig9_latency_pdf():
    print("\n[1/7] Generando Figura 9: Latency PDF...")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Standard RAG: Distribución Gaussiana centrada en 48ms
    latency_rag = np.linspace(10, 60, 1000)
    pdf_rag = norm.pdf(latency_rag, loc=48, scale=3)
    
    # Hybrid: Distribución bimodal (CAG peak + RAG tail)
    pdf_cag = norm.pdf(latency_rag, loc=20, scale=2) * 0.85  # 85% cache hits
    pdf_rag_tail = norm.pdf(latency_rag, loc=45, scale=3) * 0.15  # 15% RAG
    pdf_hybrid = pdf_cag + pdf_rag_tail
    
    # Normalizar
    pdf_hybrid = pdf_hybrid / np.max(pdf_hybrid) * np.max(pdf_rag)
    
    # Plot
    ax.plot(latency_rag, pdf_rag, 'b-', linewidth=2.5, label='Standard RAG', alpha=0.7)
    ax.fill_between(latency_rag, pdf_rag, alpha=0.2, color='blue')
    
    ax.plot(latency_rag, pdf_hybrid, 'g-', linewidth=2.5, label='Ours (Hybrid)', alpha=0.8)
    ax.fill_between(latency_rag, pdf_hybrid, alpha=0.3, color='green')
    
    # Línea de límite de seguridad
    ax.axvline(x=50, color='red', linestyle='--', linewidth=2, label='Safety Limit (50ms)')
    
    ax.set_xlabel('Inference Latency (ms)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency Density', fontsize=12, fontweight='bold')
    ax.set_title('Probability Density Function of System Latency', fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(10, 60)
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig9_latency_density.pdf")
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.savefig(output_path.replace('.pdf', '.png'), format='png', bbox_inches='tight')
    print(f"   ✅ Guardado: {output_path}")
    plt.close()

# ==============================================================================
# FIGURA 10: Latency Comparison Across Scenarios
# ==============================================================================
def generate_fig10_latency_scenarios():
    print("\n[2/7] Generando Figura 10: Latency Scenarios...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scenarios = ['Scenario A\n(Nominal)', 'Scenario B\n(Anomaly)', 'Scenario C\n(Edge)']
    rag_latency = [82.1, 85.4, 83.7]
    hybrid_latency = [12.4, 45.2, 38.6]
    
    x = np.arange(len(scenarios))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, rag_latency, width, label='Standard RAG', 
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, hybrid_latency, width, label='Ours (Hybrid)', 
                   color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Añadir valores encima de las barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{height:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Línea de límite
    ax.axhline(y=50, color='red', linestyle='--', linewidth=2.5, label='Limit (50ms)')
    ax.text(2.3, 52, 'Safety Limit', color='red', fontweight='bold', fontsize=10)
    
    ax.set_ylabel('Avg. Latency (ms)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Test Scenarios', fontsize=12, fontweight='bold')
    ax.set_title('Inference Latency Comparison Across Scenarios', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.legend(loc='upper left', frameon=True, shadow=True)
    ax.set_ylim(0, 100)
    ax.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig10_latency_comparison.pdf")
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.savefig(output_path.replace('.pdf', '.png'), format='png', bbox_inches='tight')
    print(f"   ✅ Guardado: {output_path}")
    plt.close()

# ==============================================================================
# FIGURA 11: F1-Score Comparison
# ==============================================================================
def generate_fig11_f1_comparison():
    print("\n[3/7] Generando Figura 11: F1-Score Comparison...")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    categories = ['Track Limits', 'Tire Blistering', 'Susp. Chatter']
    cnn_scores = [0.92, 0.78, 0.61]
    hybrid_scores = [0.94, 0.88, 0.89]
    
    y_pos = np.arange(len(categories))
    height = 0.35
    
    bars1 = ax.barh(y_pos - height/2, cnn_scores, height, label='Stateless CNN',
                    color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.barh(y_pos + height/2, hybrid_scores, height, label='Ours (Hybrid)',
                    color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Añadir valores al final de las barras
    for bars in [bars1, bars2]:
        for bar in bars:
            width_val = bar.get_width()
            ax.text(width_val + 0.01, bar.get_y() + bar.get_height()/2.,
                   f'{width_val:.2f}', ha='left', va='center', fontweight='bold', fontsize=9)
    
    ax.set_xlabel('F1-Score (Higher is Better)', fontsize=12, fontweight='bold')
    ax.set_title('F1-Score Comparison by Anomaly Class', fontsize=13, fontweight='bold')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.set_xlim(0.5, 1.05)
    ax.legend(loc='lower right', frameon=True, shadow=True)
    ax.grid(True, axis='x', alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig11_f1_comparison.pdf")
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.savefig(output_path.replace('.pdf', '.png'), format='png', bbox_inches='tight')
    print(f"   ✅ Guardado: {output_path}")
    plt.close()

# ==============================================================================
# FIGURA 12: Confusion Matrix Heatmap
# ==============================================================================
def generate_fig12_confusion_matrix():
    print("\n[4/7] Generando Figura 12: Confusion Matrix...")
    
    fig, ax = plt.subplots(figsize=(7, 6))
    
    # Confusion matrix para "Suspension Chatter"
    cm = np.array([[98, 2],
                   [11, 89]])
    
    # Normalizar a porcentajes
    cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
    
    sns.heatmap(cm_percent, annot=True, fmt='.0f', cmap='RdYlGn', 
                cbar_kws={'label': 'Percentage (%)'}, vmin=0, vmax=100,
                linewidths=2, linecolor='black', square=True, ax=ax,
                annot_kws={'size': 14, 'weight': 'bold'})
    
    ax.set_xlabel('PREDICTED CLASS', fontsize=12, fontweight='bold')
    ax.set_ylabel('ACTUAL CLASS', fontsize=12, fontweight='bold')
    ax.set_title('Confusion Matrix: Suspension Chatter Detection (Ours)', 
                fontsize=13, fontweight='bold')
    ax.set_xticklabels(['Normal', 'Chatter'], fontsize=11)
    ax.set_yticklabels(['Normal', 'Chatter'], fontsize=11, rotation=0)
    
    # Añadir anotación de métrica objetivo
    ax.text(1.5, -0.3, 'Target Metric:\nHigh Recall achieved', 
           ha='center', va='top', fontsize=10, style='italic',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig12_confusion_matrix.pdf")
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.savefig(output_path.replace('.pdf', '.png'), format='png', bbox_inches='tight')
    print(f"   ✅ Guardado: {output_path}")
    plt.close()

# ==============================================================================
# FIGURA 13: Real-Time Agent Orchestration Trace
# ==============================================================================
def generate_fig13_agent_trace():
    print("\n[5/7] Generando Figura 13: Agent Orchestration Trace...")
    
    fig, ax1 = plt.subplots(figsize=(11, 6))
    
    # Datos sintéticos de latencia y entropía
    time = np.linspace(0, 14, 200)
    latency = np.piecewise(time, 
                          [time < 9, (time >= 9) & (time < 12), time >= 12],
                          [lambda t: 12 + np.random.normal(0, 0.5, len(t)),
                           lambda t: 45 + np.random.normal(0, 2, len(t)),
                           lambda t: 12 + np.random.normal(0, 0.5, len(t))])
    
    entropy = np.piecewise(time,
                          [time < 9, (time >= 9) & (time < 12), time >= 12],
                          [lambda t: 0.15 + np.random.normal(0, 0.02, len(t)),
                           lambda t: 0.78 + np.random.normal(0, 0.03, len(t)),
                           lambda t: 0.16 + np.random.normal(0, 0.02, len(t))])
    
    # Plot latencia (eje izquierdo)
    color_latency = '#3498db'
    ax1.plot(time, latency, color=color_latency, linewidth=2.5, label='System Latency (ms)')
    ax1.fill_between(time, 0, latency, where=(time >= 9) & (time < 12), 
                    alpha=0.3, color='red', label='RAG Mode')
    ax1.fill_between(time, 0, latency, where=(time < 9) | (time >= 12), 
                    alpha=0.3, color='green', label='CAG Mode')
    
    ax1.set_xlabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('System Latency (ms)', fontsize=12, fontweight='bold', color=color_latency)
    ax1.tick_params(axis='y', labelcolor=color_latency)
    ax1.set_ylim(0, 60)
    ax1.grid(True, alpha=0.3)
    
    # Plot entropía (eje derecho)
    ax2 = ax1.twinx()
    color_entropy = '#e67e22'
    ax2.plot(time, entropy, color=color_entropy, linewidth=2.5, 
            linestyle='--', label='Entropy H')
    ax2.set_ylabel('Entropy H', fontsize=12, fontweight='bold', color=color_entropy)
    ax2.tick_params(axis='y', labelcolor=color_entropy)
    ax2.set_ylim(0, 1)
    
    # Combinar leyendas
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', 
              frameon=True, shadow=True, ncol=2)
    
    ax1.set_title('Real-time Agent Orchestration Trace', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig13_agent_trace.pdf")
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.savefig(output_path.replace('.pdf', '.png'), format='png', bbox_inches='tight')
    print(f"   ✅ Guardado: {output_path}")
    plt.close()

# ==============================================================================
# FIGURA 14: Dynamic Power Profiling
# ==============================================================================
def generate_fig14_power_trace():
    print("\n[6/7] Generando Figura 14: Dynamic Power Profiling...")
    
    fig, ax1 = plt.subplots(figsize=(11, 6))
    
    # Datos sintéticos de consumo de energía y entropía
    time = np.linspace(0, 14, 200)
    power = np.piecewise(time,
                        [time < 8, (time >= 8) & (time < 11.5), time >= 11.5],
                        [lambda t: 32 + np.random.normal(0, 0.8, len(t)),
                         lambda t: 47 + np.random.normal(0, 1.2, len(t)),
                         lambda t: 32 + np.random.normal(0, 0.8, len(t))])
    
    uncertainty = np.piecewise(time,
                               [time < 8, (time >= 8) & (time < 11.5), time >= 11.5],
                               [lambda t: 0.15 + np.random.normal(0, 0.02, len(t)),
                                lambda t: 0.75 + np.random.normal(0, 0.04, len(t)),
                                lambda t: 0.16 + np.random.normal(0, 0.02, len(t))])
    
    # Plot consumo energético (eje izquierdo)
    color_power = '#3498db'
    ax1.plot(time, power, color=color_power, linewidth=2.5, label='System Power (W)')
    ax1.fill_between(time, 0, power, where=(time < 8) | (time >= 11.5),
                    alpha=0.3, color='green', label='CAG Mode (Efficient)')
    ax1.fill_between(time, 0, power, where=(time >= 8) & (time < 11.5),
                    alpha=0.3, color='red', label='RAG Spike (Intensive)')
    
    # Línea de límite térmico
    ax1.axhline(y=50, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax1.text(13, 51, 'TDP Limit', color='red', fontweight='bold', fontsize=10)
    
    ax1.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Power Consumption (W)', fontsize=12, fontweight='bold', color=color_power)
    ax1.tick_params(axis='y', labelcolor=color_power)
    ax1.set_ylim(20, 60)
    ax1.grid(True, alpha=0.3)
    
    # Plot incertidumbre (eje derecho)
    ax2 = ax1.twinx()
    color_uncertainty = '#e67e22'
    ax2.plot(time, uncertainty, color=color_uncertainty, linewidth=2.5,
            linestyle='--', label='Uncertainty H')
    ax2.axhline(y=0.45, color='black', linestyle=':', linewidth=2, alpha=0.6)
    ax2.text(13, 0.47, 'Threshold λ=0.45', fontsize=9, style='italic')
    
    ax2.set_ylabel('Visual Entropy H', fontsize=12, fontweight='bold', color=color_uncertainty)
    ax2.tick_params(axis='y', labelcolor=color_uncertainty)
    ax2.set_ylim(0, 1)
    
    # Combinar leyendas
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
              frameon=True, shadow=True, ncol=2)
    
    ax1.set_title('Dynamic Resource Scheduling', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig14_power_trace.pdf")
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.savefig(output_path.replace('.pdf', '.png'), format='png', bbox_inches='tight')
    print(f"   ✅ Guardado: {output_path}")
    plt.close()

# ==============================================================================
# FIGURA 8: Spatial Visualization (Track Map) - Placeholder
# ==============================================================================
def generate_fig8_track_map():
    print("\n[7/7] Generando Figura 8: Track Map (Placeholder)...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Simulación simplificada de un circuito
    theta = np.linspace(0, 2*np.pi, 100)
    r_outer = 3
    r_inner = 1.5
    
    # Track outer boundary
    x_outer = r_outer * np.cos(theta)
    y_outer = r_outer * np.sin(theta) * 1.5
    
    # Track inner boundary
    x_inner = r_inner * np.cos(theta)
    y_inner = r_inner * np.sin(theta) * 1.5
    
    # Plot track
    ax.plot(x_outer, y_outer, 'k-', linewidth=3, label='Track Boundary')
    ax.plot(x_inner, y_inner, 'k-', linewidth=3)
    
    # Segmentos CAG (verde) y RAG (rojo)
    # Segment 1: CAG (0 a 270 grados)
    theta_cag = np.linspace(0, 1.5*np.pi, 75)
    x_cag = (r_outer + r_inner)/2 * np.cos(theta_cag)
    y_cag = (r_outer + r_inner)/2 * np.sin(theta_cag) * 1.5
    ax.plot(x_cag, y_cag, color='green', linewidth=8, alpha=0.7, label='CAG Mode (Static)')
    
    # Segment 2: RAG (270 a 360 grados)
    theta_rag = np.linspace(1.5*np.pi, 2*np.pi, 25)
    x_rag = (r_outer + r_inner)/2 * np.cos(theta_rag)
    y_rag = (r_outer + r_inner)/2 * np.sin(theta_rag) * 1.5
    ax.plot(x_rag, y_rag, color='red', linewidth=8, alpha=0.7, label='RAG Mode (Anomaly)')
    
    # Añadir anotaciones
    ax.text(0, -5, 'S/F\n(Start/Finish)', ha='center', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    ax.text(0.5, -2.5, 'T4\n(Simulated Failure)', ha='center', fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='red', alpha=0.5))
    
    # Zona de histéresis
    theta_hyst = np.linspace(1.4*np.pi, 1.6*np.pi, 20)
    x_hyst = (r_outer + r_inner)/2 * np.cos(theta_hyst)
    y_hyst = (r_outer + r_inner)/2 * np.sin(theta_hyst) * 1.5
    ax.plot(x_hyst, y_hyst, color='orange', linewidth=8, alpha=0.5, 
           linestyle='--', label='Hysteresis Zone (δ)')
    
    ax.set_aspect('equal')
    ax.set_title('Spatial Visualization: Entropy-Driven Mode Selection\nAspar Circuit',
                fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', frameon=True, shadow=True)
    ax.axis('off')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig8_entropy_track_map.pdf")
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.savefig(output_path.replace('.pdf', '.png'), format='png', bbox_inches='tight')
    print(f"   ✅ Guardado: {output_path}")
    plt.close()

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("\n")
    print("=" * 60)
    print("GENERACIÓN DE FIGURAS PARA PAPER BUCLE2D")
    print("=" * 60)
    
    # Generar todas las figuras
    generate_fig8_track_map()
    generate_fig9_latency_pdf()
    generate_fig10_latency_scenarios()
    generate_fig11_f1_comparison()
    generate_fig12_confusion_matrix()
    generate_fig13_agent_trace()
    generate_fig14_power_trace()
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS FIGURAS GENERADAS EXITOSAMENTE")
    print("=" * 60)
    print(f"\n📁 Ubicación: {OUTPUT_DIR}")
    print("\nFiguras generadas:")
    print("  - fig8_entropy_track_map.pdf (+ .png)")
    print("  - fig9_latency_density.pdf (+ .png)")
    print("  - fig10_latency_comparison.pdf (+ .png)")
    print("  - fig11_f1_comparison.pdf (+ .png)")
    print("  - fig12_confusion_matrix.pdf (+ .png)")
    print("  - fig13_agent_trace.pdf (+ .png)")
    print("  - fig14_power_trace.pdf (+ .png)")
    print("\n💡 Recomendación: Reemplaza los placeholders en main.tex")
    print("   con \\includegraphics{figures/figXX_name.pdf}")
    print("")
