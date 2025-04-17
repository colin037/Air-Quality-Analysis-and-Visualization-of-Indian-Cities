import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from statsmodels.stats.weightstats import ztest


# Loading the dataset from a CSV file
df = pd.read_csv(r"C:\LPU NOTES\SEM 4\CLASS\PYTHON\PROJECT\ABC.csv")

# Checking for missing values in each column
print(df.isnull().sum())

# Calculating the total number of missing values in the entire dataset
print(df.isnull().sum().sum())

print("\nAfter cleaning.\n")
# Filling missing values in numeric columns with their respective column means
df.fillna(df.mean(numeric_only=True), inplace=True)

# Verifying that missing values have been filled
print(df.isnull().sum())


# Bar plot: Number of Stations in Each State
# This plot shows the number of unique pollution monitoring stations in each state
stations_per_state = df.groupby('state')['station'].nunique()

plt.figure(figsize=(12, 6))
sns.barplot(x=stations_per_state.index, y=stations_per_state.values, palette='viridis')
plt.title("Number of Stations in Each State", fontsize=14, fontweight='bold')
plt.xlabel("State", fontsize=12)
plt.ylabel("Number of Stations", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# Box plot: Pollution Level Distribution in Top 10 States
# This box plot shows the distribution of pollution levels in the top 10 states with the highest average pollution levels
df['pollutant_avg'] = df['pollutant_avg'].fillna(df['pollutant_avg'].mean())

top_states = df.groupby('state')['pollutant_avg'].mean().nlargest(10)

top_states_data = df[df['state'].isin(top_states.index)]

plt.figure(figsize=(12, 8))
sns.boxplot(x='state', y='pollutant_avg', data=top_states_data, palette='Reds')
plt.title("Pollution Level Distribution in Top 10 States")
plt.xlabel("State")
plt.ylabel("Pollution Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Bar plot: Average Pollutant Levels by Pollutant Type
# This bar plot shows the average pollution level for each pollutant type
pollutant_avg = df.groupby('pollutant_id')['pollutant_avg'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=pollutant_avg.index, y=pollutant_avg.values, palette='viridis')
plt.title("Average Pollutant Levels by Pollutant Type")
plt.xlabel("Pollutant Type")
plt.ylabel("Average Pollution Level")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# Scatter plot: State-wise Pollutant Type Variation
# This scatter plot shows the variation in pollution levels by state and pollutant type
state_pollutant_avg = df.groupby(['state', 'pollutant_id'])['pollutant_avg'].mean().reset_index()

plt.figure(figsize=(14, 8))
sns.scatterplot(data=state_pollutant_avg, x='state', y='pollutant_avg', hue='pollutant_id', s=100)
plt.title("State-wise Pollutant Type Variation")
plt.xlabel("State")
plt.ylabel("Average Pollution Level")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# Scatter plot: Pollution Distribution by Latitude and Longitude
# This scatter plot shows the pollution distribution across the latitude and longitude of monitoring stations
custom_greys = LinearSegmentedColormap.from_list(
    "custom_greys", ["#B0B0B0", "#3A3A3A"]
)

plt.figure(figsize=(8, 10))

plt.gca().set_facecolor('#E8E8E8')
plt.gcf().set_facecolor('#E8E8E8')

scatter = plt.scatter(
    df['longitude'],
    df['latitude'],
    c=df['pollutant_avg'],
    cmap=custom_greys,
    s=20,
    alpha=0.8
)

cbar = plt.colorbar(scatter, label='Average Pollution Level')
cbar.ax.yaxis.label.set_color('black')
cbar.ax.tick_params(colors='black')

plt.title("Pollution Distribution by Latitude and Longitude", color='black')
plt.xlabel("Longitude", color='black')
plt.ylabel("Latitude", color='black')

plt.xticks(color='black')
plt.yticks(color='black')

plt.tight_layout()

plt.show()



# Z-Test: Compare pollution levels between two states
# Performing a Z-test to compare the pollution levels between two states, e.g., 'State1' and 'State2'
state1_pollution = df[df['state'] == 'State1']['pollutant_avg'].dropna()
state2_pollution = df[df['state'] == 'State2']['pollutant_avg'].dropna()

print(f"State1 entries: {len(state1_pollution)}, State2 entries: {len(state2_pollution)}")

if len(state1_pollution) > 0 and len(state2_pollution) > 0:
    z_stat, p_val = ztest(state1_pollution, state2_pollution)
    print(f"\nZ-statistic: {z_stat:.2f}, P-value: {p_val:.4f}")
    if p_val < 0.05:
        print("Significant difference in pollution levels between State1 and State2.")
    else:
        print("No significant difference found.")
else:
    print("Not enough data to perform Z-test.")