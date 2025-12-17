import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file with the correct structure
# Line 12 (index 11) has the column headers with years
df = pd.read_csv('3610043403-eng.csv', skiprows=11)

# The columns are: NAICS description, then years 1997-2025, then empty column
# Get the year columns (excluding first column and last empty column)
year_columns = [col for col in df.columns[1:] if col.strip() and col.strip().replace(',', '').isdigit()]
years = [int(col) for col in year_columns]

# Skip the first row which just says "Dollars"
df = df.iloc[1:].reset_index(drop=True)

# Extract the rows for total GDP and forestry using raw strings to avoid escape issues
all_industries_row = df[df.iloc[:, 0].str.contains(r'All industries  \[T001\]', na=False, regex=True)]
forestry_row = df[df.iloc[:, 0].str.contains(r'Agriculture, forestry, fishing and hunting  \[11\]', na=False, regex=True)]

# Check if rows were found
if len(all_industries_row) == 0:
    print("Available industries in the data:")
    print(df.iloc[:, 0].head(20))
    raise ValueError("Could not find 'All industries' row")
    
if len(forestry_row) == 0:
    print("Available industries in the data:")
    print(df.iloc[:, 0].head(20))
    raise ValueError("Could not find 'Agriculture, forestry' row")

# Get the GDP values for the year columns
total_gdp_values = []
forestry_gdp_values = []

for year_col in year_columns:
    total_val = all_industries_row[year_col].values[0]
    forestry_val = forestry_row[year_col].values[0]
    
    # Remove commas and convert to float
    total_val = float(str(total_val).replace(',', '')) if total_val else np.nan
    forestry_val = float(str(forestry_val).replace(',', '')) if forestry_val else np.nan
    
    total_gdp_values.append(total_val)
    forestry_gdp_values.append(forestry_val)

total_gdp = np.array(total_gdp_values)
forestry_gdp = np.array(forestry_gdp_values)

# Calculate forestry as percentage of total GDP
forestry_percentage = (forestry_gdp / total_gdp) * 100

# Filter out any years with NaN or inf values
valid_indices = ~(np.isnan(forestry_percentage) | np.isinf(forestry_percentage))
years_filtered = np.array(years)[valid_indices]
forestry_percentage_filtered = forestry_percentage[valid_indices]

# Create the line graph
plt.figure(figsize=(14, 7))
plt.plot(years_filtered, forestry_percentage_filtered, linewidth=2, color='black')
plt.title('Agriculture, Forestry, Fishing and Hunting as % of Total GDP (1997-2024)', 
          fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Percentage of Total GDP (%)', fontsize=12)
plt.grid(True, alpha=0.3, linestyle='--', color='gray')
plt.xticks(years_filtered[::2], rotation=45)  # Show every other year to avoid crowding
plt.tight_layout()

# Add a horizontal line at the mean
mean_percentage = forestry_percentage_filtered.mean()
plt.axhline(y=mean_percentage, color='gray', linestyle='--', alpha=0.5, 
            label=f'Mean: {mean_percentage:.2f}%')
plt.legend()

# Save the plot to images folder
plt.savefig('../../images/forestry_gdp.png', dpi=300, bbox_inches='tight')
plt.close()

# Print summary statistics
print("\n=== Summary Statistics ===")
print(f"Mean: {mean_percentage:.2f}%")
print(f"Min: {forestry_percentage_filtered.min():.2f}% (Year {years_filtered[forestry_percentage_filtered.argmin()]})")
print(f"Max: {forestry_percentage_filtered.max():.2f}% (Year {years_filtered[forestry_percentage_filtered.argmax()]})")
print(f"Latest (2024): {forestry_percentage_filtered[-1]:.2f}%")
