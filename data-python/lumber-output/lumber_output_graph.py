import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Read the older dataset (2003-2018) - header is at row 10
df_old = pd.read_csv('lumber-output/1610004501-eng.csv', skiprows=9)

# Read the newer dataset (2014-2025) - header is at row 10
df_new = pd.read_csv('lumber-output/1610001701-eng.csv', skiprows=9)

# Get the date columns from headers
old_date_columns = [col for col in df_old.columns[1:] if col.strip() and not col.startswith('Unnamed')]
new_date_columns = [col for col in df_new.columns[1:] if col.strip() and not col.startswith('Unnamed')]

# Skip the units row and get production data
df_old = df_old.iloc[1:]  # Skip "Cubic metres" row
df_new = df_new.iloc[1:]  # Skip "Cubic metres" row

# Extract production data for total softwood and hardwood
old_production_row = df_old[df_old.iloc[:, 0].str.contains('Total softwood and hardwood, production', na=False, regex=False)]
new_production_row = df_new[df_new.iloc[:, 0].str.contains('Total softwood and hardwood, production', na=False, regex=False)]

# Parse dates and extract data
def parse_data(date_columns, data_row):
    """Parse date columns and extract corresponding values"""
    dates = []
    values = []
    
    for col in date_columns:
        try:
            # Parse the date string (format: "Month Year")
            date_obj = pd.to_datetime(col, format='%B %Y')
            
            # Get the value for this column
            if len(data_row) > 0 and col in data_row.columns:
                val = data_row[col].values[0]
                
                # Clean the value (remove quality indicators and convert to float)
                if pd.notna(val) and str(val).strip() and str(val) != '..':
                    val_str = str(val).replace('r', '').replace('A', '').replace('B', '').replace('C', '') \
                                     .replace('D', '').replace('E', '').replace('F', '').strip()
                    try:
                        value = float(val_str.replace(',', ''))
                        dates.append(date_obj)
                        values.append(value)
                    except:
                        pass
        except:
            continue
    
    return dates, values

# Parse old data
old_dates, old_values = parse_data(old_date_columns, old_production_row)

# Parse new data
new_dates, new_values = parse_data(new_date_columns, new_production_row)

# Combine the datasets, prioritizing newer data
# Create a dictionary to store date -> value mapping
combined_data = {}

# Add old data first
for date, value in zip(old_dates, old_values):
    if pd.notna(value):
        combined_data[date] = value

# Overwrite with new data (this prioritizes newer file)
for date, value in zip(new_dates, new_values):
    if pd.notna(value):
        combined_data[date] = value

# Filter data from 2003 onwards
start_date = pd.to_datetime('2003-01-01')
filtered_data = {date: value for date, value in combined_data.items() if date >= start_date}

# Sort by date
sorted_dates = sorted(filtered_data.keys())
sorted_values = [filtered_data[date] for date in sorted_dates]

# Convert to thousands of cubic metres (values are already in thousands)
# Create the plot
fig, ax = plt.subplots(figsize=(16, 8))

# Plot the data
ax.plot(sorted_dates, sorted_values, linewidth=1.5, color='black', alpha=0.8)

# Add vertical lines for key events
# Add vertical lines and shaded areas for key events
ax.axvline(x=pd.to_datetime('2006-10-01'), color='#333333', linestyle='--', alpha=0.8, linewidth=2, label='SLA Start (Oct 2006)')  # Dark gray, dashed
ax.axvspan(pd.to_datetime('2007-01-01'), pd.to_datetime('2009-12-31'), color='#666666', alpha=0.3, label='Financial Crisis (2007-2009)')  # Shaded area
ax.axvline(x=pd.to_datetime('2015-10-01'), color='#666666', linestyle=':', alpha=0.8, linewidth=2, label='SLA End (Oct 2015)')  # Medium gray, dotted
ax.axvline(x=pd.to_datetime('2016-11-01'), color='#999999', linestyle='-.', alpha=0.8, linewidth=2, label='Trump Elected (Nov 2016)')  # Light gray, dash-dot

# Add legend
ax.legend(loc='upper right', fontsize=17, framealpha=0.9)

# Add title and labels
ax.set_title('Total Lumber Production in Canada (2003-2025)', fontsize=24, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=20)
ax.set_ylabel('Production (thousands of cubic metres)', fontsize=20)

# Format the x-axis
ax.grid(True, alpha=0.3, linestyle='--', color='gray')

# Format the plot
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Print summary statistics
print("\n=== Lumber Production Summary Statistics ===")
print(f"Time Period: {sorted_dates[0].strftime('%B %Y')} to {sorted_dates[-1].strftime('%B %Y')}")
print(f"Mean Production: {np.mean(sorted_values):,.0f} thousand cubic metres")
print(f"Maximum Production: {np.max(sorted_values):,.0f} thousand cubic metres ({sorted_dates[np.argmax(sorted_values)].strftime('%B %Y')})")
print(f"Minimum Production: {np.min(sorted_values):,.0f} thousand cubic metres ({sorted_dates[np.argmin(sorted_values)].strftime('%B %Y')})")
print(f"Latest (most recent): {sorted_values[-1]:,.0f} thousand cubic metres ({sorted_dates[-1].strftime('%B %Y')})")

# Calculate year-over-year changes
yearly_data = {}
for date, value in zip(sorted_dates, sorted_values):
    year = date.year
    if year not in yearly_data:
        yearly_data[year] = []
    yearly_data[year].append(value)

# Calculate annual averages
annual_averages = {year: np.mean(values) for year, values in yearly_data.items()}
print("\n=== Annual Average Production ===")
for year in sorted(annual_averages.keys()):
    print(f"{year}: {annual_averages[year]:,.0f} thousand cubic metres")

# Save the plot to images folder
plt.savefig('../images/lumber_output_graph.png', dpi=300, bbox_inches='tight')
plt.close()
