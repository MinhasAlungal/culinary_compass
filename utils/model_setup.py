import streamlit as st
from sentence_transformers import SentenceTransformer
import torch
import os
import warnings
warnings.filterwarnings('ignore')

# Force CPU usage and disable CUDA
os.environ["CUDA_VISIBLE_DEVICES"] = ""
torch.set_num_threads(1)

def init_model():
    """Initialize the model with specific settings"""
    try:
        with st.spinner('Loading model...'):
            model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
            return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Cache the model globally
if 'model' not in st.session_state:
    st.session_state['model'] = init_model()

def get_model():
    """Get the cached model"""
    return st.session_state.get('model') 