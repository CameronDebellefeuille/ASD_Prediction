import biom
import pandas as pd

# Set paths
otu_path = r"C:\Users\21cd51\OneDrive - Queen's University\ASD_ML_proj\BIOM\otu_table.biom"
mapping_path = r"C:\Users\21cd51\OneDrive - Queen's University\ASD_ML_proj\mapping_file\13652_20230201-071723.txt"

# Load OTU table
otu_table = biom.load_table(otu_path)

# Load mapping file
mapping_df = pd.read_csv(mapping_path, sep="\t")

# Convert OTU table to dense dataframe
otu_df = otu_table.to_dataframe(dense=True)

# Transpose OTU table
otu_df = otu_df.T

# Keep only the necessary columns in mapping file
mapping_df = mapping_df[["sample_name", "diagnosis", "household"]]

# Set sample_name as index in mapping file
mapping_df = mapping_df.set_index("sample_name")

# Ensure sample IDs match
common_samples = otu_df.index.intersection(mapping_df.index)

otu_df = otu_df.loc[common_samples]
mapping_df = mapping_df.loc[common_samples]

# Join tables
otu_with_labels = otu_df.join(mapping_df)

# Print first few rows of OTU table with labels
print(otu_with_labels["diagnosis"].value_counts())
print(otu_with_labels["household"].value_counts())
print(otu_with_labels.head())

# Save OTU table with labels to CSV
otu_with_labels.to_csv("otu_table_with_labels.csv", index=True)
print(otu_with_labels.head())

