import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

app=Flask(__name__)

def get_weather(city):
    base_url="https://api.openweathermap.org/data/2.5/weather"
    params = { "q": city,
                "appid" : API_KEY,
                "units":"metric"
               }
    response=requests.get(base_url,params=params)
    data=response.json()

    
    if response.status_code == 200:
        return {
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "icon": data["weather"][0]["icon"]
        }
    else:
        return {"error": data.get("message", "Unable to fetch weather")}
@app.route("/",methods=["GET","POST"])
def index():
    weather=None
    if request.method=="POST":
        city=request.form.get("city")
        if city:
            weather=get_weather(city)
            weather["city"]=city
    return render_template("index.html",weather=weather)
if __name__ == "__main__":
    app.run(debug=True)
               
