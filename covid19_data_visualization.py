import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests

# Step 1: Fetch COVID-19 Data from an API
def fetch_covid_data():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)

# Step 2: Data Preprocessing
def preprocess_data(df):
    # Selecting relevant columns
    df = df[['country', 'cases', 'todayCases', 'deaths', 'todayDeaths', 'recovered', 'active', 'critical', 'casesPerOneMillion', 'deathsPerOneMillion', 'tests', 'population']]
    df['cases_per_100k'] = df['cases'] / df['population'] * 100000
    df['deaths_per_100k'] = df['deaths'] / df['population'] * 100000
    return df

# Step 3: Create Visualizations
def create_visualizations(df):
    # 3.1 Plotting Top 10 Countries by Total Cases
    top10_cases = df.nlargest(10, 'cases')
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='cases', y='country', data=top10_cases)
    plt.title("Top 10 Countries by Total COVID-19 Cases")
    plt.xlabel("Total Cases")
    plt.ylabel("Country")
    plt.show()

    # 3.2 Plotting Total Cases vs Total Deaths with Scatterplot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='cases', y='deaths', data=df, hue='country', s=100)
    plt.title("Total COVID-19 Cases vs Deaths by Country")
    plt.xlabel("Total Cases")
    plt.ylabel("Total Deaths")
    plt.show()

    # 3.3 Interactive World Map (Cases per 100,000 People)
    fig = px.choropleth(df, locations="country", locationmode="country names",
                        color="cases_per_100k", hover_name="country", 
                        title="COVID-19 Cases per 100,000 People",
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.show()

# Step 4: Main Execution
def main():
    # Fetch the data
    covid_data = fetch_covid_data()
    
    # Preprocess the data
    covid_data_clean = preprocess_data(covid_data)
    
    # Generate visualizations
    create_visualizations(covid_data_clean)

if __name__ == "__main__":
    main()
