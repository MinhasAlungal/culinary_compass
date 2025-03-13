from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import os

app = FastAPI()

class UserHistory(BaseModel):
    name: str
    age: int
    gender: str
    weight: float
    height: float
    bmi: float
    bmi_category: str
    food_preference: str
    deficiencies: list
    recommendation: str

HISTORY_FILE = "history.xlsx"
SHEET_NAME = 'User History'

@app.post("/save-history/")
async def save_history(data: UserHistory):
    """Save user details and recommendation to Excel file."""
    try:
        new_entry = {
            "Timestamp": datetime.now(),
            "Name": data.name,
            "Age": data.age,
            "Gender": data.gender,
            "Weight (kg)": data.weight,
            "Height (m)": data.height,
            "BMI": data.bmi,
            "BMI Category": data.bmi_category,
            "Food Preference": data.food_preference,
            "Deficiencies": ", ".join(data.deficiencies) if data.deficiencies else "None",
            "Recommendation": data.recommendation
        }

        df = pd.DataFrame([new_entry])
        if os.path.exists(HISTORY_FILE):
            existing_df = pd.read_excel(HISTORY_FILE)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(HISTORY_FILE, index=False, sheet_name=SHEET_NAME)
        return {"message": "History saved successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-history/")
async def get_history():
    """Retrieve all history records."""
    try:
        if os.path.exists(HISTORY_FILE):
            return {"history": pd.read_excel(HISTORY_FILE).to_dict(orient='records')}
        return {"history": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
