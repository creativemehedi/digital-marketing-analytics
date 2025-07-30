
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the simulated data
df = pd.read_csv("/home/ubuntu/digital_marketing_project/marketing_campaign_data.csv")

# --- Data Cleaning and Preprocessing ---
# Convert 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

# Handle potential missing values (though simulated data should be clean)
# For demonstration, let's fill any potential NaNs in numerical columns with 0
df[['Impressions', 'Clicks', 'Conversions', 'Cost', 'Revenue']] = \
    df[['Impressions', 'Clicks', 'Conversions', 'Cost', 'Revenue']].fillna(0)

# Ensure numerical types
df['Impressions'] = df['Impressions'].astype(int)
df['Clicks'] = df['Clicks'].astype(int)
df['Conversions'] = df['Conversions'].astype(int)
df['Cost'] = df['Cost'].astype(float)
df['Revenue'] = df['Revenue'].astype(float)

# --- KPI Calculation ---
# Click-Through Rate (CTR)
df['CTR'] = (df['Clicks'] / df['Impressions']).fillna(0) * 100

# Conversion Rate (CVR)
df['CVR'] = (df['Conversions'] / df['Clicks']).fillna(0) * 100

# Cost Per Click (CPC)
df['CPC'] = (df['Cost'] / df['Clicks']).fillna(0)

# Cost Per Acquisition (CPA)
df['CPA'] = (df['Cost'] / df['Conversions']).fillna(0)

# Return on Ad Spend (ROAS)
df['ROAS'] = (df['Revenue'] / df['Cost']).fillna(0)

# --- Campaign Performance Evaluation ---
print("\n--- Overall KPIs ---")
print(f"Total Impressions: {df['Impressions'].sum():,.0f}")
print(f"Total Clicks: {df['Clicks'].sum():,.0f}")
print(f"Total Conversions: {df['Conversions'].sum():,.0f}")
print(f"Total Cost: ${df['Cost'].sum():,.2f}")
print(f"Total Revenue: ${df['Revenue'].sum():,.2f}")
print(f"Overall CTR: {df['Clicks'].sum() / df['Impressions'].sum() * 100:.2f}%")
print(f"Overall CVR: {df['Conversions'].sum() / df['Clicks'].sum() * 100:.2f}%")
print(f"Overall ROAS: {df['Revenue'].sum() / df['Cost'].sum():.2f}")

# Aggregate by Campaign
campaign_summary = df.groupby('Campaign').agg(
    TotalImpressions=('Impressions', 'sum'),
    TotalClicks=('Clicks', 'sum'),
    TotalConversions=('Conversions', 'sum'),
    TotalCost=('Cost', 'sum'),
    TotalRevenue=('Revenue', 'sum')
).reset_index()

campaign_summary['CTR'] = (campaign_summary['TotalClicks'] / campaign_summary['TotalImpressions']).fillna(0) * 100
campaign_summary['CVR'] = (campaign_summary['TotalConversions'] / campaign_summary['TotalClicks']).fillna(0) * 100
campaign_summary['ROAS'] = (campaign_summary['TotalRevenue'] / campaign_summary['TotalCost']).fillna(0)

print("\n--- Campaign Performance Summary ---")
print(campaign_summary.sort_values(by='ROAS', ascending=False).to_markdown(index=False))

# Aggregate by Channel
channel_summary = df.groupby('Channel').agg(
    TotalImpressions=('Impressions', 'sum'),
    TotalClicks=('Clicks', 'sum'),
    TotalConversions=('Conversions', 'sum'),
    TotalCost=('Cost', 'sum'),
    TotalRevenue=('Revenue', 'sum')
).reset_index()

channel_summary['CTR'] = (channel_summary['TotalClicks'] / channel_summary['TotalImpressions']).fillna(0) * 100
channel_summary['CVR'] = (channel_summary['TotalConversions'] / channel_summary['TotalClicks']).fillna(0) * 100
channel_summary['ROAS'] = (channel_summary['TotalRevenue'] / channel_summary['TotalCost']).fillna(0)

print("\n--- Channel Performance Summary ---")
print(channel_summary.sort_values(by='ROAS', ascending=False).to_markdown(index=False))

# Aggregate by Platform
platform_summary = df.groupby('Platform').agg(
    TotalImpressions=('Impressions', 'sum'),
    TotalClicks=('Clicks', 'sum'),
    TotalConversions=('Conversions', 'sum'),
    TotalCost=('Cost', 'sum'),
    TotalRevenue=('Revenue', 'sum')
).reset_index()

platform_summary['CTR'] = (platform_summary['TotalClicks'] / platform_summary['TotalImpressions']).fillna(0) * 100
platform_summary['CVR'] = (platform_summary['TotalConversions'] / platform_summary['TotalClicks']).fillna(0) * 100
platform_summary['ROAS'] = (platform_summary['TotalRevenue'] / platform_summary['TotalCost']).fillna(0)

print("\n--- Platform Performance Summary ---")
print(platform_summary.sort_values(by='ROAS', ascending=False).to_markdown(index=False))

# --- Visualizations ---
# Sales Trend over time
df['Month'] = df['Date'].dt.to_period('M')
monthly_summary = df.groupby('Month').agg(TotalRevenue=('Revenue', 'sum'), TotalCost=('Cost', 'sum')).reset_index()
monthly_summary['Month'] = monthly_summary['Month'].astype(str)

plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_summary, x='Month', y='TotalRevenue', label='Total Revenue')
sns.lineplot(data=monthly_summary, x='Month', y='TotalCost', label='Total Cost')
plt.title('Monthly Revenue and Cost Trend')
plt.xlabel('Month')
plt.ylabel('Amount ($)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('/home/ubuntu/digital_marketing_project/monthly_trend.png')
plt.close()

# ROAS by Channel
plt.figure(figsize=(10, 6))
sns.barplot(data=channel_summary.sort_values(by='ROAS', ascending=False), x='Channel', y='ROAS', palette='viridis')
plt.title('ROAS by Channel')
plt.xlabel('Channel')
plt.ylabel('ROAS')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('/home/ubuntu/digital_marketing_project/roas_by_channel.png')
plt.close()

# Conversions by Platform
plt.figure(figsize=(12, 6))
sns.barplot(data=platform_summary.sort_values(by='TotalConversions', ascending=False), x='Platform', y='TotalConversions', palette='magma')
plt.title('Total Conversions by Platform')
plt.xlabel('Platform')
plt.ylabel('Total Conversions')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('/home/ubuntu/digital_marketing_project/conversions_by_platform.png')
plt.close()

print("Analysis complete and visualizations saved.")


