import psycopg
import os
import pandas as pd


conn = psycopg.connect(os.environ.get('DATABASE_URL'))

def create_table():
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (id SERIAL PRIMARY KEY, title TEXT, source TEXT, sentiment TEXT, " \
    "confidence_pos REAL, confidence_neu REAL, confidence_neg REAL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(title, source))")
    conn.commit()

def insert_post(title, source, sentiment, confidence_pos, confidence_neu, confidence_neg, timestamp):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, source, sentiment, confidence_pos, confidence_neu, confidence_neg, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (title, source) DO NOTHING",
                   (title, source, sentiment, confidence_pos, confidence_neu, confidence_neg, timestamp))
    conn.commit()

def delete_all_posts():
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts")
    conn.commit()

def fetch_filtered_posts(start_date=None, end_date=None, sentiment_filter=None, keyword_filter=None):
    query = "SELECT * FROM posts WHERE 1=1"
    params = []

    if start_date and end_date:
        query += " AND timestamp BETWEEN %s AND %s"
        params.extend([start_date, end_date])
    
    if sentiment_filter and sentiment_filter != "All":
        query += " AND sentiment = %s"
        params.append(sentiment_filter)
    
    if keyword_filter:
        query += " AND (title ILIKE %s OR source ILIKE %s)"
        keyword_param = f"%{keyword_filter}%"
        params.extend([keyword_param, keyword_param])
    
    df = pd.read_sql_query(query, conn, params=params)
    return df


def db_to_dataframe():
    df = pd.read_sql_query("SELECT * FROM posts", conn)
    return df