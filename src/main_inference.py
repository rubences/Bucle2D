"""
Main Inference Pipeline: Complete Racing Agent System

Orchestrates the full pipeline combining:
- Vision encoding (NestedUNet)
- Agent reasoning (ReAct loop)
- Memory systems (CAG + RAG)
- Simulated telemetry output
"""

import torch
import numpy as np
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys

# Import components
from agent_orchestrator import RacingAgent, ToolType
from memory_systems import CAGMemory, RAGSystem, TelemetryRecord
from vision_encoder import create_vision_encoder


class RacingInferencePipeline:
    """
    Complete inference pipeline for high-performance motorsport perception.
    
    Simulates a full lap around Aspar Circuit with real-time decision-making.
    """
    
    def __init__(self, 
                 config_path: str = "../data/aspar_circuit_config.json",
                 confidence_threshold: float = 0.85,
                 device: str = "cpu"):
        """
        Initialize the inference pipeline.
        
        Args:
            config_path: Path to circuit configuration
            confidence_threshold: CAG/RAG decision threshold
            device: Computation device (cpu or cuda)
        """
        self.device = torch.device(device)
        self.config_path = config_path
        
        print("[INIT] Loading racing vision system components...")
        
        # Initialize vision encoder
        print("  • Loading NestedUNet vision encoder...")
        self.vision_encoder = create_vision_encoder()
        self.vision_encoder = self.vision_encoder.to(self.device)
        self.vision_encoder.eval()
        
        # Initialize agent
        print("  • Initializing ReAct agent...")
        self.agent = RacingAgent(
            confidence_threshold=confidence_threshold,
            embedding_dim=512,
            max_history=100
        )
        
        # Initialize memory systems
        print("  • Loading CAG (static cache)...")
        self.cag_memory = CAGMemory(config_path=config_path)
        
        print("  • Initializing RAG (dynamic retrieval)...")
        self.rag_system = RAGSystem(embedding_dim=512)
        
        # Load circuit configuration
        with open(config_path, 'r') as f:
            self.circuit_config = json.load(f)
        
        self.sectors = self.circuit_config.get("sectors", [])
        self.num_sectors = len(self.sectors)
        self.sector_lengths_km = self._compute_sector_lengths()
        self.sector_difficulties = self._compute_sector_difficulties()
        
        print(f"\n✓ System initialized. Circuit has {self.num_sectors} sectors.")

    def _compute_sector_lengths(self) -> List[float]:
        lengths = []
        for s in self.sectors:
            start = s.get("start_km")
            end = s.get("end_km")
            if start is not None and end is not None:
                lengths.append(max(0.01, float(end) - float(start)))
            else:
                lengths.append(0.0)
        # Fill missing lengths evenly if any are zero
        if any(l == 0.0 for l in lengths) and len(lengths) > 0:
            default_len = self.circuit_config.get("circuit_metadata", {}).get("track_length_km", 3.2) / max(len(lengths), 1)
            lengths = [l if l > 0 else default_len for l in lengths]
        return lengths

    def _compute_sector_difficulties(self) -> List[float]:
        difficulties = []
        for s in self.sectors:
            banking = float(s.get("banking_degrees", 0.0))
            critical = 1.0 if s.get("critical_for_performance", False) else 0.0
            lean_max = float(s.get("lean_angle_max", s.get("avg_lean_angle", 35.0)))
            braking = 0.6 if s.get("braking_intensity") == "hard" else 0.25 if s.get("braking_intensity") else 0.0
            difficulty = min(1.0, 0.15 * critical + 0.01 * max(banking, 0) + 0.01 * max(lean_max - 40.0, 0) + braking)
            difficulties.append(difficulty)
        return difficulties
    
    def simulate_frame(self, sector_idx: int, frame_num: int) -> torch.Tensor:
        """
        Simulate a racing video frame for the current sector.
        
        In a real system, this would be from actual camera input.
        
        Args:
            sector_idx: Current sector index
            frame_num: Frame number within the sector
            
        Returns:
            Simulated frame tensor (1, 3, 512, 512)
        """
        # Create frame with sector-specific characteristics
        frame = torch.randn(1, 3, 512, 512)
        sector = self.sectors[sector_idx]
        
        # Encode sector information into frame
        sector_speed = sector["avg_speed_kmh"]
        sector_lean = sector.get("avg_lean_angle", sector.get("lean_angle_max", 30))
        banking = sector.get("banking_degrees", 0.0)
        difficulty = self.sector_difficulties[sector_idx]
        
        frame[:, 0, :, :] *= (sector_speed / 320.0)  # Speed in red channel
        frame[:, 1, :, :] *= (sector_lean / 70.0)    # Lean angle in green channel
        frame[:, 2, :, :] *= max(0.4, 1.0 - difficulty)  # Harder sectors slightly darker
        
        # Add temporal variation and slight blur for high banking turns
        variability = 0.08 + 0.02 * difficulty + 0.01 * (banking / 10.0)
        frame += torch.randn_like(frame) * variability
        
        return frame
    
    def run_lap_simulation(self, num_sectors_per_lap: Optional[int] = None,
                          frames_per_sector: int = 30,
                          verbose: bool = True) -> Dict:
        """
        Simulate a complete racing lap with real-time decision-making.
        
        Args:
            num_sectors_per_lap: Number of sectors to simulate (default: all)
            frames_per_sector: Number of frames to process per sector
            verbose: Whether to print progress information
            
        Returns:
            Dictionary with lap statistics and telemetry
        """
        if num_sectors_per_lap is None:
            num_sectors_per_lap = self.num_sectors
        else:
            num_sectors_per_lap = min(num_sectors_per_lap, self.num_sectors)
        
        lap_results = {
            "lap_number": 1,
            "total_frames": 0,
            "sector_telemetry": [],
            "decision_timeline": [],
            "performance_metrics": {}
        }
        
        sim_time_s = 0.0
        sector_times = []
        
        if verbose:
            print("\n" + "=" * 70)
            print("RACING LAP SIMULATION - Aspar Circuit")
            print("=" * 70)
        
        # Process each sector
        for sector_idx in range(num_sectors_per_lap):
            sector = self.sectors[sector_idx]
            sector_id = sector["id"]
            sector_name = sector["name"]
            
            if verbose:
                print(f"\n[SECTOR {sector_idx + 1}/{num_sectors_per_lap}] {sector_id} - {sector_name}")
                print(f"  Speed: {sector['avg_speed_kmh']} km/h | "
                      f"Banking: {sector.get('banking_degrees', 0)}°")
            
            sector_length_km = self.sector_lengths_km[sector_idx]
            sector_avg_speed = sector["avg_speed_kmh"]
            sector_time_s = (sector_length_km / max(sector_avg_speed, 1e-3)) * 3600.0
            dt_frame = sector_time_s / frames_per_sector
            sector_times.append(sector_time_s)
            sector_telemetry = []
            sector_decisions = []
            
            # Process frames within sector
            for frame_num in range(frames_per_sector):
                frame_start_time = time.time()
                
                # Simulate input frame
                frame = self.simulate_frame(sector_idx, frame_num)
                frame = frame.to(self.device)
                
                # Vision encoding
                with torch.no_grad():
                    _, visual_embedding = self.vision_encoder(frame)
                    visual_embedding = visual_embedding.cpu().numpy()
                
                # Agent reasoning and decision
                context = {
                    "sector": sector_id,
                    "frame": frame_num,
                    "lap_progress": sector_idx / num_sectors_per_lap,
                    "sector_difficulty": self.sector_difficulties[sector_idx],
                    "banking_degrees": sector.get("banking_degrees", 0.0),
                    "lean_angle_max": sector.get("lean_angle_max", sector.get("avg_lean_angle", 35.0)),
                }
                
                decision = self.agent.step(visual_embedding[0], context=context)
                
                # Extract decision info
                confidence = decision["phase_1_reasoning"]["confidence"]
                tool_used = decision["phase_2_action"]["tool"]
                decision_time = decision["phase_3_observation"]["processing_time_ms"]
                
                # Simulate telemetry output with physics-informed profile
                decision_payload = decision["phase_3_observation"]["decision"]
                throttle = float(decision_payload.get("throttle", 0.6)) if "throttle" in decision_payload else float(decision_payload.get("throttle_position", 0.6))
                braking_force = float(decision_payload.get("braking_force", 0.0))
                lean_angle = float(decision_payload.get("lean_angle", decision_payload.get("lean_angle_max", 25)))

                base_speed = sector_avg_speed
                if braking_force > 0:
                    base_speed *= max(0.55, 1.0 - 0.5 * braking_force)
                speed_kmh = base_speed * (0.8 + 0.25 * throttle)
                speed_kmh += np.random.normal(0, 3.0)
                speed_kmh = float(np.clip(speed_kmh, 30.0, 330.0))
                
                telemetry = {
                    "frame": frame_num,
                    "timestamp": sim_time_s,
                    "speed_kmh": speed_kmh,
                    "lean_angle": lean_angle,
                    "throttle": throttle,
                    "confidence": confidence,
                    "tool": tool_used.name,
                    "decision_time_ms": decision_time
                }
                
                sector_telemetry.append(telemetry)
                sector_decisions.append(decision)
                
                # Verbose output
                if verbose and frame_num % 10 == 0:
                    tool_str = "CAG (cache)" if tool_used == ToolType.CAG else "RAG (retrieval)"
                    print(f"    Frame {frame_num:2d}: Conf={confidence:.2f} | "
                          f"Tool={tool_str:15s} | Speed={speed_kmh:6.1f}km/h | "
                          f"Time={decision_time:5.1f}ms")
                
                lap_results["total_frames"] += 1
                sim_time_s += dt_frame
            
            # Store sector results
            lap_results["sector_telemetry"].append({
                "sector_id": sector_id,
                "sector_name": sector_name,
                "duration_s": sector_time_s,
                "frames_processed": len(sector_telemetry),
                "avg_speed_kmh": np.mean([t["speed_kmh"] for t in sector_telemetry]),
                "telemetry": sector_telemetry
            })
            
            if verbose:
                avg_conf = np.mean([t["confidence"] for t in sector_telemetry])
                cag_ratio = sum(1 for t in sector_telemetry if t["tool"] == "CAG") / len(sector_telemetry)
                print(f"  Summary: Avg Confidence={avg_conf:.3f} | CAG Usage={cag_ratio*100:.1f}%")
        
        # Compute lap statistics
        total_lap_time_s = float(np.sum(sector_times))
        
        agent_stats = self.agent.get_statistics()
        
        lap_results["performance_metrics"] = {
            "total_lap_time_s": total_lap_time_s,
            "avg_frame_time_ms": (total_lap_time_s * 1000 / lap_results["total_frames"]),
            "fps": lap_results["total_frames"] / max(total_lap_time_s, 0.001),
            "cag_usage_percent": agent_stats["cag_usage_percent"],
            "rag_usage_percent": agent_stats["rag_usage_percent"],
            "memory_hit_rate": agent_stats["memory_hit_rate"],
            "avg_decision_time_ms": agent_stats["avg_decision_time_ms"],
            "latency_reduction_percent": agent_stats["latency_reduction_percent"]
        }
        
        if verbose:
            print("\n" + "=" * 70)
            print("LAP COMPLETE - Performance Summary")
            print("=" * 70)
            print(f"Total Lap Time (simulado): {total_lap_time_s:.2f}s")
            print(f"Frames Processed: {lap_results['total_frames']}")
            print(f"Average FPS (simulado): {lap_results['performance_metrics']['fps']:.1f}")
            print(f"CAG Usage (Cache Hits): {agent_stats['cag_usage_percent']:.1f}%")
            print(f"RAG Usage (Retrievals): {agent_stats['rag_usage_percent']:.1f}%")
            print(f"Average Decision Time: {agent_stats['avg_decision_time_ms']:.2f}ms")
            print(f"Latency Reduction vs RAG-only: {agent_stats['latency_reduction_percent']:.1f}%")
            print("=" * 70)
        
        return lap_results
    
    def save_results(self, results: Dict, output_path: str = "lap_results.json"):
        """Save lap results to JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert numpy types to Python native types for JSON serialization
        def convert_types(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            return obj
        
        results_serializable = convert_types(results)
        
        with open(output_file, 'w') as f:
            json.dump(results_serializable, f, indent=2)
        
        print(f"\n✓ Results saved to {output_file}")


def main():
    """Main entry point for lap simulation."""
    
    print("\n╔════════════════════════════════════════════════════════════════════╗")
    print("║     Agentic Racing Vision - RAG/CAG Hybrid Memory System         ║")
    print("║                  High-Performance Motorsport AI                  ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    try:
        # Initialize pipeline
        pipeline = RacingInferencePipeline(
            config_path="data/aspar_circuit_config.json",
            confidence_threshold=0.85,
            device="cpu"  # Change to "cuda" if GPU available
        )
        
        # Run lap simulation
        lap_results = pipeline.run_lap_simulation(
            num_sectors_per_lap=8,  # Full circuit
            frames_per_sector=30,
            verbose=True
        )
        
        # Save results
        pipeline.save_results(lap_results, output_path="lap_results.json")
        
        print("\n✓ Lap simulation completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error during simulation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
