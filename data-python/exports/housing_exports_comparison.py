import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Read US housing starts data
housing = pd.read_csv('housing-starts/HOUST.csv')
housing['observation_date'] = pd.to_datetime(housing['observation_date'])
housing['Year'] = housing['observation_date'].dt.year

# Calculate annual average housing starts
annual_housing = housing.groupby('Year')['HOUST'].mean().reset_index()
annual_housing.columns = ['Year', 'Housing_Starts']

# Read Canadian lumber exports data
exports = pd.read_csv('exports/1610001801-eng.csv', skiprows=11, nrows=1)

# The data row has alternating pattern: year header, then 4 empty cols, repeat
# But the actual data is in one long row
data_row = exports.iloc[0]

# Extract values - pattern is: Total, Rail, Truck, Water (repeating)
# Start from column 1 (skip "Canada" label)
years = list(range(2000, 2025))  # Years from 2000 to 2024
total_exports = []

for i, year in enumerate(years):
    # Each year group has 4 values: Total, Rail, Truck, Water
    # Starting at column 1, then every 4 columns
    col_index = 1 + (i * 4)
    value = data_row.iloc[col_index]
    # Remove commas and convert to float
    if isinstance(value, str):
        value = float(value.replace(',', ''))
    else:
        value = float(value)
    total_exports.append(value)

print(f"Debug: Found {len(years)} years and {len(total_exports)} export values")
print(f"First few exports: {total_exports[:5]}")

# Create exports dataframe
df_exports = pd.DataFrame({'Year': years, 'Total_Exports': total_exports})

# Merge the two datasets
df = pd.merge(annual_housing, df_exports, on='Year', how='inner')

# Calculate base year (first year) values
base_housing = df.iloc[0]['Housing_Starts']
base_exports = df.iloc[0]['Total_Exports']

# Create indices (first year = 100)
df['Housing_Index'] = (df['Housing_Starts'] / base_housing) * 100
df['Exports_Index'] = (df['Total_Exports'] / base_exports) * 100

# Create the plot
fig, ax = plt.subplots(figsize=(16, 8))

# Plot both indices
ax.plot(df['Year'], df['Housing_Index'], linewidth=2, color='black', 
        label='US Housing Starts Index')
ax.plot(df['Year'], df['Exports_Index'], linewidth=2, color='gray', linestyle='--',
        label='Canadian Lumber Exports Index')

# Add horizontal line at 100 (base year)
ax.axhline(y=100, color='black', linestyle=':', linewidth=1, alpha=0.5)

# Add title and labels
ax.set_title(f'US Housing Starts vs Canadian Lumber Exports ({df["Year"].min()}=100)', 
             fontsize=24, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=20)
ax.set_ylabel(f'Index ({df["Year"].min()} = 100)', fontsize=20)

# Add legend
ax.legend(loc='best', fontsize=17, frameon=True, fancybox=False, edgecolor='black')

# Format the axes
ax.grid(True, alpha=0.3, linestyle='--', color='gray')

plt.tight_layout()

# Print summary statistics
print("\n=== US Housing Starts vs Canadian Lumber Exports ===")
print(f"Time Period: {df['Year'].min()} to {df['Year'].max()}")
print(f"Base Year: {df['Year'].min()} (Index = 100)")
print(f"\nBase Year Values:")
print(f"  US Housing Starts: {base_housing:,.0f} thousand units (annual average)")
print(f"  Canadian Lumber Exports: {base_exports:,.0f} thousand cubic metres")

print("\n=== Latest Values ===")
latest = df.iloc[-1]
print(f"  Year: {int(latest['Year'])}")
print(f"  Housing Starts Index: {latest['Housing_Index']:.1f}")
print(f"  Lumber Exports Index: {latest['Exports_Index']:.1f}")

print("\n=== Key Statistics ===")
print(f"Housing Starts - Min Index: {df['Housing_Index'].min():.1f} ({int(df.loc[df['Housing_Index'].idxmin(), 'Year'])})")
print(f"Housing Starts - Max Index: {df['Housing_Index'].max():.1f} ({int(df.loc[df['Housing_Index'].idxmax(), 'Year'])})")
print(f"Lumber Exports - Min Index: {df['Exports_Index'].min():.1f} ({int(df.loc[df['Exports_Index'].idxmin(), 'Year'])})")
print(f"Lumber Exports - Max Index: {df['Exports_Index'].max():.1f} ({int(df.loc[df['Exports_Index'].idxmax(), 'Year'])})")

# Save the first plot to images folder
plt.savefig('../images/housing_exports_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# Calculate correlation
correlation = df['Housing_Index'].corr(df['Exports_Index'])
print(f"\nCorrelation between Housing Starts and Lumber Exports: {correlation:.3f}")

# Run linear regression
# Using actual values (not indices) for more meaningful coefficients
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Housing_Starts'], df['Total_Exports'])

print("\n=== Linear Regression Analysis ===")
print(f"Dependent Variable: Canadian Lumber Exports (thousand cubic metres)")
print(f"Independent Variable: US Housing Starts (thousand units)")
print(f"\nRegression Equation: Exports = {intercept:.2f} + {slope:.2f} × Housing_Starts")
print(f"\nR-squared: {r_value**2:.4f}")
print(f"Correlation coefficient (r): {r_value:.4f}")
print(f"P-value: {p_value:.6f}")
print(f"Standard Error: {std_err:.4f}")

# Interpretation
print(f"\nInterpretation:")
print(f"- For every 1,000 unit increase in US housing starts, Canadian lumber exports")
print(f"  increase by {slope:.2f} thousand cubic metres (or {slope*1000:.0f} cubic metres)")
print(f"- The model explains {(r_value**2)*100:.1f}% of the variation in lumber exports")
if p_value < 0.001:
    print(f"- The relationship is statistically significant at the 0.1% level")
elif p_value < 0.01:
    print(f"- The relationship is statistically significant at the 1% level")
elif p_value < 0.05:
    print(f"- The relationship is statistically significant at the 5% level")

# Calculate predicted values and residuals
df['Predicted_Exports'] = intercept + slope * df['Housing_Starts']
df['Residuals'] = df['Total_Exports'] - df['Predicted_Exports']

print(f"\nResidual Statistics:")
print(f"Mean Residual: {df['Residuals'].mean():.2f} (should be close to 0)")
print(f"Std Dev of Residuals: {df['Residuals'].std():.2f}")
print(f"Max Positive Residual: {df['Residuals'].max():.2f} thousand cubic metres ({int(df.loc[df['Residuals'].idxmax(), 'Year'])})")
print(f"Max Negative Residual: {df['Residuals'].min():.2f} thousand cubic metres ({int(df.loc[df['Residuals'].idxmin(), 'Year'])})")

# Create scatter plot with regression line
fig2, ax1 = plt.subplots(figsize=(12, 8))

ax1.scatter(df['Housing_Starts'], df['Total_Exports'], color='black', s=50, alpha=0.6, edgecolors='black', linewidth=1)
ax1.plot(df['Housing_Starts'], df['Predicted_Exports'], color='gray', linewidth=2, linestyle='--', 
         label=f'y = {intercept:.0f} + {slope:.2f}x\nR² = {r_value**2:.4f}')
ax1.set_xlabel('US Housing Starts (thousand units)', fontsize=20)
ax1.set_ylabel('Canadian Lumber Exports (thousand cubic metres)', fontsize=20)
ax1.set_title('Linear Regression: Housing Starts vs Lumber Exports', fontsize=24, fontweight='bold')
ax1.legend(loc='best', fontsize=17, frameon=True, fancybox=False, edgecolor='black')
ax1.grid(True, alpha=0.3, linestyle='--', color='gray')

plt.tight_layout()
plt.savefig('../images/housing_exports_scatter.png', dpi=300, bbox_inches='tight')
plt.close()

# Create residual plot
fig3, ax2 = plt.subplots(figsize=(12, 8))

ax2.scatter(df['Year'], df['Residuals'], color='black', s=50, alpha=0.6, edgecolors='black', linewidth=1)
ax2.axhline(y=0, color='gray', linestyle='--', linewidth=2)
ax2.set_xlabel('Year', fontsize=20)
ax2.set_ylabel('Residuals (thousand cubic metres)', fontsize=20)
ax2.set_title('Residual Plot Over Time', fontsize=24, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--', color='gray')

plt.tight_layout()
plt.savefig('../images/housing_exports_residuals.png', dpi=300, bbox_inches='tight')
plt.close()
