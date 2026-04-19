from datetime import datetime
import requests

def scrape_top_stories_HN():
    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    data = response.json()
    return data

def get_story_HN(id):
    response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty')
    data = response.json()
    return data

def filter_story_HN(story):
    mask = {"title", "time"}
    filtered_story = {k: story[k] for k in mask}
    filtered_story["time"] = datetime.fromtimestamp(filtered_story["time"])
    filtered_story["source"] = 'HackerNews'
    return filtered_story