from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI()
calls = 0
weather_dict = {"Copenhagen": {"23/07/23": '🌞', "24/07/23": '💧'},
                "Seattle": {"23/07/23": '🌥️', "24/07/23": "🌞"},
                "Berlin": {"23/07/23": "💧", "24/07/23": "🌥️"}}

@app.get("/weather/{location}")
def get_weather(location: str):
    global calls
    if calls==0:
        today = "23/07/23"
    else:
        today = "24/07/23"

    # today = datetime.today().strftime('%d/%m/%y')
    calls += 1
    return weather_dict[location][today]

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
