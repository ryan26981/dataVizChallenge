import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Load 2010 baseball season data
df2010 = pd.read_csv("baseball10.csv")

# Load 2021 baseball season data for comparison
df2021 = pd.read_csv("baseball21.csv")

print("2010 data shape:", df2010.shape)
print("2021 data shape:", df2021.shape)
print("\n2010 data columns:", df2010.columns.tolist())
print("\nFirst few rows of 2010 data:")
print(df2010.head())

# Stage 2: Curation of Content
# Aggregate data to get average runs per stadium

# Process 2010 data
avgDF_2010 = (df2010
    .assign(totalRuns = lambda df: df.homeScore + df.visScore)
    .assign(totalHR = lambda df: df.homeHR + df.visHR)
    .drop(columns = ['date', 'visiting'])
    .groupby(['home'], as_index=False)
    .mean()
)

# Process 2021 data
avgDF_2021 = (df2021
    .assign(totalRuns = lambda df: df.homeScore + df.visScore)
    .assign(totalHR = lambda df: df.homeHR + df.visHR)
    .drop(columns = ['date', 'visiting'])
    .groupby(['home'], as_index=False)
    .mean()
)

print("2010 Stadium Averages (Top 5):")
print(avgDF_2010.head())
print("\n2021 Stadium Averages (Top 5):")
print(avgDF_2021.head())

# Stage 3: Structuring of Visual Mappings
# Explore different geometries and aesthetics

# Sort data for better visualization
avgDF_2010_sorted = avgDF_2010.sort_values('totalRuns', ascending=True)

# Create figure with subplots to compare approaches
fig, axes = plt.subplots(2, 2, figsize=(8, 9))

# Approach 1: Scatter plot (not ideal for categorical data)
axes[0,0].scatter(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns)
axes[0,0].set_title("Approach 1: Scatter Plot")
axes[0,0].set_xlabel("Stadium")
axes[0,0].set_ylabel("Average Runs")
axes[0,0].tick_params(axis='x', labelsize=9)

# Approach 2: Horizontal bar chart (better for categorical data)
axes[0,1].barh(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns)
axes[0,1].set_title("Approach 2: Horizontal Bar Chart")
axes[0,1].set_xlabel("Average Runs")
axes[0,1].set_ylabel("Stadium")
axes[0,1].tick_params(axis='y', labelsize=9)

# Approach 3: Vertical bar chart
axes[1,0].bar(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns)
axes[1,0].set_title("Approach 3: Vertical Bar Chart")
axes[1,0].set_xlabel("Stadium")
axes[1,0].set_ylabel("Average Runs")
axes[1,0].tick_params(axis='x', rotation=45, labelsize=9)

# Approach 4: Highlight Colorado
colorado_colors = ["darkorchid" if stadium == "COL" else "lightgrey" 
                   for stadium in avgDF_2010_sorted.home]
axes[1,1].barh(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns, color=colorado_colors)
axes[1,1].set_title("Approach 4: Highlight Colorado")
axes[1,1].set_xlabel("Average Runs")
axes[1,1].set_ylabel("Stadium")
axes[1,1].tick_params(axis='y', labelsize=9)

plt.tight_layout()
plt.show()

# Stage 4: Formatting for Your Audience
# Create a professional, publication-ready visualization

# Set style for professional appearance
plt.style.use("seaborn-v0_8-whitegrid")

# Create the main visualization
fig, ax = plt.subplots(figsize=(8, 6))

# Create color array for highlighting Colorado
colorado_colors = ["darkorchid" if stadium == "COL" else "lightgrey" 
                   for stadium in avgDF_2010_sorted.home]

# Create horizontal bar chart
bars = ax.barh(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns, color=colorado_colors)

# Add title and labels
ax.set_title("Colorado (COL) is the Most Run-Friendly Ballpark in 2010", 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel("Average Runs Per Game", fontsize=12)
ax.set_ylabel("Stadium (Home Team)", fontsize=12)

# Add legend
colorado_bar = plt.Rectangle((0,0),1,1, color="darkorchid", label="Colorado Rockies")
other_bar = plt.Rectangle((0,0),1,1, color="lightgrey", label="Other Stadiums")
ax.legend(handles=[colorado_bar, other_bar], loc='lower right', frameon=True)

# Add annotation for Colorado
colorado_index = avgDF_2010_sorted[avgDF_2010_sorted.home == "COL"].index[0]
colorado_runs = avgDF_2010_sorted[avgDF_2010_sorted.home == "COL"]["totalRuns"].iloc[0]
ax.annotate(f"COL: {colorado_runs:.2f} runs/game", 
            xy=(colorado_runs, colorado_index), 
            xytext=(colorado_runs + 0.5, colorado_index),
            arrowprops=dict(arrowstyle='->', color='darkorchid', lw=2),
            fontsize=10, fontweight='bold', color='darkorchid')

# Set x-axis to start from 0 for better comparison
ax.set_xlim(0, max(avgDF_2010_sorted.totalRuns) * 1.1)

# Smaller font for stadium (y-axis) tick labels
ax.tick_params(axis='y', labelsize=9)

# Add grid for easier reading
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Print summary statistics
print(f"\nSummary Statistics for 2010:")
print(f"Colorado (COL) average runs per game: {colorado_runs:.2f}")
print(f"League average runs per game: {avgDF_2010_sorted.totalRuns.mean():.2f}")
print(f"Colorado is {((colorado_runs / avgDF_2010_sorted.totalRuns.mean()) - 1) * 100:.1f}% above league average")
# Advanced Object-Oriented Techniques
# Create a comprehensive comparison visualization
#
# Visualization explanation:
# We build a side-by-side comparison of average runs per game by stadium for 2010
# and 2021. The two horizontal bar charts share the same y-axis (stadium names) so
# you can easily compare the same venue across seasons. Within each panel, bars
# are sorted by runs (low to high). The stadium with the highest average runs in
# each season is highlighted in dark orchid; all others are light grey. This makes
# it clear which ballpark was the highest-scoring environment in each year (e.g.
# Coors Field in Denver) and how that ranking or gap might have changed from 2010
# to 2021.

This visualization is correct but it did not give a conclusion, it just explained what the visualiztion was doing 
from a technical standpoint.

# Prepare data for comparison
comparison_data = pd.merge(
    avgDF_2010[['home', 'totalRuns']].rename(columns={'totalRuns': 'runs_2010'}),
    avgDF_2021[['home', 'totalRuns']].rename(columns={'totalRuns': 'runs_2021'}),
    on='home', how='inner'
)

## Create the visualization: 2010 vs 2021 side by side
fig, axs = plt.subplots(1, 2, figsize=(12, 8), sharey=True)

for index, (season, runs_col) in enumerate([(2010, "runs_2010"), (2021, "runs_2021")]):
    groupDF = comparison_data.sort_values(runs_col, ascending=True)
    runs = groupDF[runs_col]
    bestRuns = runs.max()
    colorArray = ["darkorchid" if r == bestRuns else "lightgrey" for r in runs]
    axs[index].barh(groupDF.home, runs, color=colorArray)
    axs[index].set_title(f"Season: {season}")
    axs[index].set_xlabel("Average Runs")
    axs[index].set_ylabel("Stadium")
    axs[index].tick_params(axis="y", labelsize=9)

fig.suptitle("Comparison of Runs per Stadium by Season")
plt.tight_layout()
plt.show()