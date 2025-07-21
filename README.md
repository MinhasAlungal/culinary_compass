# 🧭 Culinary Compass – NLP-Based Food & Recipe Recommendation System

**Technologies:** Python, Streamlit, FastAPI, KNN, Sentence Transformers, Matplotlib, Seaborn, Git

**Live Demo:** 👉 [Try the App](https://huggingface.co/spaces/minhasalungal/culinarycompass) 

Culinary Compass is a recommendation system designed to suggest foods and recipes tailored to users' **micronutrient deficiencies** (e.g., Iron, Vitamin D), **nutritional goals**, and **dietary preferences** (e.g., vegetarian, non-vegetarian).

## 🔧 Project Overview

The system is built as a two-module pipeline:

- **Module 1 – Food Recommendation:**  
  Utilizes **K-Nearest Neighbors (KNN)** to recommend foods based on user-input deficiencies and dietary goals.

- **Module 2 – Recipe Recommendation:**  
  Uses **Sentence Transformers** to recommend recipes that align with selected foods and user-defined nutritional targets (e.g., calories, protein, fiber, etc.).

## 🌐 Features

- Interactive UI built with **Streamlit** for seamless user input and food selection.
- Backend APIs deployed using **FastAPI** for scalable and modular architecture.
- Data visualizations created using **Matplotlib** and **Seaborn** to explore trends and insights.
- Version-controlled with **Git** for reproducibility and collaboration.

## 🚀 Use Case

1. User enters basic health metrics and dietary preferences.
2. System recommends foods rich in deficient nutrients.
3. User selects preferred foods and specifies nutrition targets.
4. Recipes are recommended that best match those foods and goals.



## Requirements:

- pyenv with Python: 3.11.3

### Setup

Use the requirements file in this repo to create a new environment.

```BASH
make setup

#or

pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```











