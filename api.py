from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()

# Define a request model
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

# File to store history
HISTORY_FILE = "history.csv"

@app.post("/save-history/")
async def save_history(data: UserHistory):
    """Save user details and recommendation to history file."""
    entry = f"{datetime.now()},{data.name},{data.age},{data.gender},{data.weight},{data.height},{data.bmi},{data.bmi_category},{data.food_preference},{'|'.join(data.deficiencies)},{data.recommendation}"
    with open(HISTORY_FILE, "a") as file:
        file.write(entry)
    
    return {"message": "History saved successfully!"}
