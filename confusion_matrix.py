import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap

# 1. Define your confusion matrix data
# Rows = Observed, Columns = Predicted
data = np.array([[15, 0], 
                 [1, 8]])

# 2. Create labels
labels = ['ASD', 'TD']
df_cm = pd.DataFrame(data, index=labels, columns=labels)

# Create a color mask: 1 for diagonal (correct), 0 for off-diagonal (incorrect)
# This allows us to strictly control the 2 box colors regardless of count values
color_data = np.eye(2) 
df_colors = pd.DataFrame(color_data, index=labels, columns=labels)

# 3. Plotting
plt.figure(figsize=(7.6, 7.6))
sns.set_theme(style="white")

# Define custom 2-color map: Off-white for 0, Blue #143a6d for 1
off_white = "#f7f7f7"
brand_blue = "#143a6d"
cmap = ListedColormap([off_white, brand_blue])

# Create heatmap using color_data for colors, but data for numbers
ax = sns.heatmap(df_colors, annot=df_cm, fmt='d', cmap=cmap, cbar=False,
                 annot_kws={"size": 24, "weight": "bold"},
                 linewidths=1, linecolor='white')

# Manually adjust text colors for contrast
# Loop over the text annotations and set color based on the cell value
# Since we used a binary mask: 1 (Diagonal) -> Blue background -> White text
# 0 (Off-diagonal) -> White background -> Dark text
for text, val in zip(ax.texts, color_data.flatten()):
    if val == 1:
        text.set_color("white")
    else:
        text.set_color("#333333")

# 4. Add titles and labels
plt.xlabel('Predicted Diagnosis', fontsize=14, labelpad=15, weight='bold')
plt.ylabel('Observed Diagnosis', fontsize=14, labelpad=15, weight='bold')

# Customize tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12, rotation=0)

# 5. Add stats as a footnote
stats_text = f"AUC: 0.9704\nMisclassification Rate: 0.0417"
plt.figtext(0.5, 0.02, stats_text, ha="center", fontsize=14, 
            bbox={"facecolor":"#f0f0f0", "alpha":0.5, "pad":10, "edgecolor": brand_blue, "boxstyle": "round,pad=0.5"})

plt.tight_layout()
plt.subplots_adjust(bottom=0.2)
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
print("Confusion matrix saved as 'confusion_matrix.png'")
plt.show()