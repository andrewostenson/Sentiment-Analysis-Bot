import sqlite3
import pandas as pd

def create_table():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, source TEXT, sentiment TEXT, " \
    "confidence_pos REAL, confidence_neu REAL, confidence_neg REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, UNIQUE(title, source))")
    connection.commit()

def insert_post(title, source, sentiment, confidence_pos, confidence_neu, confidence_neg, timestamp):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO posts (title, source, sentiment, confidence_pos, confidence_neu, confidence_neg, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (title, source, sentiment, confidence_pos, confidence_neu, confidence_neg, timestamp))
    connection.commit()

def delete_all_posts():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM posts")
    connection.commit()

def fetch_filtered_posts(start_date=None, end_date=None, sentiment_filter=None, keyword_filter=None):
    connection = sqlite3.connect("data.db")

    query = "SELECT * FROM posts WHERE 1=1"
    params = []

    if start_date and end_date:
        query += " AND timestamp BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    
    if sentiment_filter and sentiment_filter != "All":
        query += " AND sentiment = ?"
        params.append(sentiment_filter)
    
    if keyword_filter:
        query += " AND (title LIKE ? OR source LIKE ?)"
        keyword_param = f"%{keyword_filter}%"
        params.extend([keyword_param, keyword_param])
    
    df = pd.read_sql_query(query, connection, params=params)
    return df


def db_to_dataframe():
    connection = sqlite3.connect("data.db")
    df = pd.read_sql_query("SELECT * FROM posts", connection)
    return df