### Import libraries
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
#import plotly.express as px

# this is how we import streamlit
import streamlit as st

st.title("Recipes Based On User Preferences")

# Load the data set
df = pd.read_excel("data/food_data.xlsx")





# Let's add a sidebar for navigation and the page names

#st.sidebar.page_link(page='pages/food_recommendation.py',label='Food Recommendation', icon='📊')
#st.sidebar.page_link(page='deficiency_EDA.py', label='Recipe Selection',icon ='💡')
#st.sidebar.write('---')

# Getting user preferences
st.sidebar.write('Select Preferences')

calories = st.sidebar.slider(label='Calories', min_value=0, max_value=100)
Fat = st.sidebar.slider(label='Fat', min_value=0, max_value=100)
Saturated_fat = st.sidebar.slider(label='Saturated Fat', min_value=0, max_value=100)
Cholesterol = st.sidebar.slider(label='Cholesterol', min_value=0, max_value=100)
Sodium = st.sidebar.slider(label='Sodium', min_value=0, max_value=100)
Carbohydrate = st.sidebar.slider(label='Carbohydrate', min_value=0, max_value=100)
Fiber = st.sidebar.slider(label='Fiber', min_value=0, max_value=100)
Sugar = st.sidebar.slider(label='Sugar', min_value=0, max_value=100)
Protein = st.sidebar.slider(label='Protein', min_value=0, max_value=100)

