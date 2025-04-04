"""
Streamlit Web App for analyzing nutrient deficiency data and related diseases.
"""

import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# Constants
DATA_PATH = Path("data/EDA/deficiency_data.xlsx")
DISEASE_COLUMNS = [
    'Age', 'Gender', 'Diet Type', 'Living Environment', 'Night Blindness',
    'Dry Eyes', 'Bleeding Gums', 'Fatigue', 'Tingling Sensation',
    'Low Sun Exposure', 'Reduced Memory Capacity', 'Shortness of Breath',
    'Loss of Appetite', 'Fast Heart Rate', 'Brittle Nails', 'Weight Loss',
    'Reduced Wound Healing Capacity', 'Skin Condition', 'Predicted Deficiency'
]

def load_data(file_path: Path) -> pd.DataFrame:
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

def create_deficiency_chart(df: pd.DataFrame):
    st.markdown('<div class="custom-subheader">Gender-wise Nutrient Deficiencies</div>', unsafe_allow_html=True)
    
    df_counts = (
        df.groupby(["Predicted Deficiency", "Gender"])
        .size()
        .reset_index(name="Count")
        .sort_values(by="Count", ascending=False)
    )
    
    fig = px.bar(
        df_counts,
        x="Predicted Deficiency",
        y="Count",
        color="Gender",
        barmode="group",
        title="Gender-wise Nutrient Deficiencies"
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        width=500,
        title_font=dict(size=16),  # Title font size
        xaxis=dict(
            title_font=dict(size=14),  # X-axis title font size
            tickfont=dict(size=12)     # X-axis tick labels font size
        ),
        yaxis=dict(
            title_font=dict(size=14),  # Y-axis title font size
            tickfont=dict(size=12)     # Y-axis tick labels font size
        ),
        legend=dict(
            title_font=dict(size=14),  # Legend title font size
            font=dict(size=12)         # Legend items font size
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_disease_analysis(df: pd.DataFrame):
    st.markdown('<div class="custom-subheader">Deficiency & Disease Analysis</div>', unsafe_allow_html=True)
    
    selected_deficiencies = st.multiselect(
        "Select nutrient deficiencies:",
        df["Predicted Deficiency"].unique(),
        default=df["Predicted Deficiency"].unique()
    )
    
    filtered_df = df[df["Predicted Deficiency"].isin(selected_deficiencies)]
    
    columns_to_drop = ["Predicted Deficiency", "Age", "Diet Type", "Living Environment", "Low Sun Exposure"]
    genderwise_counts = (
        filtered_df
        .drop(columns=columns_to_drop)
        .groupby("Gender")
        .sum()
        .reset_index()
    )
    
    melted_df = genderwise_counts.melt(
        id_vars=["Gender"],
        var_name="Disease",
        value_name="Count"
    )
    
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
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_tickangle=-45,
        height=400,
        width=500,
        title_font=dict(size=16),  # Title font size
        xaxis=dict(
            title_font=dict(size=14),  # X-axis title font size
            tickfont=dict(size=12)     # X-axis tick labels font size
        ),
        yaxis=dict(
            title_font=dict(size=14),  # Y-axis title font size
            tickfont=dict(size=12)     # Y-axis tick labels font size
        ),
        legend=dict(
            title_font=dict(size=14),  # Legend title font size
            font=dict(size=12)         # Legend items font size
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_html_chord_chart():   
    st.markdown('<div class="custom-subheader">Ingredient Co-occurrence Chord Diagram</div>', unsafe_allow_html=True)
    with open("notebooks/chord_diagram.html", "r") as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=550, scrolling=True)

def main():
    # Custom CSS for full-width layout
    st.markdown("""
    <style>
        .main > div:first-child {
            padding-top: 0.5rem !important;
        }
        .block-container {
            padding-top: 1.25rem !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
        }
        h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        .plot-description {
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            margin: 10px 0;
        }
        .sub-container-header {
            color: #2E8B57;  /* Sea Green - represents health and nutrition */
            font-size: 22px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .custom-subheader {
            color: #FF6347;
            font-size: 26px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        /* Style for the header container */
        .header-container {
            display: flex;
            align-items: left;
            padding-top: 1rem;
            margin: 0;
            padding-bottom: 0.5rem;
        }
        .header{
            font-size: 2rem;
            font-weight: 600;
            color: #262730;
        }
        /* Style for the header icon */
        .header-icon {
            font-size: 2rem;
            margin-right: 0.3rem;
        }   
        .nutrient-info {
            text-align: right;
            color: #666666;
            font-size: 0.9rem;
            font-style: italic;
            opacity: 0.8;
        }
        .user-note {
            text-align: right;
            color: #1f77b4;  /* A nice blue color */
            font-size: 0.85rem;
            font-style: italic;
            border-radius: 4px;
        }
        .recommendation-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #262730;
            margin-bottom: 0.2rem;
            padding-bottom: 0.2rem;
            border-bottom: 2px solid #f0f2f6;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        /* Style for the page link button */
        [data-testid="stPageLink"] {
            background-color: transparent;
            border: 1px solid #e0e0e0;  
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            color: #262730 !important; 
            font-weight: 500;
            transition: all 0.2s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 1rem;
            cursor: pointer;
        }

        [data-testid="stPageLink"]:hover {
            background-color: transparent; 
            border-color: #ff4b4b; 
            color: #ff4b4b !important; 
        }

        [data-testid="stPageLink"] p {
            color: inherit !important;
            margin: 0;
            font-size: 1rem;
            font-family: 'Source Sans Pro', sans-serif;
        }

        [data-testid="stPageLink"]:hover p {
            color: #ff4b4b !important; 
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with logo using columns
    col1, col2 = st.columns([4, 2])  # Adjust column width

    with col1:
        st.markdown("""
        <div class="header-container"></div> 
        """, unsafe_allow_html=True)
        st.image("assets/CulinaryCompass.png")  # logo with banner
    with col2:
        st.markdown("""
        <div class="header-container"></div> 
        """, unsafe_allow_html=True)
    
    # Load data
    df = load_data(DATA_PATH)
    
    # First section: Deficiency Chart with description
    st.markdown('<div class="sub-container-header">Nutrient Deficiency Analysis</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        create_deficiency_chart(df)
    
    with col2:
        st.markdown("""
        <div class="plot-description">
            <h3>Understanding Nutrient Deficiencies</h3>
            <p>This visualization shows the distribution of nutrient deficiencies across different genders. 
            The data reveals important patterns in how different nutrients affect various demographic groups, 
            helping us understand where targeted nutritional interventions might be most needed.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Second section: Disease Analysis with description
    st.markdown('<div class="sub-container-header">Disease Analysis</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="plot-description">
            <h3>Disease Patterns and Nutrient Deficiencies</h3>
            <p>This analysis explores the relationship between nutrient deficiencies and various health conditions. 
            By understanding these correlations, we can better predict and prevent health issues related to 
            nutritional imbalances.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        create_disease_analysis(df)
    
    # Third section: Chord Diagram with description
    st.markdown('<div class="sub-container-header">Ingredient Relationships</div>', unsafe_allow_html=True)
    
    create_html_chord_chart()


    st.markdown("""
    <div class="plot-description">
        <h3>Ingredient Co-occurrence Analysis</h3>
        <p>The chord diagram visualizes the relationships between different ingredients in our dataset. 
        This interactive visualization helps us understand which ingredients are commonly used together 
        and can inform recipe recommendations and nutritional planning.</p>
    </div> """, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()