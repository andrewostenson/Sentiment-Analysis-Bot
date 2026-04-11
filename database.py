import sqlite3

def create_table():
    connection = sqlite3.connect("reddit_posts.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, subreddit TEXT, sentiment TEXT, " \
    "confidence_pos REAL, confidence_neu REAL, confidence_neg REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    connection.commit()

def insert_post(title, subreddit, sentiment, confidence_pos, confidence_neu, confidence_neg, timestamp):
    connection = sqlite3.connect("reddit_posts.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO posts (title, subreddit, sentiment, confidence_pos, confidence_neu, confidence_neg, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (title, subreddit, sentiment, confidence_pos, confidence_neu, confidence_neg, timestamp))
    connection.commit()