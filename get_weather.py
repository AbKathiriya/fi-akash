## ----------------------------------- Instructions Section ------------------------------------ ##
# 1. To get your own api key go to this link and sign up: http://openweathermap.org/appid
# 2. After sign up go to API keys tab. There you will find your API key
## --------------------------------- End Instructions Section ---------------------------------- ##
import requests
import json
import csv
## ----------------------------------- Configuration Section ------------------------------------ ##
city = 'London'
api_key = config.weather_key        # Put your API key here
## --------------------------------- End Configuration Section ---------------------------------- ##
if __name__ == '__main__':
    url = 'http://api.openweathermap.org/data/2.5/weather?q=London&APPID='+ api_key
    response = requests.get(url).json()
    print json.dumps(response, indent = 4 )
