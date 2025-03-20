"""
    This python script is related to the Eda part of our Streamlit Web App.
"""

### Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# this is how we import streamlit
import streamlit as st
st.title("Lets Explore the Deficiency Data")
# Reading the data
df=pd.read_excel("data/EDA/deficiency_data.xlsx")
print(df.head())
# Count occurrences of each deficiency per gender
df_counts = df.groupby(["Predicted Deficiency", "Gender"]).size().reset_index(name="Count")
# Sort by Count (Descending)
df_counts = df_counts.sort_values(by="Count", ascending=False)
# Create an interactive bar chart
fig = px.bar(df_counts, x="Predicted Deficiency", y="Count", color="Gender", barmode="group",
             title="Gender-wise Nutrient Deficiencies")
# Display in Streamlit
st.plotly_chart(fig)
# Load the data set
# penguins = pd.read_excel("data/food_data.xlsx")
# st.dataframe(penguins)
# # plot the data in heatmap
# st.write("Heatmap of the data")
# sns.heatmap(penguins.corr(), annot=True)
# st.pyplot()