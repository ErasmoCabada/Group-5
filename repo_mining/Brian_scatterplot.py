import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'data/rootbeer_author_touches.csv'
df = pd.read_csv(file_path)

# Convert Dates and calculate Project Week
df['Date'] = pd.to_datetime(df['Date'])

# Find the very first touch in the whole dataset
start_date = df['Date'].min()

# Calculate weeks from start
# Divide the total seconds by (seconds in a minute * minutes in hour * hours in day * 7 days)
df['Weeks'] = (df['Date'] - start_date).dt.total_seconds() / (60 * 60 * 24 * 7)

# Create the plot
plt.figure(figsize=(14, 10))

# Get unique authors for coloring
authors = df['Author'].unique()
# Use a turbo to make colors stand out
colors = plt.cm.get_cmap('turbo', len(authors))

# Plotting: Files on X, Weeks on Y
for i, author in enumerate(authors):
    author_data = df[df['Author'] == author]
    plt.scatter(author_data['Filename'], author_data['Weeks'], 
                label=author, s=60, color=colors(i), edgecolors='black', linewidth=0.5, alpha=0.8)

# Formatting to match example
plt.title('Project Evolution: Weeks vs File Touches', fontsize=16)
plt.xlabel('File Name', fontsize=12)
plt.ylabel('Weeks (Since Project Start)', fontsize=12)

# Rotate X-axis labels because filenames are long
plt.xticks(rotation=90, fontsize=8)


plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title="Authors", fontsize='small')

plt.tight_layout()

# 6. Save and show
plt.savefig('data/rootbeer_scatterplot.png')
plt.show()

print("Refined scatter plot generated successfully!")