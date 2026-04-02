from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/weather")
async def get_weather():
    return {
        "location": "Berlin",
        "temperature_celsius": 24,
        "condition": "Sunny",
        "forecast": "Clear skies all day"
    }