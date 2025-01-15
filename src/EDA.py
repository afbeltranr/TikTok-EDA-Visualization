import os
from google.oauth2.service_account import Credentials

# Get the path from the environment variable
json_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import pandas as pd


scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
credentials = Credentials.from_service_account_file(json_path, scopes=scopes)

client = gspread.authorize(credentials)

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1f7jIcEzhLiO2EhVZro8oUdNgm2AGaC5po8QNiuQggG4/edit?usp=sharing"
spreadsheet = client.open_by_url(spreadsheet_url)

worksheet = spreadsheet.get_worksheet(0)

data = worksheet.get_all_records()
df = pd.DataFrame(data)

print(df.head())

import seaborn as sns
import matplotlib.pyplot as plt

# List of numerical columns
numerical_columns = [
    'video_duration_sec', 
    'video_view_count', 
    'video_like_count', 
    'video_share_count', 
    'video_download_count', 
    'video_comment_count'
]

# Convert columns to numeric, coercing errors to NaN
for col in numerical_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Create a figure and axes
fig, axes = plt.subplots(6, 2, figsize=(15, 30))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Plot each numerical column as a horizontal boxplot and histogram
for i, col in enumerate(numerical_columns):
    sns.boxplot(x=df[col], ax=axes[2*i], orient='h')
    axes[2*i].set_title(f'Boxplot of {col}')
    
    sns.histplot(df[col], ax=axes[2*i + 1], kde=True)
    axes[2*i + 1].set_title(f'Histogram of {col}')

# Adjust layout
plt.tight_layout()

# Save the plot as a PNG file
plt.savefig('img/variables_distribution.png')

# Show the plot
plt.show()

df_cleaned = df[df['claim_status'] != '']
# Create a new figure for the verification status plot
plt.figure()

sns.histplot(data=df_cleaned,
             x='claim_status',
             hue='verified_status',
             multiple='dodge',
             shrink=0.9)
plt.title('Claims by verification status histogram')

# Save the plot as a PNG file
plt.savefig('img/verification_status.png')

# Show the plot
plt.show()



plt.figure()

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Pie chart for total views by video claim status
axes[0].pie(df_cleaned.groupby('claim_status')['video_view_count'].sum(), labels=['claim', 'opinion'], autopct='%1.1f%%')
axes[0].set_title('Total views by video claim status')

# Pie chart for count of claim/opinion videos
axes[1].pie(df_cleaned['claim_status'].value_counts(), labels=['claim', 'opinion'], autopct='%1.1f%%')
axes[1].set_title('Count of claim/opinion videos')

plt.savefig('img/view_count_distribution.png')


plt.figure()

ban_status_counts = df_cleaned.groupby(['author_ban_status']).median(
    numeric_only=True).reset_index()

fig = plt.figure(figsize=(5,3))
sns.barplot(data=ban_status_counts,
            x='author_ban_status',
            y='video_view_count',
            order=['active', 'under review', 'banned'],
            palette={'active':'green', 'under review':'orange', 'banned':'red'},
            alpha=0.5)
plt.title('Median View Count by Ban Status')
plt.xlabel('Author Ban Status')
plt.ylabel('Median Video View Count')

plt.tight_layout()
plt.savefig('img/account_status.png')