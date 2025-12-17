import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the GDP data
df = pd.read_csv('3610043403-eng.csv', skiprows=11)

# Find the relevant industries
industries_to_compare = {
    'Construction': None,
    'Agriculture, forestry, fishing and hunting': None
}

# Find row indices for each industry
for idx, row in df.iterrows():
    industry_name = str(row.iloc[0])
    for key in industries_to_compare.keys():
        if key in industry_name:
            industries_to_compare[key] = idx
            break

print("Found industries:")
for name, idx in industries_to_compare.items():
    print(f"  {name}: row {idx}")

# Extract 2024 data (most recent complete year)
industry_names = []
gdp_values = []

for name, idx in industries_to_compare.items():
    if idx is not None:
        # Column for 2024 should be at position -2 (second to last, as 2025 might be incomplete)
        value_2024 = df.iloc[idx, -2]  # 2024 column
        if value_2024 not in ['.', '..', '']:
            try:
                gdp_float = float(value_2024.replace(',', ''))
                industry_names.append(name)
                gdp_values.append(gdp_float)
            except (ValueError, AttributeError):
                pass

# Sort by GDP value (descending)
sorted_data = sorted(zip(industry_names, gdp_values), key=lambda x: x[1], reverse=True)
industry_names = [x[0] for x in sorted_data]
gdp_values = [x[1] for x in sorted_data]

# Create the bar chart
fig, ax = plt.subplots(figsize=(14, 8))

# Create bars
bars = ax.barh(industry_names, gdp_values, color='black', edgecolor='black', linewidth=1)

# Add value labels on the bars
for i, (name, value) in enumerate(zip(industry_names, gdp_values)):
    ax.text(value + 5000, i, f'${value:,.0f}M', 
            va='center', fontsize=11, fontweight='bold')

# Add title and labels
ax.set_title('Canadian Industry GDP Comparison (2024)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('GDP (millions of chained 2017 dollars)', fontsize=13)
ax.set_ylabel('Industry', fontsize=13)

# Extend x-axis to accommodate labels
ax.set_xlim(0, max(gdp_values) * 1.15)

# Format the axes
ax.grid(True, alpha=0.3, linestyle='--', color='gray', axis='x')
ax.set_axisbelow(True)

# Format x-axis to show values in thousands
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}B'))

plt.tight_layout()

# Print summary statistics
print("\n=== Canadian Industry GDP Comparison (2024) ===")
print("\nGDP by Industry (millions of chained 2017 dollars):")
for name, value in zip(industry_names, gdp_values):
    print(f"  {name}: ${value:,.0f}M (${value/1000:.1f}B)")

print(f"\nTotal GDP of selected industries: ${sum(gdp_values):,.0f}M (${sum(gdp_values)/1000:.1f}B)")

# Get total GDP from the All industries row
total_gdp_row = df[df.iloc[:, 0].str.contains('All industries  \[T001\]', na=False)]
if not total_gdp_row.empty:
    total_gdp_value = total_gdp_row.iloc[0, -2]
    if isinstance(total_gdp_value, str):
        total_gdp_2024 = float(total_gdp_value.replace(',', ''))
    else:
        total_gdp_2024 = float(total_gdp_value)
    print(f"Total Canadian GDP (2024): ${total_gdp_2024:,.0f}M (${total_gdp_2024/1000:.1f}B)")
    
    print("\nShare of Total GDP:")
    for name, value in zip(industry_names, gdp_values):
        percentage = (value / total_gdp_2024) * 100
        print(f"  {name}: {percentage:.2f}%")
else:
    print("Could not find total GDP")

print("\n=== Key Comparisons ===")
construction_gdp = gdp_values[industry_names.index('Construction')]
forestry_gdp = gdp_values[industry_names.index('Agriculture, forestry, fishing and hunting')]
print(f"Construction is {construction_gdp/forestry_gdp:.1f}x larger than Agriculture/Forestry/Fishing/Hunting")

# Save the plot to images folder
plt.savefig('../../images/industry_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
