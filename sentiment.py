from transformers import pipeline
import json

# Load sample posts from a JSON file
with open("data/sample_posts.json", "r") as f:
    sample_posts = json.load(f)

def sentiment():
    # Load the sentiment analysis pipeline using the specified model
    sentiment_analysis = pipeline(task="sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
    return sentiment_analysis

if __name__ == "__main__":
    # Grab the sentiment analysis pipeline
    sentiment_analysis = sentiment()

    for post in sample_posts:
        # Perform sentiment analysis on the post's title and comments print the results
        result_title = sentiment_analysis(post["title"])
        
        print(f"Post Title: {post['title']}")
        print(f"Sentiment Analysis Result: {result_title}\n")
        
        # Loop through all comments and perform sentiment analysis on each comment, print the results
        for comment in post["comments"]:
            result_comments = sentiment_analysis(comment)
            print(f"Comment: {comment}")
            print(f"Sentiment Analysis Result: {result_comments}\n")

