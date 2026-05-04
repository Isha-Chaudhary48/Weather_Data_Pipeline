# 🌦️ Weather Data Pipeline using Airflow

## 📌 About the Project

In this project, I have built a data pipeline using Apache Airflow. It fetches weather data from an API, processes it, and stores it into a cloud database (Supabase PostgreSQL).

The pipeline runs daily and helps in understanding how real-world data pipelines work.

---

## 🚀 What it does

* Fetches weather data from OpenWeather API
* Processes the data (temperature, humidity, etc.)
* Stores the data into PostgreSQL database
* Runs automatically using Airflow DAG

---

## 🛠️ Tech Used

* Python
* Apache Airflow
* PostgreSQL (Supabase)
* Requests
* Psycopg2
* dotenv

---

## 📂 Project Structure

```id="g7z5mj"
dags/
  weather_dag.py   # main pipeline code

.env.example       # sample env file
pyproject.toml     # dependencies
uv.lock            # lock file
airflow.cfg        # airflow config
```

---

## ⚙️ How to run

### 1. Clone repo

```id="h9s7w2"
git clone <your-repo-link>
cd Data_Pipeline_Weather
```

---

### 2. Create `.env` file

```id="6mkl09"
API_KEY=your_api_key
CITIES=[]
DB_URI=your_database_connection_string
```

---

### 3. Install dependencies

```id="pmu9m1"
uv pip install -r requirements.txt
```

---

### 4. Run Airflow

```id="c0vhp7"
uv run --env-file .env airflow standalone
```

---

### 5. Trigger DAG

* Open http://localhost:8080
* Search `weather_dag`
* Trigger it

---

## 🗄️ Database Table

```id="s3psn3"
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city TEXT,
    temperature FLOAT,
    humidity FLOAT,
    feels_like FLOAT,
    wind_speed FLOAT,
    heat_index FLOAT,
    is_windy BOOLEAN,
    weather TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🧠 What I learned

* How to build a data pipeline using Airflow
* How to work with APIs
* How to store data in cloud database
* Handling errors like connection issues, encoding, etc.

---

## 🚀 Future improvements

* Run tasks in parallel
* Add dashboard for visualization

---

## 👩‍💻 Author

Isha
