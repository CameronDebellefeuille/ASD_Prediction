# ASD Prediction via Gut Microbiome

Two parallel machine learning pipelines that predict Autism Spectrum Disorder (ASD) using gut microbiome composition — one using **maternal microbiome** data, one using **child microbiome** data directly. The maternal model achieves **95.8% accuracy** with an AUC of **0.9704** on held-out test data.

## Research Overview

This project investigates whether gut microbiota can serve as predictive biomarkers for child ASD diagnosis. Two approaches are compared: using the **child's own microbiome** vs. using the **mother's microbiome** to predict the child's outcome — contributing to the broader gut-brain axis hypothesis in ASD etiology.

**Study design:** Case-control study using 16S rRNA gut microbiome data (V3-V4 region, Illumina MiSeq) from 246 Chinese family samples:

| Group | Description | n |
|-------|-------------|---|
| ASD | Children with autism | 73 |
| ASDM | Mothers of children with autism | 73 |
| TD | Typically developing children | 46 |
| TDM | Mothers of typically developing children | 46 |

Two models are trained on OTU abundances and predict **child diagnosis (ASD vs. TD)**:
- **Maternal model** — uses mother's OTU features, linked to child outcome via household ID
- **Child model** — uses child's own OTU features directly

## Model Comparison

| Metric | Maternal Microbiome | Child Microbiome |
|--------|--------------------|--------------------|
| Accuracy | 95.8% | 83.3% |
| Sensitivity | 100% | 86.7% |
| Specificity | 88.9% | 77.8% |
| Balanced Accuracy | 94.4% | 86.7 |
| Precision | 93.8% | 77.8% |
| AUC | 0.9704 | 0.9333 |
| p-value | < 0.001 | 0.02 |

## Repository Structure

```
.
├── otu_model_train.Rmd                 # ML pipeline using maternal microbiome data
├── child_otu_model_train.Rmd           # ML pipeline using child microbiome data
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

### 2a. Maternal Model (`otu_model_train.Rmd`)
- Filters for mother samples (`ASDM`, `TDM`)
- Joins child diagnosis onto maternal rows via household ID
- Uses **mother OTU features** to predict child outcome

### 2b. Child Model (`child_otu_model_train.Rmd`)
- Filters for child samples (`ASD`, `TD`) directly
- No join required — child diagnosis is the target
- Uses **child OTU features** to predict their own diagnosis

Both models apply identical preprocessing and training:
- Sparsity filtering: keeps OTUs present in ≥10% of samples
- Log-transforms OTU counts (`log1p`)
- 80/20 stratified train-test split
- **Gradient Boosting Machine (GBM)** with 5-fold cross-validation

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

# Step 2: Train models and generate results (R)
# Open either .Rmd in RStudio and knit, or run:
Rscript -e "rmarkdown::render('otu_model_train.Rmd')"       # Maternal model
Rscript -e "rmarkdown::render('child_otu_model_train.Rmd')" # Child model

# Step 3: Generate visualizations (Python)
python confusion_matrix.py
python ml_performance.py
```

## Key Findings

- The maternal model achieves 95.8% accuracy with perfect sensitivity (100%) — no ASD cases missed
- Specific bacterial taxa in maternal gut microbiota are significantly associated with child ASD status
- Running the same pipeline on child microbiome data enables a direct comparison of predictive power between maternal and child gut signatures
- Results contribute to the gut-brain axis hypothesis and the potential for transgenerational microbiome-based ASD biomarkers

<img width="4608" height="3456" alt="CUCOH Poster - Predicting ASD" src="https://github.com/user-attachments/assets/9db0413a-7ace-43e6-b1ac-78151f2130ed" />
