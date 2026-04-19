from transformers import pipeline

sentiment_analysis = pipeline(task="sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", top_k=None)

def run_sentiment(title):
    sentiment_results = sentiment_analysis(title)
    return sentiment_results