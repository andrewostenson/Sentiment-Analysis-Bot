import database

def average_sentiment(start_date, end_date):
    df = database.fetch_filtered_posts(start_date=start_date, end_date=end_date)
    if df.empty:
        return None

    avg_pos = df['confidence_pos'].mean()
    avg_neg = df['confidence_neg'].mean()
    
    avg_sentiment = avg_pos - avg_neg
    return avg_sentiment

def highest_scored_stories(start_date, end_date, sentiment_type):
    df = database.fetch_filtered_posts(start_date=start_date, end_date=end_date)
    if df.empty:
        return None

    if sentiment_type == "positive":
        highest_stories = df.nlargest(5, 'confidence_pos')
    elif sentiment_type == "negative":
        highest_stories = df.nlargest(5, 'confidence_neg')
    else:
        return None

    return highest_stories