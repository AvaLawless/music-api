## Final Case Study for DS 2022 by Ava Lawless

### 1) Executive Summary

This final project creates a dashboard based on a data set of Billboard's Hot 100 Songs of 2024. It allows users to interact with the data and clearly see the overall summary of the most popular songs of 2024. They can see the overall statistics, top ten songs, and the most engaged songs out of the list. This is for anyone who is curious about pop music and wants to see what kinds of songs were most popular last year in a concise format.

### 2) System Overview

In this case study, I wanted to create a website with an HTML dashboard like we did for the first assignment about NYC data. To do this with strategies learned in class, I used Flask, Pandas, and an app.py file to create the backend of the website. Flask API is used to create the website with Python code. It runs an API using HTTP requests.

#### Architecture Diagram:
View assets folder

#### Data/Models/Services
Data: Top 100 Songs of 2024 - Billboard Hot 100
Format: CSV (100 Rows, 9 Columns)
Size: 50 KB
License: Public Data (Billboard)
Columns: channel, title, published, description, views, likes, dislikes, comments

### 3) How to Run (local)

**1. Clone or Download the Repository**

git clone https://github.com/AvaLawless/music-api.git

cd music-api

**2. Create a Virtual Environment**

Windows:

python -m venv venv

venv\Scripts\activate

Mac/Linux:

bashpython3 -m venv venv

source venv/bin/activate


**3. Install Dependencies**

bashpip install -r requirements.txt

This installs Flask, pandas, and flask-cors.

**4. Run the Flask Application**

python app.py

**5. Access the Application**
   
Open your web browser and go to:

Web Dashboard (Frontend):

http://localhost:5000/dashboard

You can also check these endpoints:

http://localhost:5000/ - API documentation

http://localhost:5000/stats/summary - Overall statistics

http://localhost:5000/stats/top/10 - Top 10 songs

http://localhost:5000/stats/engagement - Engagement analysis

http://localhost:5000/health - Health check

**6. Stop the Server**

Use ctrl+C to stop running the app.py

### Alternative: Use Docker

docker build -t music-api:latest .

docker run --rm -p 5000:5000 music-api:latest

### 4) Design Decisions

Why this Concept? I wanted to make a simple interactive platform. I could have used other data similar to music, such as the most popular TV shows or Movies of 2024.

Tradeoffs: Flask is good for a small web project like this, but it may not be the best for larger data sets.

Security/Privacy: This project uses public data.

Ops: Logging: Flask default logging to console

Metrics: Can track request counts via Flask middleware (not implemented)

Scaling: Single-instance sufficient for this data size

Limitations:

Data loaded once at startup (no refresh without restart)

In-memory only (no persistence)

Single-threaded (fine for <1000 requests/sec)

### 5) Results and Evaluation

View assets folder for screenshot

Summary Statistics Example:

Total views across all 100 songs: 17+ billion

Average views per song: 178 million

Most viewed: "Calm Down" by Rema & Selena Gomez (1 billion+ views)

100 unique artists/channels

### 6) What's Next

This code could be applied to other CSV files of music data or other media, such as TV shows or movies, as described earlier. Or, just using this data, there could be more features added to the website, such as top songs per month over the course of the year. 

### 7) Links

**GitHub Repo:** github.com/AvaLawless/music-api



