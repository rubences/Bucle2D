"""
Memory Systems: CAG (Cache-Augmented Generation) and RAG (Retrieval-Augmented Generation)

This module implements the dual-memory architecture for the racing agent system:
- CAGMemory: Static Key-Value cache for predefined circuit characteristics
- RAGSystem: Dynamic vector-based retrieval for novel racing scenarios
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from scipy.spatial.distance import cosine
from pathlib import Path


@dataclass
class TelemetryRecord:
    """Represents a single telemetry measurement record."""
    timestamp: float
    sector: str
    speed_kmh: float
    lean_angle: float
    throttle_position: float
    braking_force: float
    g_lateral: float
    g_longitudinal: float
    confidence: float


class CAGMemory:
    """
    Cache-Augmented Generation Memory System.
    
    Stores static, pre-indexed circuit information for rapid lookup.
    Designed for high-frequency access with minimal latency.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize CAG Memory.
        
        Args:
            config_path: Path to circuit configuration JSON file
        """
        self.cache = {}
        self.sector_index = {}
        self.access_count = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
        if config_path and Path(config_path).exists():
            self._load_circuit_config(config_path)
        else:
            self._initialize_default_cache()
    
    def _load_circuit_config(self, config_path: str):
        """Load circuit configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Index sectors
            if "sectors" in config:
                for sector in config["sectors"]:
                    sector_id = sector["id"]
                    self.sector_index[sector_id] = sector
                    self.cache[f"sector_{sector_id}"] = sector
                    self.access_count[f"sector_{sector_id}"] = 0
            
            # Store metadata
            self.cache["circuit_metadata"] = config.get("circuit_metadata", {})
            self.cache["hazards"] = config.get("static_hazards", [])
            self.cache["benchmarks"] = config.get("telemetry_benchmarks", {})
            
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            self._initialize_default_cache()
    
    def _initialize_default_cache(self):
        """Initialize with default Aspar Circuit data."""
        self.cache = {
            "circuit_metadata": {
                "name": "Aspar Circuit",
                "track_length_km": 3.2,
                "num_sectors": 8
            },
            "sector_Sector_1": {
                "id": "Sector_1",
                "name": "Straight_Main",
                "avg_speed_kmh": 240,
                "banking_degrees": 0.0,
                "optimal_throttle": 0.95,
                "optimal_lean_angle": 5.0
            },
            "sector_Sector_2": {
                "id": "Sector_2",
                "name": "Turn_1_Braking",
                "avg_speed_kmh": 95,
                "banking_degrees": 2.5,
                "optimal_throttle": 0.0,
                "optimal_lean_angle": 45.0,
                "braking_intensity": "hard"
            },
            "sector_Sector_3": {
                "id": "Sector_3",
                "name": "Turn_2_Apex",
                "avg_speed_kmh": 120,
                "banking_degrees": 0.0,
                "optimal_throttle": 0.3,
                "optimal_lean_angle": 62.0
            },
            "sector_Sector_4": {
                "id": "Sector_4",
                "name": "Turn_4_Banking",
                "avg_speed_kmh": 210,
                "banking_degrees": 15.0,
                "optimal_throttle": 0.7,
                "optimal_lean_angle": 48.0,
                "critical": True
            },
            "sector_Sector_5": {
                "id": "Sector_5",
                "name": "Straight_Secondary",
                "avg_speed_kmh": 230,
                "banking_degrees": 0.0,
                "optimal_throttle": 0.95,
                "optimal_lean_angle": 8.0
            },
            "sector_Sector_6": {
                "id": "Sector_6",
                "name": "Turn_6_Tight",
                "avg_speed_kmh": 85,
                "banking_degrees": -2.0,
                "optimal_throttle": 0.2,
                "optimal_lean_angle": 64.0
            },
            "sector_Sector_7": {
                "id": "Sector_7",
                "name": "Turn_8_Banking",
                "avg_speed_kmh": 190,
                "banking_degrees": 12.5,
                "optimal_throttle": 0.6,
                "optimal_lean_angle": 50.0,
                "critical": True
            },
            "sector_Sector_8": {
                "id": "Sector_8",
                "name": "Final_Straight",
                "avg_speed_kmh": 260,
                "banking_degrees": 0.0,
                "optimal_throttle": 1.0,
                "optimal_lean_angle": 3.0,
                "drs_zone": True
            }
        }
        
        # Initialize access counts
        for key in self.cache.keys():
            self.access_count[key] = 0
    
    def lookup(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Perform a cache lookup (constant time O(1)).
        
        Args:
            key: Cache key (e.g., "sector_Sector_1")
            
        Returns:
            Cached value or None if not found
        """
        if key in self.cache:
            self.cache_hits += 1
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        else:
            self.cache_misses += 1
            return None
    
    def get_sector(self, sector_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve sector information by ID.
        
        Args:
            sector_id: Sector identifier (e.g., "Sector_1")
            
        Returns:
            Sector data or None
        """
        return self.lookup(f"sector_{sector_id}")
    
    def get_all_sectors(self) -> Dict[str, Dict[str, Any]]:
        """Get all cached sector information."""
        return {k: v for k, v in self.cache.items() if k.startswith("sector_")}
    
    def get_hazards_in_sector(self, sector_id: str) -> List[Dict[str, Any]]:
        """Get static hazards for a specific sector."""
        hazards = self.cache.get("hazards", [])
        return [h for h in hazards if h.get("sector_id") == sector_id]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get cache access statistics."""
        total_accesses = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_accesses * 100) if total_accesses > 0 else 0.0
        
        return {
            "cache_size": len(self.cache),
            "total_hits": self.cache_hits,
            "total_misses": self.cache_misses,
            "hit_rate_percent": hit_rate,
            "most_accessed": max(self.access_count.items(), 
                                key=lambda x: x[1], 
                                default=("N/A", 0))[0] if self.access_count else "N/A"
        }


class RAGSystem:
    """
    Retrieval-Augmented Generation System.
    
    Implements vector-based semantic search over historical telemetry data.
    Uses cosine similarity to find relevant past scenarios and adapt decisions.
    """
    
    def __init__(self, embedding_dim: int = 512, max_memory: int = 10000):
        """
        Initialize RAG System.
        
        Args:
            embedding_dim: Dimension of telemetry embeddings
            max_memory: Maximum number of historical records to maintain
        """
        self.embedding_dim = embedding_dim
        self.max_memory = max_memory
        
        # Storage for embeddings and records
        self.embeddings: List[np.ndarray] = []
        self.records: List[TelemetryRecord] = []
        self.metadata: List[Dict[str, Any]] = []
        
        # Statistics
        self.retrieval_count = 0
        self.avg_similarity = 0.0
        
        self._initialize_synthetic_data()
    
    def _initialize_synthetic_data(self):
        """Initialize with synthetic historical telemetry for demonstration."""
        # Generate synthetic telemetry embeddings
        np.random.seed(42)
        
        sectors = [f"Sector_{i}" for i in range(1, 9)]
        
        for i in range(100):  # Create 100 synthetic records
            sector = sectors[i % 8]
            
            # Generate realistic telemetry values
            speed_kmh = 100 + np.random.normal(100, 30)
            lean_angle = np.random.uniform(0, 65)
            throttle = np.random.uniform(0, 1)
            braking = np.random.uniform(0, 1)
            g_lat = 0.5 + lean_angle / 65 * 1.5 + np.random.normal(0, 0.1)
            g_lon = abs(np.random.normal(0, 0.3))
            
            # Create embedding (simulate vision encoder output)
            embedding = np.random.randn(self.embedding_dim)
            embedding[0] = speed_kmh / 300  # Encode speed
            embedding[1] = lean_angle / 65   # Encode lean angle
            embedding[2] = throttle          # Encode throttle
            embedding[3] = braking           # Encode braking
            
            # Normalize
            embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
            
            # Create record
            record = TelemetryRecord(
                timestamp=i * 0.1,
                sector=sector,
                speed_kmh=float(np.clip(speed_kmh, 30, 280)),
                lean_angle=float(np.clip(lean_angle, 0, 65)),
                throttle_position=float(np.clip(throttle, 0, 1)),
                braking_force=float(np.clip(braking, 0, 1)),
                g_lateral=float(np.clip(g_lat, 0, 3)),
                g_longitudinal=float(np.clip(g_lon, 0, 3)),
                confidence=np.random.uniform(0.7, 1.0)
            )
            
            self.embeddings.append(embedding)
            self.records.append(record)
            self.metadata.append({
                "sector": sector,
                "timestamp": record.timestamp,
                "confidence": record.confidence
            })
    
    def retrieve(self, query_embedding: np.ndarray, 
                 k: int = 5,
                 sector_filter: Optional[str] = None) -> Tuple[List[TelemetryRecord], List[float]]:
        """
        Retrieve similar telemetry records using cosine similarity.
        
        Args:
            query_embedding: Query embedding (shape: (embedding_dim,))
            k: Number of top-k results to return
            sector_filter: Optional sector to filter results
            
        Returns:
            Tuple of (retrieved_records, similarity_scores)
        """
        assert query_embedding.shape[0] == self.embedding_dim, \
            f"Embedding dimension mismatch: expected {self.embedding_dim}, got {query_embedding.shape[0]}"
        
        k = min(k, len(self.records))
        
        # Normalize query embedding
        query_embedding = query_embedding / (np.linalg.norm(query_embedding) + 1e-8)
        
        # Compute similarity scores
        similarities = []
        for i, stored_embedding in enumerate(self.embeddings):
            # Cosine similarity: 1 - cosine_distance
            similarity = 1.0 - cosine(query_embedding, stored_embedding)
            similarities.append(similarity)
        
        # Apply sector filter if specified
        if sector_filter:
            filtered_indices = [i for i, meta in enumerate(self.metadata) 
                              if meta["sector"] == sector_filter]
            similarities = [similarities[i] if i in filtered_indices else -1.0 
                          for i in range(len(similarities))]
        
        # Get top-k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        # Retrieve records and scores
        retrieved_records = [self.records[i] for i in top_k_indices]
        retrieved_scores = [similarities[i] for i in top_k_indices]
        
        # Update statistics
        self.retrieval_count += 1
        self.avg_similarity = (self.avg_similarity * (self.retrieval_count - 1) + 
                              np.mean(retrieved_scores)) / self.retrieval_count
        
        return retrieved_records, retrieved_scores
    
    def retrieve_sector_history(self, sector_id: str, 
                               limit: int = 10) -> List[TelemetryRecord]:
        """
        Retrieve all historical records for a specific sector.
        
        Args:
            sector_id: Sector identifier
            limit: Maximum number of records to return
            
        Returns:
            List of telemetry records
        """
        sector_records = [r for r in self.records if r.sector == sector_id]
        return sector_records[-limit:]
    
    def add_record(self, embedding: np.ndarray, 
                  record: TelemetryRecord,
                  metadata: Dict[str, Any]):
        """
        Add a new telemetry record to the system (for online learning).
        
        Args:
            embedding: Visual embedding
            record: Telemetry record
            metadata: Associated metadata
        """
        if len(self.embeddings) >= self.max_memory:
            # Remove oldest record
            self.embeddings.pop(0)
            self.records.pop(0)
            self.metadata.pop(0)
        
        embedding_normalized = embedding / (np.linalg.norm(embedding) + 1e-8)
        self.embeddings.append(embedding_normalized)
        self.records.append(record)
        self.metadata.append(metadata)
    
    def get_sector_statistics(self, sector_id: str) -> Dict[str, Any]:
        """Get aggregate statistics for a sector."""
        sector_records = [r for r in self.records if r.sector == sector_id]
        
        if not sector_records:
            return {}
        
        speeds = [r.speed_kmh for r in sector_records]
        lean_angles = [r.lean_angle for r in sector_records]
        
        return {
            "sector": sector_id,
            "record_count": len(sector_records),
            "avg_speed_kmh": float(np.mean(speeds)),
            "max_speed_kmh": float(np.max(speeds)),
            "min_speed_kmh": float(np.min(speeds)),
            "avg_lean_angle": float(np.mean(lean_angles)),
            "max_lean_angle": float(np.max(lean_angles))
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get RAG system statistics."""
        return {
            "total_records": len(self.records),
            "total_retrievals": self.retrieval_count,
            "avg_similarity_score": float(self.avg_similarity),
            "embedding_dim": self.embedding_dim,
            "max_memory": self.max_memory
        }


if __name__ == "__main__":
    # Example usage
    print("=" * 60)
    print("CAG Memory System Demo")
    print("=" * 60)
    
    cag = CAGMemory()
    
    # Lookup sector information
    sector_1 = cag.get_sector("Sector_1")
    print(f"\nSector_1 Info: {sector_1}")
    
    # Get all sectors
    all_sectors = cag.get_all_sectors()
    print(f"\nTotal sectors cached: {len(all_sectors)}")
    
    # Print statistics
    print("\nCAG Statistics:")
    for key, value in cag.get_statistics().items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("RAG System Demo")
    print("=" * 60)
    
    rag = RAGSystem()
    
    # Create a query embedding
    query_embedding = np.random.randn(512)
    query_embedding[0] = 0.8  # High speed scenario
    query_embedding[1] = 0.7  # High lean angle
    
    # Retrieve similar records
    records, scores = rag.retrieve(query_embedding, k=5, sector_filter="Sector_4")
    print(f"\nTop-5 similar records for Sector_4:")
    for i, (record, score) in enumerate(zip(records, scores)):
        print(f"  {i+1}. Speed: {record.speed_kmh:.1f} km/h, "
              f"Lean: {record.lean_angle:.1f}°, Similarity: {score:.3f}")
    
    # Sector statistics
    sector_stats = rag.get_sector_statistics("Sector_4")
    print(f"\nSector_4 Statistics:")
    for key, value in sector_stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    print("\nRAG Statistics:")
    for key, value in rag.get_statistics().items():
        print(f"  {key}: {value}")
