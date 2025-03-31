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

# second plot deficiencies and diseases
st.title("Deficiency & Disease Analysis")

# Multiselect filter for deficiencies
selected_deficiencies = st.multiselect("Select nutrient deficiencies:", df["Predicted Deficiency"].unique(), default=df["Predicted Deficiency"].unique())

# Filter dataset based on selected deficiencies
filtered_df = df[df["Predicted Deficiency"].isin(selected_deficiencies)]
print(filtered_df.columns)
columns= ['Age', 'Gender', 'Diet Type', 'Living Environment', 'Night Blindness',
       'Dry Eyes', 'Bleeding Gums', 'Fatigue', 'Tingling Sensation',
       'Low Sun Exposure', 'Reduced Memory Capacity', 'Shortness of Breath',
       'Loss of Appetite', 'Fast Heart Rate', 'Brittle Nails', 'Weight Loss',
       'Reduced Wound Healing Capacity', 'Skin Condition',
       'Predicted Deficiency']

# Compute gender-wise disease counts
genderwise_counts = filtered_df.drop(columns=["Predicted Deficiency", "Age", "Diet Type", "Living Environment", "Low Sun Exposure"]).groupby("Gender").sum().reset_index()

# Melt DataFrame for Plotly
melted_df = genderwise_counts.melt(id_vars=["Gender"], var_name="Disease", value_name="Count")

# Plotly Bar Chart
fig = px.bar(
    melted_df,
    x="Disease",
    y="Count",
    color="Gender",
    barmode="group",
    title="Disease Counts by Gender",
    labels={"Count": "Number of Cases", "Disease": "Disease"},
    text="Count"
)

# Display Plot
st.plotly_chart(fig, use_container_width=True)
# Load the data set
# penguins = pd.read_excel("data/food_data.xlsx")
# st.dataframe(penguins)
# # plot the data in heatmap
# st.write("Heatmap of the data")
# sns.heatmap(penguins.corr(), annot=True)
# st.pyplot()