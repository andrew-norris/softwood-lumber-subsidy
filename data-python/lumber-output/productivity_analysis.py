import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Read employment data
df_employment = pd.read_csv('../employment/1410020201-eng.csv', skiprows=10)

# Extract sawmill employment row
sawmill_employment_row = df_employment[df_employment.iloc[:, 0].str.contains(r'Sawmills and wood preservation  \[3211\]', na=False, regex=True)]

# Get years from employment data
employment_years = [int(col) for col in df_employment.columns[1:] if col.strip() and col.strip().isdigit()]

# Get employment values
employment_values = []
for year_col in [str(year) for year in employment_years]:
    val = sawmill_employment_row[year_col].values[0] if len(sawmill_employment_row) > 0 else np.nan
    
    # Clean the value (remove quality indicators and convert to float)
    if pd.notna(val):
        val_str = str(val).replace('A', '').replace('B', '').replace('C', '').replace(',', '').strip()
        try:
            employment_values.append(float(val_str))
        except:
            employment_values.append(np.nan)
    else:
        employment_values.append(np.nan)

# Read lumber output data (from the combined dataset)
# We'll need to aggregate monthly data to annual
df_old = pd.read_csv('1610004501-eng.csv', skiprows=9)
df_new = pd.read_csv('1610001701-eng.csv', skiprows=9)

# Get date columns and production data
old_date_columns = [col for col in df_old.columns[1:] if col.strip() and not col.startswith('Unnamed')]
new_date_columns = [col for col in df_new.columns[1:] if col.strip() and not col.startswith('Unnamed')]

# Skip units row
df_old = df_old.iloc[1:]
df_new = df_new.iloc[1:]

# Extract production rows
old_production_row = df_old[df_old.iloc[:, 0].str.contains('Total softwood and hardwood, production', na=False, regex=False)]
new_production_row = df_new[df_new.iloc[:, 0].str.contains('Total softwood and hardwood, production', na=False, regex=False)]

# Parse production data
def parse_production(date_columns, data_row):
    dates = []
    values = []
    for col in date_columns:
        try:
            date_obj = pd.to_datetime(col, format='%B %Y')
            if len(data_row) > 0 and col in data_row.columns:
                val = data_row[col].values[0]
                if pd.notna(val) and str(val).strip() and str(val) != '..':
                    val_str = str(val).replace('r', '').replace('A', '').replace('B', '').replace('C', '').strip()
                    try:
                        value = float(val_str.replace(',', ''))
                        dates.append(date_obj)
                        values.append(value)
                    except:
                        pass
        except:
            continue
    return dates, values

old_dates, old_values = parse_production(old_date_columns, old_production_row)
new_dates, new_values = parse_production(new_date_columns, new_production_row)

# Combine production data, prioritizing newer data
combined_data = {}
for date, value in zip(old_dates, old_values):
    if pd.notna(value):
        combined_data[date] = value
for date, value in zip(new_dates, new_values):
    if pd.notna(value):
        combined_data[date] = value

# Aggregate monthly production to annual (sum for the year)
annual_production = {}
for date, value in combined_data.items():
    year = date.year
    if year not in annual_production:
        annual_production[year] = []
    annual_production[year].append(value)

# Calculate annual totals (thousands of cubic metres)
production_years = []
production_totals = []
for year in sorted(annual_production.keys()):
    production_years.append(year)
    production_totals.append(sum(annual_production[year]))

# Align employment and production data
# Find common years (starting from 2004)
common_years = sorted(set(employment_years) & set(production_years))
common_years = [year for year in common_years if year >= 2004]

# Get aligned data
aligned_employment = []
aligned_production = []
aligned_years = []
for year in common_years:
    emp_idx = employment_years.index(year)
    prod_idx = production_years.index(year)
    
    emp_val = employment_values[emp_idx]
    prod_val = production_totals[prod_idx]
    
    if not np.isnan(emp_val) and not np.isnan(prod_val) and emp_val > 0:
        aligned_employment.append(emp_val)
        aligned_production.append(prod_val)
        aligned_years.append(year)

if len(aligned_years) == 0:
    print("\nERROR: No overlapping years with valid data!")
    print(f"Check employment data: {list(zip(employment_years, employment_values))}")
    exit(1)

# Use aligned_years instead of common_years for the rest
common_years = aligned_years

# Calculate productivity (output per worker in thousands of cubic metres per person)
productivity = np.array(aligned_production) / np.array(aligned_employment)

# Create productivity index (earliest year = 100)
productivity_index = (productivity / productivity[0]) * 100

# Create the plot
fig, ax = plt.subplots(figsize=(14, 7))

# Plot the data
ax.plot(common_years, productivity_index, linewidth=2, color='black')

# Add title and labels
ax.set_title('Sawmill Productivity Index: Output per Worker (2004 = 100)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Productivity Index', fontsize=12)

# Add a horizontal line at 100
ax.axhline(y=100, color='gray', linestyle='--', alpha=0.5, linewidth=1)

# Format the axes
ax.grid(True, alpha=0.3, linestyle='--', color='gray')
ax.set_xticks(common_years[::2])  # Show every other year
ax.set_xticklabels(common_years[::2], rotation=45)

plt.tight_layout()

# Print summary statistics
print("\n=== Sawmill Productivity Analysis ===")
print(f"Time Period: {common_years[0]} to {common_years[-1]}")
print(f"\nBase Year ({common_years[0]}):")
print(f"  Employment: {aligned_employment[0]:,.0f} persons")
print(f"  Production: {aligned_production[0]:,.0f} thousand cubic metres")
print(f"  Productivity: {productivity[0]:.2f} thousand cubic metres per worker")
print(f"  Index: 100.0")

print(f"\nLatest Year ({common_years[-1]}):")
print(f"  Employment: {aligned_employment[-1]:,.0f} persons")
print(f"  Production: {aligned_production[-1]:,.0f} thousand cubic metres")
print(f"  Productivity: {productivity[-1]:.2f} thousand cubic metres per worker")
print(f"  Index: {productivity_index[-1]:.1f}")

print(f"\nProductivity Change: {((productivity_index[-1] / 100) - 1) * 100:+.1f}%")

print("\n=== Productivity Index by Year ===")
for year, emp, prod, prod_val, idx in zip(common_years, aligned_employment, aligned_production, productivity, productivity_index):
    print(f"{year}: {idx:6.1f} (Employment: {emp:>6,.0f}, Production: {prod:>7,.0f}, Output/Worker: {prod_val:.2f})")

# Save the plot to images folder
plt.savefig('../../images/productivity_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
