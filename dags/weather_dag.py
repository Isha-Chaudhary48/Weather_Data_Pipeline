
from airflow.sdk import dag, task
from pendulum import datetime
from dotenv import load_dotenv
import os
import requests
import psycopg2
from supabase import create_client


load_dotenv()



API_KEY = os.getenv("API_KEY")
DB_URI = os.getenv("DB_URI")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")



@dag(
    dag_id="weather_dag",
    start_date= datetime(2026,4,20,tz = "Asia/Kolkata"),
    end_date = datetime(2026,5,10,tz = 'Asia/Kolkata'),
    schedule = "@daily",
    catchup = False,
    tags=['weather']
)

def weather_dag_func():

    @task
    def fetch_cities():
        supabase_cities = create_client(SUPABASE_URL,SUPABASE_KEY)
        response = supabase_cities.table("cities_india").select("*").execute()
        cities = response.data
        return cities
        

    @task
    def fetch_weather_data(cities):
        all_weather = []

        for row in cities:
            lat = row["latitude"]
            lon = row["longitude"]

            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                continue

            all_weather.append(data)

        return all_weather
    
           


    
    @task
    def process_weather_data(all_weather):
        
        results = []

        for data in all_weather:
            weather = data['weather'][0]['description']
            main = data['main']
            wind = data['wind']
            weather_info = {
            'city': data['name'],
            'temperature': main['temp'],
            'humidity':main['humidity'],
            'feels_like': main['feels_like'],
            'wind_speed': wind['speed'],
            'heat_index': round(main['temp'] + (0.33 * main['humidity'])-4,2),
            'is_windy':wind['speed'] > 10,
            'weather':weather


        }
            results.append(weather_info)  
       
        return results

    @task
    def load_data(data_list):
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        try:
            for data in data_list:
                cur.execute("""
                INSERT INTO weather_data(city,temperature,humidity,feels_like,wind_speed,heat_index,is_windy,weather)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)                
                    """,(
                        data['city'],
                        data['temperature'],
                        data['humidity'],
                        data['feels_like'],
                        data['wind_speed'],
                        data['heat_index'],
                        data['is_windy'],
                        data['weather']

                    ))
            conn.commit()
            print("Data inserted")
            
        
        finally:
             cur.close()
             conn.close()
             print("Data is inserted in the database")

    cities = fetch_cities()
    fetch = fetch_weather_data(cities)
    processed = process_weather_data(fetch)
    load_data(processed)


weather_dag = weather_dag_func()