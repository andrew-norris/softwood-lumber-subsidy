import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the value exports CSV file
df_value = pd.read_csv('exports/value-exports.csv', skiprows=4)
df_value.columns = ['Date', 'Value']
df_value = df_value[df_value['Date'].notna()]
df_value = df_value[df_value['Date'].str.contains(r'^[A-Z][a-z]{2}-\d{2}$', na=False)]
df_value['Date'] = pd.to_datetime(df_value['Date'], format='%b-%y')
df_value['Value'] = pd.to_numeric(df_value['Value'], errors='coerce')
df_value = df_value.dropna()
df_value = df_value.sort_values('Date')

# Read the volume exports CSV file
df_volume = pd.read_csv('exports/volume-exports.csv', skiprows=5)
df_volume.columns = ['Date', 'Volume']
df_volume = df_volume[df_volume['Date'].notna()]
df_volume = df_volume[df_volume['Date'].str.contains(r'^[A-Z][a-z]{2}-\d{2}$', na=False)]
df_volume['Date'] = pd.to_datetime(df_volume['Date'], format='%b-%y')
df_volume['Volume'] = pd.to_numeric(df_volume['Volume'], errors='coerce')
df_volume = df_volume.dropna()
df_volume = df_volume.sort_values('Date')

# Merge the two dataframes on Date
df = pd.merge(df_value, df_volume, on='Date', how='inner')

# Calculate base month (first month in dataset) values
base_value = df.iloc[0]['Value']
base_volume = df.iloc[0]['Volume']

# Create indices (first month = 100)
df['Value_Index'] = (df['Value'] / base_value) * 100
df['Volume_Index'] = (df['Volume'] / base_volume) * 100

# Calculate annual averages for summary
df['Year'] = df['Date'].dt.year
annual_value_index = df.groupby('Year')['Value_Index'].mean()
annual_volume_index = df.groupby('Year')['Volume_Index'].mean()

# Create the plot
fig, ax = plt.subplots(figsize=(16, 8))

# Plot both indices
ax.plot(df['Date'], df['Value_Index'], linewidth=2, color='black', 
        label='Export Value Index')
ax.plot(df['Date'], df['Volume_Index'], linewidth=2, color='gray', linestyle='--',
        label='Export Volume Index')

# Add horizontal line at 100 (base month)
ax.axhline(y=100, color='black', linestyle=':', linewidth=1, alpha=0.5)

# Add title and labels
ax.set_title('Softwood Lumber Export Value and Volume Indices (February 2012=100)', 
             fontsize=24, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=20)
ax.set_ylabel('Index (February 2012 = 100)', fontsize=20)

# Add legend
ax.legend(loc='best', fontsize=17, frameon=True, fancybox=False, edgecolor='black')

# Format the axes
ax.grid(True, alpha=0.3, linestyle='--', color='gray')

# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Print summary statistics
print("\n=== Softwood Lumber Export Indices Summary ===")
print(f"Time Period: {df['Date'].min().strftime('%B %Y')} to {df['Date'].max().strftime('%B %Y')}")
print(f"Base Month: {df['Date'].min().strftime('%B %Y')} (Index = 100)")
print(f"\nBase Month Values:")
print(f"  Export Value: ${base_value:,.0f}")
print(f"  Export Volume: {base_volume:,.0f} cubic metres")

print("\n=== Latest Values (January 2017) ===")
latest = df[df['Date'] == df['Date'].max()].iloc[0]
print(f"  Value Index: {latest['Value_Index']:.1f}")
print(f"  Volume Index: {latest['Volume_Index']:.1f}")

print("\n=== Annual Average Indices ===")
years = sorted(annual_value_index.index)
for year in years:
    if year != 2017:  # Skip partial 2017 data
        print(f"{year}: Value={annual_value_index[year]:.1f}, Volume={annual_volume_index[year]:.1f}")

# Save the plot to images folder
plt.savefig('../images/export_value_graph.png', dpi=300, bbox_inches='tight')
plt.close()
