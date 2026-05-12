from datetime import datetime
import requests

keywords = ['hiring', 'job', 'career', 'position', 'opportunity', 'vacancy', 'recruiting', 'recruitment', 'employment', 
                'remote', 'onsite', 'full-time', 'part-time', 'contract', 'internship', 'freelance', 'freelancer', 'consultant', 
                'consulting', 'agency', 'headhunter', 'headhunting', 'talent acquisition', 'talent management', 'talent sourcing', 
                'talent scouting', 'layoff', 'firing', 'termination', 'resignation', 'quitting', 'job loss', 'unemployment', 'job market', 
                'job search', 'job hunting', 'career development', 'career growth', 'career advancement', 'career change',
                'Google', 'Microsoft', 'Amazon', 'Facebook', 'Meta', 'Apple', 'Netflix', 'Tesla', 'NVIDIA', 'IBM', 'Intel', 'Salesforce',
                'Oracle', 'SAP', 'Adobe', 'Twitter', 'LinkedIn', 'Uber', 'Airbnb', 'Spotify', 'Dropbox', 'Slack', 'Zoom',
                'GitHub', 'GitLab', 'Atlassian', 'Stripe', 'Square', 'PayPal', 'Shopify', 'Twilio', 'Cloudflare', 'Reddit',]
    

# Scraper functions for Hacker News
def scrape_top_stories_HN():
    best_response = requests.get('https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty')
    top_response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    data = best_response.json() + top_response.json()
    return data

def get_story_HN(id):
    response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty')
    data = response.json()
    return data

def filter_relevant_stories_HN(story):
    title = story.get('title', '').lower()
    return any(keyword in title for keyword in keywords)


def filter_story_HN(story):
    mask = {"title", "time"}
    filtered_story = {k: story[k] for k in mask}
    filtered_story["time"] = datetime.fromtimestamp(filtered_story["time"])
    filtered_story["source"] = 'HackerNews'
    return filtered_story

# Scraper functions for DEV
def scrape_top_stories_DEV():
    response = requests.get('https://dev.to/api/articles?tag=keywords&per_page=100')
    data = response.json()
    return data