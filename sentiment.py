from transformers import pipeline
import json

# Load sample posts from a JSON file
with open("data/sample_posts.json", "r") as f:
    sample_posts = json.load(f)


def sentiment():
    # Load the sentiment analysis pipeline using the specified model
    sentiment_analysis = pipeline(task="sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
    return sentiment_analysis

def dump_sentiment_results(post_subreddit, post_title, sentiment_results, dump_data):
    # Create a dictionary to store the subreddit, title, and sentiment results for the post
    post_dump = {"subreddit": post_subreddit,"title": post_title, "sentiment": sentiment_results}
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
        dump_sentiment_results(post_subreddit, post_title, sentiment_results, dump_data)
