from curses import reset_prog_mode
from datetime import datetime
import time
import sympy as sp
import re
import requests
import json



def get_current_time():
    return datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")

def set_timer(seconds, botName):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(f"{botName}: Timer is currently on {timer}", end="\r")
        time.sleep(1)
        seconds -= 1
    print(f"{botName}: Your timer has ended now at {get_current_time()}!")


def mathsSolver(expression):
    if any(i.isdigit() for i in expression) == False:
        return (10/0)
        
    expression = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expression.replace("^", "**"))

    try:
        if "=" in expression:
            left_side, right_side = expression.split("=")
            equation = sp.Eq(sp.sympify(left_side), sp.sympify(right_side))
        else:
            equation = sp.Eq(sp.sympify(expression), 0)

        # Solve the equation
        print(sp.solve(equation))
        return sp.solve(equation)
    except Exception as e:
        return f"Error: {str(e)}"



def weatherFind(city):
    apiKey = "22b63fcd5b84f8b7b6c6f6607b74269a"
    lat, lon = LatLon(city, apiKey)
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apiKey}")
    data = response.json()
    weather, weatherDesc = (data["weather"][0]["main"]), (data["weather"][0]["description"])
    temp, minTemp, maxTemp = data["main"]["temp"], data["main"]["temp_min"], data["main"]["temp_max"]
    return weather, weatherDesc, temp, minTemp, maxTemp


def LatLon(CityName, apiKey):
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={CityName}&appid={apiKey}")
    data = response.json()
    if data:
        return data[0]["lat"], data[0]["lon"]
    else:
        raise Exception("error finding LatLon")


