### Import libraries
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import date
import requests


st.title("Recipes Based On User Preferences")
# Load the dataset
df =pd.read_csv("data/preprocessed/recipes.csv")


# Now display the DataFrame
st.write(df.head(5))



# Let's add a sidebar for navigation and the page names

#st.sidebar.page_link(page='pages/food_recommendation.py',label='Food Recommendation', icon='📊')
#st.sidebar.page_link(page='deficiency_EDA.py', label='Recipe Selection',icon ='💡')
#st.sidebar.write('---')

# Getting user preferences
st.sidebar.write('Select Preferences')

calories = st.sidebar.slider(label='Calories', min_value= df['Calories'].min(), max_value= df['Calories'].max())
Fat = st.sidebar.slider(label='Fat', min_value= df['FatContent'].min(), max_value= df['FatContent'].max())
Saturated_fat = st.sidebar.slider(label='Saturated Fat',min_value= df['SaturatedFatContent'].min(), max_value= df['SaturatedFatContent'].max())
Cholesterol = st.sidebar.slider(label='Cholesterol',min_value= df['CholesterolContent'].min(), max_value= df['CholesterolContent'].max())
Sodium = st.sidebar.slider(label='Sodium', min_value= df['SodiumContent'].min(), max_value= df['SodiumContent'].max())
Carbohydrate = st.sidebar.slider(label='Carbohydrate',min_value= df['CarbohydrateContent'].min(), max_value= df['CarbohydrateContent'].max())
Fiber = st.sidebar.slider(label='Fiber',min_value= df['FiberContent'].min(), max_value= df['FiberContent'].max())
Sugar = st.sidebar.slider(label='Sugar',min_value= df['SugarContent'].min(), max_value= df['SugarContent'].max())
Protein = st.sidebar.slider(label='Protein',min_value= df['ProteinContent'].min(), max_value= df['ProteinContent'].max())

