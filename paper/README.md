# Paper - J. Imaging Submission

## Overview

This directory contains the manuscript for submission to **J. Imaging (MDPI)** - a high-impact open-access journal covering imaging science and technology.

**Title**: *Agentic-Racing-Vision: Hybrid RAG-CAG Architecture for High-Performance Motorsport Perception*

## Files

- **main.tex** - Complete LaTeX manuscript with all sections
- **references.bib** - BibTeX bibliography with 20+ citations
- **figures/** - Directory for TikZ figures and images

## Manuscript Structure

```
1. Abstract
2. Introduction
   - Contributions
   - Paper Organization
3. Related Work
   - Agent-Based Vision Systems
   - Retrieval-Augmented Generation
   - Cache-Based Knowledge Systems
   - Vision Architectures
   - Motorsport Perception Systems
4. Methodology
   - System Overview
   - ReAct Agent Orchestrator
   - Memory Systems (CAG & RAG)
   - NestedUNet Vision Encoder
5. Experimental Setup
   - Dataset (Aspar Circuit)
   - Implementation Details
   - Baselines
   - Metrics
6. Results
   - Latency Analysis
   - Accuracy Analysis
   - Cache Hit Analysis
   - Throughput
7. Conclusion
   - Limitations
   - Future Work
   - Broader Impact
8. Bibliography
```

## Compilation Instructions

### Prerequisites

Install a LaTeX distribution:

**Ubuntu/Debian**:
```bash
sudo apt-get install texlive-latex-full texlive-fonts-recommended cm-super dvipng
```

**macOS** (using Homebrew):
```bash
brew install mactex
```

**Windows**: Download and install [MiKTeX](https://miktex.org/) or [TeX Live](https://tug.org/texlive/)

### Compiling the Manuscript

**Option 1: Using pdflatex (recommended)**
```bash
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex main.aux
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

**Option 2: Using latexmk (automatic)**
```bash
cd paper
latexmk -pdf -bibtex main.tex
```

**Option 3: Using Make (if available)**
```bash
cd ..
make docs
```

This will generate `main.pdf` with proper bibliography and cross-references.

### Output

After compilation, you will have:
- `main.pdf` - Final compiled manuscript (ready for submission)
- `main.aux` - Auxiliary file (created during compilation)
- `main.log` - Compilation log
- `main.bbl` - Bibliography entries
- `main.blg` - Bibliography log

## Submission Guidelines for J. Imaging

### MDPI Format Requirements

1. **Page Layout**: A4 page size, 2.5 cm margins
2. **Font**: Times New Roman, 12pt for main text
3. **Line Spacing**: Double spacing in submission
4. **Title**: Concise, descriptive (no more than 12 words)
5. **Abstract**: 150-200 words, structured format
6. **Keywords**: 4-6 keywords, separated by semicolons
7. **Sections**: Use numbered sections (1., 2., etc.)
8. **Equations**: Numbered and centered
9. **Figures**: High-quality (300 dpi minimum), with descriptive captions
10. **Tables**: Clear formatting with descriptive captions
11. **References**: Numbered and in alphabetical order

### Customization for MDPI

The current `main.tex` uses IEEE format. To adapt for MDPI:

1. Replace the document class with MDPI template (available on MDPI website)
2. Update formatting for MDPI guidelines
3. Ensure all figure and table captions meet MDPI standards
4. Verify reference format matches MDPI requirements

### Current Template

The manuscript is currently formatted for a general high-quality journal. Contact the authors or MDPI for their official LaTeX template before final submission.

## Figures and Diagrams

### Adding Figures

Place TikZ or imported images in the `figures/` directory:

```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/architecture.pdf}
    \caption{System architecture showing the four integrated components.}
    \label{fig:architecture}
\end{figure}
```

### TikZ Diagrams

The manuscript includes placeholder TikZ diagrams (e.g., the ReAct loop). To generate high-quality PDF figures:

```bash
cd figures
pdflatex --shell-escape diagram_name.tex
```

## Bibliography Management

The `references.bib` file contains all citations in BibTeX format. To add new references:

1. Add entry to `references.bib`:
```bibtex
@article{author2025title,
  title={Title of the Article},
  author={Author, A. and Coauthor, B.},
  journal={Journal Name},
  year={2025},
  volume={1},
  pages={1--10}
}
```

2. Cite in the manuscript:
```latex
As shown in \cite{author2025title}, ...
```

3. Recompile to update bibliography.

## Common Issues and Solutions

### Issue: Bibliography not appearing
**Solution**: Run `bibtex main.aux` between pdflatex compilations

### Issue: Cross-references showing ??
**Solution**: Compile LaTeX twice to resolve all cross-references

### Issue: Figures not displaying
**Solution**: 
- Check figure paths are relative to paper directory
- Ensure image files exist in figures/ subdirectory
- For EPS figures, use `epstopdf` to convert to PDF

### Issue: Special characters not displaying
**Solution**: Ensure UTF-8 encoding in editor. Add to preamble:
```latex
\usepackage[utf8]{inputenc}
```

## Submission Checklist

- [ ] Manuscript compiled without errors
- [ ] All cross-references resolved (no ?? marks)
- [ ] Bibliography complete and properly formatted
- [ ] All figures have captions and are referenced
- [ ] All tables have captions and are referenced
- [ ] Author information is current
- [ ] Manuscript follows MDPI format guidelines
- [ ] Spelling and grammar checked
- [ ] All equations are numbered
- [ ] File size < 50MB for online submission

## Contact Information

For questions about the manuscript:
- Check README.md in root directory
- Review main.tex for implementation details
- See ../STRUCTURE.md for project architecture
- Consult ../TESTING.md for experimental validation

## Version History

- **v1.0** (December 2025): Initial manuscript draft
  - Complete methodology section
  - Experimental setup and results
  - 20+ citations included
  - Ready for review and feedback

---

**Last Updated**: December 29, 2025
**Status**: Ready for submission preparation
**Target Journal**: J. Imaging (MDPI)
**Estimated Page Count**: 12-15 pages
