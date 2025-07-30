
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set a seed for reproducibility
np.random.seed(42)

# Define parameters for data generation
num_rows = 1000
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 30)

campaigns = [
    'Summer Sale 2024 - Search',
    'Summer Sale 2024 - Social',
    'New Product Launch - Search',
    'New Product Launch - Display',
    'Brand Awareness - Social',
    'Retargeting - Display'
]

channels = ['Search', 'Social Media', 'Display']

platforms = {
    'Search': ['Google Ads', 'Bing Ads'],
    'Social Media': ['Facebook', 'Instagram', 'TikTok', 'LinkedIn'],
    'Display': ['Google Display Network', 'Programmatic Display']
}

# Generate data
data = {
    'Date': [start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days)) for _ in range(num_rows)],
    'Campaign': np.random.choice(campaigns, num_rows),
    'Impressions': np.random.randint(1000, 100000, num_rows),
    'Clicks': np.random.randint(50, 5000, num_rows),
    'Conversions': np.random.randint(1, 500, num_rows),
    'Cost': np.round(np.random.uniform(10, 1000, num_rows), 2),
    'Revenue': np.round(np.random.uniform(50, 5000, num_rows), 2),
}

df = pd.DataFrame(data)

# Assign Channel and Platform based on Campaign
df['Channel'] = df['Campaign'].apply(lambda x: 'Search' if 'Search' in x else ('Social Media' if 'Social' in x else 'Display'))
df['Platform'] = df.apply(lambda row: np.random.choice(platforms[row['Channel']]), axis=1)

# Ensure Clicks <= Impressions and Conversions <= Clicks
df['Clicks'] = df.apply(lambda row: min(row['Clicks'], row['Impressions'] * 0.1), axis=1) # Clicks max 10% of impressions
df['Conversions'] = df.apply(lambda row: min(row['Conversions'], row['Clicks'] * 0.2), axis=1) # Conversions max 20% of clicks

# Calculate KPIs (will be done in analysis script, but good to have a sense)
# CTR = Clicks / Impressions
# CVR = Conversions / Clicks
# ROAS = Revenue / Cost

df.to_csv('/home/ubuntu/digital_marketing_project/marketing_campaign_data.csv', index=False)
print("Simulated marketing campaign data generated successfully.")


