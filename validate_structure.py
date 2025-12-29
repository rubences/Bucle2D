#!/usr/bin/env python3
"""
Validation script to verify the complete Agentic-Racing-Vision project structure.
Run this script to ensure all required files and directories are in place.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple


class ProjectValidator:
    """Validates the project structure and dependencies."""
    
    def __init__(self, root_path: str = "."):
        self.root = Path(root_path)
        self.errors = []
        self.warnings = []
        self.checks = []
    
    def check_file_exists(self, path: str, description: str = "") -> bool:
        """Check if a file exists."""
        full_path = self.root / path
        exists = full_path.is_file()
        status = "✓" if exists else "✗"
        desc_str = f" ({description})" if description else ""
        print(f"{status} {path}{desc_str}")
        
        if not exists:
            self.errors.append(f"Missing file: {path}")
        else:
            self.checks.append(f"File exists: {path}")
        
        return exists
    
    def check_directory_exists(self, path: str, description: str = "") -> bool:
        """Check if a directory exists."""
        full_path = self.root / path
        exists = full_path.is_dir()
        status = "✓" if exists else "✗"
        desc_str = f" ({description})" if description else ""
        print(f"{status} {path}/{desc_str}")
        
        if not exists:
            self.errors.append(f"Missing directory: {path}")
        else:
            self.checks.append(f"Directory exists: {path}")
        
        return exists
    
    def check_file_size(self, path: str, min_size: int = 100) -> bool:
        """Check if a file has minimum size."""
        full_path = self.root / path
        if not full_path.is_file():
            return False
        
        size = full_path.stat().st_size
        if size < min_size:
            self.warnings.append(f"File {path} is very small ({size} bytes)")
            return False
        
        print(f"  └─ {size:,} bytes")
        return True
    
    def check_python_syntax(self, path: str) -> bool:
        """Check if a Python file has valid syntax."""
        full_path = self.root / path
        if not full_path.is_file():
            return False
        
        try:
            with open(full_path, 'r') as f:
                compile(f.read(), str(full_path), 'exec')
            return True
        except SyntaxError as e:
            self.errors.append(f"Syntax error in {path}: {e}")
            return False
    
    def validate_structure(self):
        """Run all validation checks."""
        print("\n" + "=" * 70)
        print("AGENTIC-RACING-VISION PROJECT STRUCTURE VALIDATION")
        print("=" * 70)
        
        # Check root files
        print("\n[1] Root Files")
        print("-" * 70)
        self.check_file_exists("README.md", "Project overview")
        self.check_file_exists("requirements.txt", "Dependencies")
        self.check_file_exists("setup.py", "Package setup")
        self.check_file_exists(".gitignore", "Git ignore file")
        self.check_file_exists("STRUCTURE.md", "Structure documentation")
        self.check_file_exists("TESTING.md", "Testing guide")
        
        # Check directories
        print("\n[2] Directory Structure")
        print("-" * 70)
        self.check_directory_exists("src", "Source code")
        self.check_directory_exists("paper", "Manuscript")
        self.check_directory_exists("data", "Circuit data")
        self.check_directory_exists("paper/figures", "Figures directory")
        
        # Check source files
        print("\n[3] Source Code Files")
        print("-" * 70)
        self.check_file_exists("src/__init__.py", "Package init")
        self.check_file_exists("src/agent_orchestrator.py", "ReAct agent")
        self.check_file_exists("src/memory_systems.py", "Memory systems")
        self.check_file_exists("src/vision_encoder.py", "Vision encoder")
        self.check_file_exists("src/main_inference.py", "Inference pipeline")
        
        # Check paper files
        print("\n[4] Paper Files")
        print("-" * 70)
        self.check_file_exists("paper/main.tex", "LaTeX manuscript")
        self.check_file_exists("paper/references.bib", "Bibliography")
        
        # Check data files
        print("\n[5] Data Files")
        print("-" * 70)
        self.check_file_exists("data/aspar_circuit_config.json", "Circuit config")
        
        # Check file sizes
        print("\n[6] File Size Validation")
        print("-" * 70)
        self.check_file_size("src/agent_orchestrator.py", min_size=1000)
        self.check_file_size("src/memory_systems.py", min_size=1000)
        self.check_file_size("src/vision_encoder.py", min_size=1000)
        self.check_file_size("src/main_inference.py", min_size=1000)
        self.check_file_size("paper/main.tex", min_size=5000)
        
        # Check Python syntax
        print("\n[7] Python Syntax Validation")
        print("-" * 70)
        py_files = [
            "src/__init__.py",
            "src/agent_orchestrator.py",
            "src/memory_systems.py",
            "src/vision_encoder.py",
            "src/main_inference.py",
        ]
        
        for py_file in py_files:
            result = self.check_python_syntax(py_file)
            status = "✓" if result else "✗"
            print(f"{status} {py_file}")
        
        # Print summary
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print(f"✓ Checks passed: {len(self.checks)}")
        print(f"✗ Errors: {len(self.errors)}")
        print(f"⚠ Warnings: {len(self.warnings)}")
        
        if self.warnings:
            print("\nWarnings:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  ✗ {error}")
            return False
        
        print("\n✓ All validations passed! Project structure is complete.")
        return True
    
    def generate_summary(self):
        """Generate a summary of the project."""
        print("\n" + "=" * 70)
        print("PROJECT SUMMARY")
        print("=" * 70)
        
        # Count lines of code
        print("\n[Code Statistics]")
        total_lines = 0
        py_files = list(self.root.glob("src/*.py"))
        
        for py_file in sorted(py_files):
            try:
                with open(py_file, 'r') as f:
                    lines = len(f.readlines())
                    total_lines += lines
                    print(f"  {py_file.name:30s}: {lines:5d} lines")
            except Exception as e:
                print(f"  {py_file.name:30s}: Error reading file")
        
        print(f"  {'TOTAL (Python)':30s}: {total_lines:5d} lines")
        
        # Check LaTeX
        tex_file = self.root / "paper/main.tex"
        if tex_file.exists():
            with open(tex_file, 'r') as f:
                tex_lines = len(f.readlines())
            print(f"  {'paper/main.tex':30s}: {tex_lines:5d} lines")
        
        # Dependencies
        print("\n[Dependencies]")
        req_file = self.root / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                deps = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            print(f"  Total packages: {len(deps)}")
            print(f"  Key packages: torch, torchvision, numpy, scipy, scikit-learn")
        
        # Data files
        print("\n[Data Files]")
        data_dir = self.root / "data"
        if data_dir.exists():
            json_files = list(data_dir.glob("*.json"))
            for json_file in json_files:
                size_kb = json_file.stat().st_size / 1024
                print(f"  {json_file.name}: {size_kb:.1f} KB")
        
        print("\n" + "=" * 70)


def main():
    """Main entry point."""
    validator = ProjectValidator()
    
    # Run validation
    success = validator.validate_structure()
    
    # Generate summary
    validator.generate_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
