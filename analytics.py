import database

def average_sentiment(start_date, end_date):
    df = database.fetch_filtered_posts(start_date=start_date, end_date=end_date)
    if df.empty:
        return None

    avg_pos = df['confidence_pos'].mean()
    avg_neg = df['confidence_neg'].mean()
    
    avg_sentiment = avg_pos - avg_neg
    return avg_sentiment