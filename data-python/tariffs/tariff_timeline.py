import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the tariff data
df = pd.read_csv('tariffs/tariff-weights.csv', encoding='utf-8')

# Convert dates to datetime
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])

# Create a daily time series from 2017-04-28 to today
date_range = pd.date_range(start='2017-04-28', end='2025-11-26', freq='D')
tariff_series = []

# For each date, find which tariff period it falls into
for date in date_range:
    for idx, row in df.iterrows():
        if pd.isna(row['end_date']):
            # If end_date is NaN, it's effective from start_date onwards
            if date >= row['start_date']:
                tariff_series.append(row['weighted_tariff'])
                break
        else:
            # Check if date falls within this period
            if row['start_date'] <= date <= row['end_date']:
                tariff_series.append(row['weighted_tariff'])
                break

# Create dataframe for plotting
plot_df = pd.DataFrame({'Date': date_range, 'Weighted_Tariff': tariff_series})

# Create the plot
fig, ax = plt.subplots(figsize=(16, 8))

# Plot the tariff rate
ax.plot(plot_df['Date'], plot_df['Weighted_Tariff'] * 100, linewidth=2, color='black')

# Add vertical lines and shaded areas for key events
financial_crisis_start = pd.to_datetime('2007-01-01')
financial_crisis_end = pd.to_datetime('2009-12-31')
trump_elected = pd.to_datetime('2016-11-01')
trump_reelected = pd.to_datetime('2024-11-01')

# Check if events fall within our time range and add them
if financial_crisis_start >= plot_df['Date'].min() and financial_crisis_end <= plot_df['Date'].max():
    ax.axvspan(financial_crisis_start, financial_crisis_end, color='#666666', alpha=0.3, label='Financial Crisis (2007-2009)')

if trump_elected >= plot_df['Date'].min() and trump_elected <= plot_df['Date'].max():
    ax.axvline(x=trump_elected, color='#999999', linestyle='-.', alpha=0.8, linewidth=2, label='Trump Elected (Nov 2016)')

if trump_reelected >= plot_df['Date'].min() and trump_reelected <= plot_df['Date'].max():
    ax.axvline(x=trump_reelected, color='#CCCCCC', linestyle='-.', alpha=0.8, linewidth=2, label='Trump Reelected (Nov 2024)')

# Add legend
ax.legend(loc='upper left', fontsize=17, framealpha=0.9)

# Add title and labels
ax.set_title('US Weighted Tariff Rate on Canadian Softwood Lumber (2017-2025)', 
             fontsize=24, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=20)
ax.set_ylabel('Weighted Tariff Rate (%)', fontsize=20)

# Format the axes
ax.grid(True, alpha=0.3, linestyle='--', color='gray')

# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Print summary statistics
print("\n=== US Softwood Lumber Tariff Summary ===")
print(f"Time Period: {plot_df['Date'].min().strftime('%B %d, %Y')} to {plot_df['Date'].max().strftime('%B %d, %Y')}")
print(f"\nWeighted Tariff Rates:")
for idx, row in df.iterrows():
    end_str = row['end_date'].strftime('%Y-%m-%d') if pd.notna(row['end_date']) else 'Present'
    print(f"  {row['start_date'].strftime('%Y-%m-%d')} to {end_str}: {row['weighted_tariff']*100:.1f}% - {row['event']}")

print(f"\nCurrent Tariff Rate: {df.iloc[-1]['weighted_tariff']*100:.1f}%")
print(f"Average Tariff Rate (2017-2025): {plot_df['Weighted_Tariff'].mean()*100:.1f}%")
print(f"Minimum Tariff Rate: {plot_df['Weighted_Tariff'].min()*100:.1f}%")
print(f"Maximum Tariff Rate: {plot_df['Weighted_Tariff'].max()*100:.1f}%")

# Save the plot to images folder
plt.savefig('../images/tariff_timeline.png', dpi=300, bbox_inches='tight')
plt.close()
