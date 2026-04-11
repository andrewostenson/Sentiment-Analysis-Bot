from transformers import pipeline
import json
import database

# Load sample posts from a JSON file
with open("data/sample_posts.json", "r") as f:
    sample_posts = json.load(f)

database.create_table()  # Create the database table for storing sentiment analysis results

def sentiment():
    # Load the sentiment analysis pipeline using the specified model
    sentiment_analysis = pipeline(task="sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", top_k=None)
    return sentiment_analysis

def dump_sentiment_results(post_subreddit, post_title, sentiment_results, timestamp, dump_data):
    # Create a dictionary to store the subreddit, title, and sentiment results for the post
    post_dump = {"subreddit": post_subreddit,"title": post_title, "sentiment": sentiment_results, "timestamp": timestamp}
    dump_data.append(post_dump)
    
    with open("data/filtered_data.json", "w") as f:
        json.dump(dump_data, f, indent = 4)

if __name__ == "__main__":
    # Grab the sentiment analysis pipeline
    sentiment_analysis = sentiment()

    # Create an empty list to store the sentiment analysis results for each post
    dump_data = []

    for post in sample_posts:
        # Perform sentiment analysis on the post's title, print the results
        post_subreddit = post["subreddit"]
        post_title = post["title"]
        sentiment_results = sentiment_analysis(post["title"])
        timestamp = post["timestamp"]
        sentiment_dict = {}
        dump_sentiment_results(post_subreddit, post_title, sentiment_results, timestamp, dump_data)
        
        for sentiment_result in sentiment_results[0]:
            sentiment_dict[sentiment_result['label']] = sentiment_result['score']
        
        database.insert_post(post_title, post_subreddit, sentiment_results[0][0]['label'], sentiment_dict.get('positive', 0), sentiment_dict.get('neutral', 0), sentiment_dict.get('negative', 0), timestamp)
