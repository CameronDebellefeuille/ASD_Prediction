import matplotlib.pyplot as plt
import pandas as pd

# Data for the table
data = {
    "Metric": [
        "Accuracy",
        "95% CI",
        "Sensitivity",
        "Specificity",
        "Balanced Accuracy",
        "Precision",
        "P-value"
    ],
    "Value": [
        "95.8%",
        "78.9–99.9%",
        "100%",
        "88.9%",
        "94.4%",
        "93.8%",
        "< 0.001"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(6, 5)) # Adjust size as needed

# Hide the axes
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)

# Create the table
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='left', loc='center')

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.8) # Scale width and height

# Remove all cell borders
for key, cell in table.get_celld().items():
    cell.set_linewidth(0)

# Add specific lines (Scientific / Booktabs style)
# Top line, Header bottom line, Bottom line

for (row, col), cell in table.get_celld().items():
    row_count = len(df)
    
    # Header row
    if row == 0:
        cell.set_text_props(weight='bold')
        cell.visible_edges = 'TB' # Top and Bottom of header
        cell.set_linewidth(1.5)
    
    # Last row
    elif row == row_count:
        cell.visible_edges = 'B' # Bottom of table
        cell.set_linewidth(1.5)
    
    # Other rows
    else:
        cell.visible_edges = 'open' # No borders


plt.savefig('publication_table.png', bbox_inches='tight', dpi=300)
plt.show() # Commented out for non-interactive env

