# -*- coding: utf-8 -*-
"""DHV_PROJECT.ipynb"""

import pandas as pd
import numpy as np

df = pd.read_csv('/content/climate_change_indicators.csv')

df.head()

df.tail()

df.info()

df.isna().any()

missing_values = df.iloc[:, :10].isnull().sum()

missing_values

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

# Time Series Plot of Global Average Temperature Change

# Calculate the global average temperature change for each year
years = [col for col in df.columns if col.startswith('F')]
global_avg_temp_change = df[years].mean()

# Convert years from string 'FYYYY' to integer YYYY for plotting
int_years = [int(year[1:]) for year in years]

# Time Series Plot
plt.figure(figsize=(14, 7))
plt.plot(int_years, global_avg_temp_change, marker='o', linestyle='-', color='b')
plt.title('Global Average Temperature Change Over Years', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Average Temperature Change (°C)', fontsize=14)
plt.xticks(int_years[::5], rotation=45)  # Show every 5th year for clarity
plt.grid(True)
plt.show()

# For the heatmap, we'll select a subset of years for better visibility and clarity
selected_years = ['F2010', 'F2012', 'F2014', 'F2016', 'F2018', 'F2020', 'F2022']
heatmap_data = df.set_index('Country')[selected_years].dropna()  # Drop countries with missing values for simplicity

# Creating a heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(heatmap_data, cmap='coolwarm')
plt.title('Heatmap of Temperature Changes (2010, 2012, 2014, 2016, 2018, 2020, 2022)', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Country', fontsize=14)
plt.show()

# For the box plot, we'll categorize the years into decades for simplicity

# Creating a new DataFrame with year as a column and a new decade column

decade_data = pd.melt(df, id_vars=['Country'], value_vars=years, var_name='Year', value_name='TempChange')
decade_data['Decade'] = decade_data['Year'].apply(lambda x: x[1:4] + "0s")  # Group years into decades

# Creating the box plot
plt.figure(figsize=(12, 8))
sns.boxplot(x='Decade', y='TempChange', data=decade_data)
plt.title('Distribution of Temperature Changes by Decade', fontsize=16)
plt.xlabel('Decade', fontsize=14)
plt.ylabel('Temperature Change (°C)', fontsize=14)
plt.xticks(rotation=45)
plt.show()

# Set the plot size for better readability
plt.figure(figsize=(10, 6))

# Create the histogram for temperature changes in 2022
sns.histplot(df['F2022'], color='skyblue', kde=True)

# Add a title to the plot
plt.title('Distribution of Temperature Changes in 2022', fontsize=16)

# Label the axes
plt.xlabel('Temperature Change (Degree Celsius)', fontsize=14)
plt.ylabel('Frequency', fontsize=14)

# Show the plot
plt.show()

# Data Preparation
# Dropping rows with missing values in the specified columns to keep the example simple
df_clean = df[['F2020', 'F2021', 'F2022']].dropna()

# Feature Selection
X = df_clean[['F2020', 'F2021']].values  # Features: Temperature changes in 2020 and 2021
y = df_clean['F2022'].values  # Target: Temperature changes in 2022

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Evaluation
r2 = r2_score(y_test, y_pred)

r2

year_list = []
for i in range(1963, 2023):
    year = f"F{i}"
    year_list.append(year)

df_melt = pd.melt(df, id_vars = ["Country"], value_vars = year_list)
df_melt.rename(columns={"variable":"Year", "value":"Tempurate_Change"}, inplace = True)
df_melt['Year'] = df_melt['Year'].str.replace(r'F', '', regex=True)
df_melt['Year'] = df_melt['Year'].astype(int)

df_melt.head()

import plotly.express as px
top_countries_year = df_melt.groupby(["Year", "Country"])["Tempurate_Change"].mean().reset_index()
top_countries_year = top_countries_year.groupby("Year").apply(lambda x: x.nlargest(1, "Tempurate_Change")).reset_index(drop=True)
top_countries_year = top_countries_year[top_countries_year["Year"] > 1999]
fig = px.bar(top_countries_year.sort_values("Year", ascending=False), x='Year', y='Tempurate_Change', color='Tempurate_Change',color_continuous_scale = 'orrd', title='The country with the maximum temperature change for each year', text="Country",labels={'Tempurate_Change': 'Tempuarete Cahnge (°C)'})

fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),plot_bgcolor='rgba(0,0,0,0)')
fig.show()

from wordcloud import WordCloud
from wordcloud import STOPWORDS

df_word=pd.read_csv('/content/climate_change_indicators.csv', usecols=['Country'])
df_word.head()

text=''.join(item for item in df_word['Country'])
print(text)

stopwords=set(STOPWORDS)

wordcloud=WordCloud(stopwords=stopwords,background_color='white').generate(text)
plt.figure(figsize=(15,10))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.margins(x=0,y=0)
plt.show()

wordcloud=WordCloud(background_color='white',max_words=100,max_font_size=300,width=800,height=500,colormap='magma').generate(text)
plt.figure(figsize=(20,20))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.margins(x=0,y=0)

# prompt: cleate more types of plots using sns

# Create a line plot
sns.lineplot(data=df_clean[['F2020', 'F2021', 'F2022']])
plt.xlabel('Year')
plt.ylabel('Temperature Change')
plt.title('Line Plot of Temperature Changes')
plt.show()

# Create a violin plot
sns.violinplot(y='F2022', data=df)
plt.xlabel('Temperature Change in 2022')
plt.title('Violin Plot of Temperature Changes')
plt.show()

sns.swarmplot(y='F2021', data=df)
plt.xlabel('Temperature Change in 2022')
plt.title('swarm Plot of Temperature Changes')
plt.show()
