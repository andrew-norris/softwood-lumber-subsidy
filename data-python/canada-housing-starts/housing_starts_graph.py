import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Read the dataset - header is at row 7, data starts at row 9
df = pd.read_csv('canada-housing-starts/3410015801-eng.csv', skiprows=7)

# Get the date columns from headers (skip first column which is Geography)
date_columns = [col for col in df.columns[1:] if col.strip() and not col.startswith('Unnamed')]

# Skip the units row and get Canada data
df = df.iloc[1:]  # Skip "Units" row

# Extract data for Canada (first row after units row)
canada_row = df.iloc[0]  # Canada is the first row

# Parse dates and extract data
def parse_housing_data(date_columns, data_row):
    """Parse date columns and extract corresponding values for housing starts"""
    dates = []
    values = []
    
    for col in date_columns:
        try:
            # Parse the date string (format: "Month Year")
            date_obj = pd.to_datetime(col, format='%B %Y')
            
            # Get the value for this column
            if col in data_row.index:
                val = data_row[col]
                
                # Clean the value and convert to float
                if pd.notna(val) and str(val).strip() and str(val) != '..':
                    val_str = str(val).replace('r', '').replace('A', '').replace('B', '').replace('C', '') \
                                     .replace('D', '').replace('E', '').replace('F', '').strip()
                    try:
                        # Convert to annual rate (data is already in thousands and annualized)
                        value = float(val_str.replace(',', ''))
                        dates.append(date_obj)
                        values.append(value)
                    except:
                        pass
        except:
            continue
    
    return dates, values

# Parse the data
dates, values = parse_housing_data(date_columns, canada_row)

# Create a dictionary for easier handling
housing_data = dict(zip(dates, values))

# Sort by date
sorted_dates = sorted(housing_data.keys())
sorted_values = [housing_data[date] for date in sorted_dates]

# Create the plot
fig, ax = plt.subplots(figsize=(16, 8))

# Plot the data
ax.plot(sorted_dates, sorted_values, linewidth=1.5, color='black', alpha=0.8)

# Add title and labels
ax.set_title('Canadian Housing Starts (2005-2025)', fontsize=24, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=20)
ax.set_ylabel('Housing Starts (thousands)', fontsize=20)

# Format the plot
ax.grid(True, alpha=0.3, linestyle='--', color='gray')

# Format the x-axis
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Print summary statistics
print("\n=== Canadian Housing Starts Summary Statistics ===")
print(f"Time Period: {sorted_dates[0].strftime('%B %Y')} to {sorted_dates[-1].strftime('%B %Y')}")
print(f"Mean Housing Starts: {np.mean(sorted_values):,.0f} thousand units")
print(f"Maximum Housing Starts: {np.max(sorted_values):,.0f} thousand units ({sorted_dates[np.argmax(sorted_values)].strftime('%B %Y')})")
print(f"Minimum Housing Starts: {np.min(sorted_values):,.0f} thousand units ({sorted_dates[np.argmin(sorted_values)].strftime('%B %Y')})")
print(f"Latest (most recent): {sorted_values[-1]:,.0f} thousand units ({sorted_dates[-1].strftime('%B %Y')})")

# Calculate year-over-year changes
yearly_data = {}
for date, value in zip(sorted_dates, sorted_values):
    year = date.year
    if year not in yearly_data:
        yearly_data[year] = []
    yearly_data[year].append(value)

# Calculate annual averages
annual_averages = {year: np.mean(values) for year, values in yearly_data.items()}
print("\n=== Annual Average Housing Starts ===")
for year in sorted(annual_averages.keys()):
    print(f"{year}: {annual_averages[year]:,.0f} thousand units")

# Identify key periods
print("\n=== Key Periods ===")

# Financial crisis period (2008-2009)
crisis_data = [val for date, val in zip(sorted_dates, sorted_values) if 2008 <= date.year <= 2009]
if crisis_data:
    print(f"Financial Crisis Average (2008-2009): {np.mean(crisis_data):,.0f} thousand units")

# Recovery period (2010-2015)
recovery_data = [val for date, val in zip(sorted_dates, sorted_values) if 2010 <= date.year <= 2015]
if recovery_data:
    print(f"Recovery Period Average (2010-2015): {np.mean(recovery_data):,.0f} thousand units")

# Recent period (2020-2025)
recent_data = [val for date, val in zip(sorted_dates, sorted_values) if date.year >= 2020]
if recent_data:
    print(f"Recent Period Average (2020-2025): {np.mean(recent_data):,.0f} thousand units")

# Save the plot to images folder
plt.savefig('../images/canada_housing_starts.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\nGraph saved to: ../../images/canada_housing_starts.png")