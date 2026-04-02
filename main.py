from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# A simple in-memory list to simulate a database
fake_db = []

# Pydantic model for item validation
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True  # Default value set to True


# GET route for the root URL
@app.get("/")
async def root():
    return {"message": "Hello World"}


# GET route that returns fake weather data
@app.get("/weather")
async def get_weather():
    return {
        "location": "Berlin",
        "temperature_celsius": 24,
        "condition": "Sunny",
        "forecast": "Clear skies all day"
    }


# POST route to add a new item to the database
@app.post("/items")
async def create_item(item: Item):
    # Convert item to a dictionary and store it in the fake DB
    fake_db.append(item.model_dump())


# GET route to retrieve all items from the database
@app.get("/items")
async def read_items():
    return {"items": fake_db}


# Run the app: uvicorn main:app --reload
# Visit the API docs at: http://localhost:8000/docs