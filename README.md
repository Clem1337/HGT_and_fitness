# "HGT-Mediated Intra-species Functional Complementarity Facilitates Intra-species Fitness"

This repository contains custom scripts and source data used in the study:  

## 🧬 Project Overview

This project explores how horizontally transferred genes (HGT) contribute to functional complementarity and enhanced fitness within bacteria populations. The analyses combine genomic, transcriptomic, and experimental data to quantify intra-species interactions mediated by HGT events.

## 📁 Repository Structure

- `scripts/` – Custom analysis scripts written in Python and R.  
- `data/` – Source data including gene presence-absence matrices, transcriptomic results, and fitness measurements.  
- `results/` – Processed outputs and figures.  

## ⚙️ Environment

- **Python**: 3.9  
- **R**: 4.3.2 / 4.3.3  
- Key Python libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, etc.  
- Key R packages: `tidyverse`, `ggplot2`, `vegan`, `data.table`, etc.

We recommend using a virtual environment or Conda for dependency management.

## 📦 Setup

### Python Environment
```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
