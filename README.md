# ASD Prediction via Maternal Gut Microbiome

A machine learning pipeline that predicts Autism Spectrum Disorder (ASD) in children using their **mothers' gut microbiome** composition. The model achieves **95.8% accuracy** with an AUC of **0.9704** on held-out test data.

## Research Overview

This project investigates whether maternal gut microbiota can serve as early predictive biomarkers for child ASD diagnosis — contributing to the broader gut-brain axis hypothesis in ASD etiology.

**Study design:** Case-control study using 16S rRNA gut microbiome data (V3-V4 region, Illumina MiSeq) from 246 Chinese family samples:

| Group | Description | n |
|-------|-------------|---|
| ASD | Children with autism | 73 |
| ASDM | Mothers of children with autism | 73 |
| TD | Typically developing children | 46 |
| TDM | Mothers of typically developing children | 46 |

The model is trained on **maternal OTU abundances** and predicts their **child's diagnosis (ASD vs. TD)**.

## Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 95.8% |
| Sensitivity | 100% |
| Specificity | 88.9% |
| Balanced Accuracy | 94.4% |
| Precision | 93.8% |
| AUC | 0.9704 |
| p-value | < 0.001 |

## Repository Structure

```
.
├── otu_model_train.Rmd                 # Main ML pipeline (data prep, GBM model, feature importance)
├── data_cleaning.py                    # Merges OTU table (.biom) with sample metadata
├── ml_performance.py                   # Generates publication-ready performance metrics table
├── confusion_matrix.py                 # Generates styled confusion matrix visualization
├── requirements.txt                    # Python dependencies
├── data_summary.txt                    # Dataset summary statistics
├── otu_table.biom                      # Raw OTU abundance table (6,195 OTUs × 246 samples)
├── otu_table_with_labels_header.csv    # Processed OTU table with numeric OTU IDs as column names
├── otu_table_with_labels_tax.csv       # Processed OTU table with full taxonomy strings as column names
├── 97_otu_taxonomy.txt                 # OTU taxonomy annotations (Greengenes database)
└── mapping_file/                       # Sample metadata (246 samples, 46 variables)
```

## Pipeline

### 1. Data Preparation (`data_cleaning.py`)
- Loads the `.biom` OTU table and sample metadata
- Merges OTU abundances with diagnostic labels
- Outputs two processed CSVs:
  - `otu_table_with_labels_header.csv` — numeric OTU IDs as column names
  - `otu_table_with_labels_tax.csv` — full taxonomy strings as column names

### 2. Model Training (`otu_model_train.Rmd`)
- Links mothers to children via household ID
- Sparsity filtering: keeps OTUs present in ≥10% of samples
- Log-transforms OTU counts (`log1p`)
- 80/20 stratified train-test split
- Trains a **Gradient Boosting Machine (GBM)** with 5-fold cross-validation

**GBM hyperparameters:**
```
n.trees = 500 | interaction.depth = 4 | shrinkage = 0.01 | cv.folds = 5
```

### 3. Feature Importance
- Extracts top 10 OTU biomarkers by relative influence
- Maps OTU IDs to bacterial taxonomy (Greengenes)
- Statistical validation with t-tests + Benjamini-Hochberg correction

### 4. Visualization (`confusion_matrix.py`, `ml_performance.py`)
- Styled confusion matrix with performance statistics
- Publication-ready metrics table
- Boxplots of top biomarkers by diagnosis group

## Getting Started

### Prerequisites
- R (≥ 4.0) with the following packages: `dplyr`, `tidyr`, `caret`, `gbm`, `pROC`, `ggplot2`, `gridExtra`
- Python 3.x

### Python Setup
```bash
# Clone the repository
git clone https://github.com/your-username/ASD_Prediction.git
cd ASD_Prediction

# Create and activate a virtual environment
python -m venv .venv
.venv/Scripts/activate        # Windows
source .venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Running the Pipeline
```bash
# Step 1: Process raw data (Python)
python data_cleaning.py

# Step 2: Train model and generate results (R)
# Open otu_model_train.Rmd in RStudio and knit, or run:
Rscript -e "rmarkdown::render('otu_model_train.Rmd')"

# Step 3: Generate visualizations (Python)
python confusion_matrix.py
python ml_performance.py
```

## Key Findings

- Specific bacterial taxa in maternal gut microbiota are significantly associated with child ASD status
- The GBM model identifies interpretable biomarkers that differentiate ASD and TD family groups
- Perfect sensitivity (100%) means no ASD cases were missed in the test set
- Results support the hypothesis that maternal microbiome composition has transgenerational neurodevelopmental implications
