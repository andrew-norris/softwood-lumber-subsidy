import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('raw-exports.csv', skiprows=3)

# Filter out rows with missing country data
df = df[df['Country'].notna()]

# Remove footer rows
df = df[df['Province'].notna()]

# Convert Value to numeric
df['Value ($)'] = pd.to_numeric(df['Value ($)'], errors='coerce')
df = df.dropna(subset=['Value ($)'])

# Classify exports as US or Rest of World
df['Region'] = df['Country'].apply(lambda x: 'United States' if x == 'United States' else 'Rest of World')

# Calculate total exports by region
region_totals = df.groupby('Region')['Value ($)'].sum()

# Calculate percentages
total = region_totals.sum()
percentages = (region_totals / total) * 100

# Create the pie chart
fig, ax = plt.subplots(figsize=(10, 8))

# Define colors (grayscale)
colors = ['#404040', '#BFBFBF']

# Create pie chart
wedges, texts, autotexts = ax.pie(region_totals, 
                                    labels=region_totals.index,
                                    autopct='%1.1f%%',
                                    startangle=90,
                                    colors=colors,
                                    textprops={'fontsize': 13, 'weight': 'bold'},
                                    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})

# Make percentage text white for better contrast
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(14)
    autotext.set_weight('bold')

# Add title
ax.set_title('Canadian Softwood Lumber Export Share by Destination\n(January 2017)', 
             fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()

# Print summary statistics
print("\n=== Canadian Softwood Lumber Export Share ===")
print(f"Period: January 2017")
print(f"\nTotal Export Value: ${total:,.0f}")
print("\nExport Share by Destination:")
for region in region_totals.index:
    value = region_totals[region]
    pct = percentages[region]
    print(f"  {region}: ${value:,.0f} ({pct:.1f}%)")

# Save the plot to images folder
plt.savefig('../../images/export_share_piechart.png', dpi=300, bbox_inches='tight')
plt.close()
