import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('prices/1810026601-eng.csv', skiprows=9)

# Extract the row for "Softwood lumber"
lumber_price_row = df[df.iloc[:, 0].str.contains(r'Softwood lumber \(except tongue and groove and other edge worked lumber\)  \[24112\]', na=False, regex=True)]

# Get the date columns from headers (skip first column which is the product name)
date_columns = [col for col in df.columns[1:] if col.strip() and not col.startswith('Unnamed')]

# Skip the units row and get price data
df = df.iloc[1:]  # Skip "Index, 202001=100" row

# Re-extract the row after skipping units row
lumber_price_row = df[df.iloc[:, 0].str.contains(r'Softwood lumber \(except tongue and groove and other edge worked lumber\)  \[24112\]', na=False, regex=True)]

# Parse dates and extract data
dates = []
prices = []

for col in date_columns:
    try:
        # Parse the date string (format: "Month Year")
        date_obj = pd.to_datetime(col, format='%B %Y')
        
        # Get the value for this column
        if len(lumber_price_row) > 0 and col in lumber_price_row.columns:
            val = lumber_price_row[col].values[0]
            
            # Clean the value (remove quality indicators and convert to float)
            if pd.notna(val) and str(val).strip() and str(val) not in ['..', 'F']:
                val_str = str(val).replace('E', '').strip()
                try:
                    value = float(val_str.replace(',', ''))
                    dates.append(date_obj)
                    prices.append(value)
                except:
                    pass
    except:
        continue

# Convert to numpy arrays
dates = np.array(dates)
prices = np.array(prices)

# Filter to start from 2003 for consistency with lumber output graph
start_date = pd.to_datetime('2003-01-01')
mask = dates >= start_date
dates_filtered = dates[mask]
prices_filtered = prices[mask]

# Create the plot
fig, ax = plt.subplots(figsize=(16, 8))

# Plot the data
ax.plot(dates_filtered, prices_filtered, linewidth=1.5, color='black', alpha=0.8)

# Add title and labels
ax.set_title('Softwood Lumber Price Index in Canada (2003-2025)', 
             fontsize=24, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=20)
ax.set_ylabel('Price Index (January 2020 = 100)', fontsize=20)

# Format the axes
ax.grid(True, alpha=0.3, linestyle='--', color='gray')

# Format the plot
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Print summary statistics
print("\n=== Softwood Lumber Price Index Summary Statistics ===")
print(f"Time Period: {dates_filtered[0].strftime('%B %Y')} to {dates_filtered[-1].strftime('%B %Y')}")
print(f"Mean Price Index: {prices_filtered.mean():.1f}")
print(f"Maximum Price Index: {prices_filtered.max():.1f} ({dates_filtered[np.argmax(prices_filtered)].strftime('%B %Y')})")
print(f"Minimum Price Index: {prices_filtered.min():.1f} ({dates_filtered[np.argmin(prices_filtered)].strftime('%B %Y')})")
print(f"Latest: {prices_filtered[-1]:.1f} ({dates_filtered[-1].strftime('%B %Y')})")

# Calculate year-over-year changes for select years
print("\n=== Price Index by Year (January values) ===")
years_to_show = [2003, 2004, 2005, 2010, 2015, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
for year in years_to_show:
    # Get January value if available
    jan_mask = np.array([(d.year == year and d.month == 1) for d in dates_filtered])
    if jan_mask.any():
        jan_value = prices_filtered[jan_mask][0]
        print(f"January {year}: {jan_value:.1f}")

# Save the plot to images folder
plt.savefig('../images/lumber_price_graph.png', dpi=300, bbox_inches='tight')
plt.close()
