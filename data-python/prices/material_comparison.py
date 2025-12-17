import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the price index data
df = pd.read_csv('1810026601-eng.csv', skiprows=9)

# Find the rows for each material
lumber_row = None
steel_row = None
concrete_row = None

for idx, row in df.iterrows():
    product = str(row.iloc[0])
    if 'Softwood lumber (except tongue and groove' in product and lumber_row is None:
        lumber_row = idx
    elif 'Fabricated steel plate' in product:
        steel_row = idx
    elif 'Ready-mixed concrete' in product:
        concrete_row = idx

print(f"Lumber row: {lumber_row}, Steel row: {steel_row}, Concrete row: {concrete_row}")

# Extract the data for each material
lumber_data = df.iloc[lumber_row, 1:].values
steel_data = df.iloc[steel_row, 1:].values
concrete_data = df.iloc[concrete_row, 1:].values

# Get column names (dates)
date_columns = df.columns[1:]

# Create lists for the data
dates = []
lumber_values = []
steel_values = []
concrete_values = []

# Parse dates and values
for i, col in enumerate(date_columns):
    try:
        # Parse date from column name (e.g., "June 1990")
        date = pd.to_datetime(col, format='%B %Y')
        
        # Get values, skip if missing
        lumber_val = lumber_data[i]
        steel_val = steel_data[i]
        concrete_val = concrete_data[i]
        
        # Only include if all three have values
        if lumber_val not in ['.', '..', ''] and steel_val not in ['.', '..', ''] and concrete_val not in ['.', '..', '']:
            try:
                lumber_float = float(lumber_val)
                steel_float = float(steel_val)
                concrete_float = float(concrete_val)
                
                dates.append(date)
                lumber_values.append(lumber_float)
                steel_values.append(steel_float)
                concrete_values.append(concrete_float)
            except (ValueError, TypeError):
                pass
    except:
        pass

# Create dataframe
plot_df = pd.DataFrame({
    'Date': dates,
    'Lumber': lumber_values,
    'Steel': steel_values,
    'Concrete': concrete_values
})

# Filter to start from 2003 onwards
plot_df = plot_df[plot_df['Date'] >= '2003-01-01']

# Calculate indices (first month = 100)
base_lumber = plot_df['Lumber'].iloc[0]
base_steel = plot_df['Steel'].iloc[0]
base_concrete = plot_df['Concrete'].iloc[0]

plot_df['Lumber_Index'] = (plot_df['Lumber'] / base_lumber) * 100
plot_df['Steel_Index'] = (plot_df['Steel'] / base_steel) * 100
plot_df['Concrete_Index'] = (plot_df['Concrete'] / base_concrete) * 100

# Create the plot
fig, ax = plt.subplots(figsize=(16, 8))

# Plot all three indices
ax.plot(plot_df['Date'], plot_df['Lumber_Index'], linewidth=2, color='black', 
        label='Softwood Lumber')
ax.plot(plot_df['Date'], plot_df['Steel_Index'], linewidth=2, color='gray', linestyle='--',
        label='Fabricated Steel')
ax.plot(plot_df['Date'], plot_df['Concrete_Index'], linewidth=2, color='darkgray', linestyle=':',
        label='Ready-Mixed Concrete')

# Add horizontal line at 100 (base month)
ax.axhline(y=100, color='black', linestyle=':', linewidth=1, alpha=0.5)

# Add title and labels
ax.set_title(f'Construction Material Price Indices ({plot_df["Date"].iloc[0].strftime("%B %Y")}=100)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=13)
ax.set_ylabel(f'Price Index ({plot_df["Date"].iloc[0].strftime("%B %Y")} = 100)', fontsize=13)

# Add legend
ax.legend(loc='best', fontsize=11, frameon=True, fancybox=False, edgecolor='black')

# Format the axes
ax.grid(True, alpha=0.3, linestyle='--', color='gray')

# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Print summary statistics
print("\n=== Construction Material Price Index Comparison ===")
print(f"Time Period: {plot_df['Date'].min().strftime('%B %Y')} to {plot_df['Date'].max().strftime('%B %Y')}")
print(f"Base Month: {plot_df['Date'].min().strftime('%B %Y')} (Index = 100)")

print(f"\nBase Month Values (Index Points):")
print(f"  Lumber: {base_lumber:.1f}")
print(f"  Steel: {base_steel:.1f}")
print(f"  Concrete: {base_concrete:.1f}")

print(f"\nLatest Index Values ({plot_df['Date'].max().strftime('%B %Y')}):")
print(f"  Lumber: {plot_df['Lumber_Index'].iloc[-1]:.1f}")
print(f"  Steel: {plot_df['Steel_Index'].iloc[-1]:.1f}")
print(f"  Concrete: {plot_df['Concrete_Index'].iloc[-1]:.1f}")

print(f"\nTotal Change Since Base Month:")
print(f"  Lumber: {plot_df['Lumber_Index'].iloc[-1] - 100:+.1f} percentage points")
print(f"  Steel: {plot_df['Steel_Index'].iloc[-1] - 100:+.1f} percentage points")
print(f"  Concrete: {plot_df['Concrete_Index'].iloc[-1] - 100:+.1f} percentage points")

print(f"\nPeak Index Values:")
print(f"  Lumber: {plot_df['Lumber_Index'].max():.1f} ({plot_df.loc[plot_df['Lumber_Index'].idxmax(), 'Date'].strftime('%B %Y')})")
print(f"  Steel: {plot_df['Steel_Index'].max():.1f} ({plot_df.loc[plot_df['Steel_Index'].idxmax(), 'Date'].strftime('%B %Y')})")
print(f"  Concrete: {plot_df['Concrete_Index'].max():.1f} ({plot_df.loc[plot_df['Concrete_Index'].idxmax(), 'Date'].strftime('%B %Y')})")

print(f"\nAverage Annual Growth Rate (2003-2025):")
years_elapsed = (plot_df['Date'].max() - plot_df['Date'].min()).days / 365.25
lumber_cagr = ((plot_df['Lumber_Index'].iloc[-1] / 100) ** (1/years_elapsed) - 1) * 100
steel_cagr = ((plot_df['Steel_Index'].iloc[-1] / 100) ** (1/years_elapsed) - 1) * 100
concrete_cagr = ((plot_df['Concrete_Index'].iloc[-1] / 100) ** (1/years_elapsed) - 1) * 100
print(f"  Lumber: {lumber_cagr:.2f}% per year")
print(f"  Steel: {steel_cagr:.2f}% per year")
print(f"  Concrete: {concrete_cagr:.2f}% per year")

# Save the plot to images folder
plt.savefig('../../images/material_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
