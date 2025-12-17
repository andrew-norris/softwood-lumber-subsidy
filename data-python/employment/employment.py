import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('1410020201-eng.csv', skiprows=10)

# Extract the sawmills and wood preservation row
sawmills_row = df[df.iloc[:, 0] == 'Sawmills and wood preservation  [3211]']

# Get the years from the column names (starting from column 1)
years = df.columns[1:].astype(int)

# Get the employment values for sawmills
values = sawmills_row.iloc[0, 1:].values

# Remove quality indicators (A, B, etc.) from the values and convert to numeric
cleaned_values = []
for val in values:
    if isinstance(val, str):
        # Remove letters and convert to float
        cleaned_val = ''.join(c for c in val if c.isdigit() or c == ',' or c == '.')
        cleaned_val = cleaned_val.replace(',', '')
        cleaned_values.append(float(cleaned_val))
    else:
        cleaned_values.append(float(val))

# Create the line graph
plt.figure(figsize=(12, 6))
plt.plot(years, cleaned_values, linewidth=2, color='black')
plt.title('Employment in Sawmills and Wood Preservation (2001-2024)', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Employees (Persons)', fontsize=12)
plt.grid(True, alpha=0.3, linestyle='--', color='gray')
plt.xticks(years[::2], rotation=45)  # Show every other year to avoid crowding
plt.tight_layout()

# Save the plot to images folder
plt.savefig('../../images/employment.png', dpi=300, bbox_inches='tight')
plt.close()
