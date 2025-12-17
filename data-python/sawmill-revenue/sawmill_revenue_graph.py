import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('1610011701-eng.csv', skiprows=10)

# Extract the row for "Revenue from goods manufactured"
revenue_row = df[df.iloc[:, 0].str.contains('Revenue from goods manufactured', na=False, regex=False)]

# Get the years from column names (starting from column 1)
year_columns = [col for col in df.columns[1:] if col.strip() and col.strip().isdigit()]
years = [int(col) for col in year_columns]

# Get the revenue values
revenue_values = []
for year_col in year_columns:
    val = revenue_row[year_col].values[0] if len(revenue_row) > 0 else np.nan
    
    # Clean the value (remove quality indicators and convert to float)
    if pd.notna(val) and str(val).strip() and str(val) not in ['F', '..']:
        val_str = str(val).replace('A', '').replace('B', '').replace('C', '') \
                         .replace('D', '').replace('E', '').replace('F', '').strip()
        try:
            revenue_values.append(float(val_str.replace(',', '')))
        except:
            revenue_values.append(np.nan)
    else:
        revenue_values.append(np.nan)

# Filter out NaN values
valid_indices = ~np.isnan(revenue_values)
years_filtered = np.array(years)[valid_indices]
revenue_filtered = np.array(revenue_values)[valid_indices]

# Convert to billions of dollars for easier reading
revenue_billions = revenue_filtered / 1_000_000

# Create the plot
fig, ax = plt.subplots(figsize=(12, 7))

# Plot the data
ax.plot(years_filtered, revenue_billions, linewidth=2, color='black')

# Add title and labels
ax.set_title('Sawmill Revenue from Goods Manufactured in Canada (2013-2023)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Revenue (billions of dollars)', fontsize=12)

# Format the axes
ax.grid(True, alpha=0.3, linestyle='--', color='gray')
ax.set_xticks(years_filtered)
ax.set_xticklabels(years_filtered, rotation=0)

# Format y-axis to show currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.1f}B'))

plt.tight_layout()

# Print summary statistics
print("\n=== Sawmill Revenue Summary Statistics ===")
print(f"Time Period: {years_filtered[0]} to {years_filtered[-1]}")
print(f"Mean Revenue: ${revenue_billions.mean():.2f} billion")
print(f"Maximum Revenue: ${revenue_billions.max():.2f} billion (Year {years_filtered[np.argmax(revenue_billions)]})")
print(f"Minimum Revenue: ${revenue_billions.min():.2f} billion (Year {years_filtered[np.argmin(revenue_billions)]})")
print(f"Latest (2023): ${revenue_billions[-1]:.2f} billion")

print("\n=== Annual Revenue ===")
for year, revenue in zip(years_filtered, revenue_billions):
    print(f"{year}: ${revenue:.2f} billion")

# Calculate growth rates
print("\n=== Year-over-Year Growth Rates ===")
for i in range(1, len(years_filtered)):
    growth_rate = ((revenue_billions[i] - revenue_billions[i-1]) / revenue_billions[i-1]) * 100
    print(f"{years_filtered[i-1]} to {years_filtered[i]}: {growth_rate:+.1f}%")

# Save the plot to images folder
plt.savefig('../../images/sawmill_revenue_graph.png', dpi=300, bbox_inches='tight')
plt.close()
