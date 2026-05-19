from datetime import datetime
import requests

keywords = [
    # Job market general
    'hiring', 'layoff', 'laid off', 'job market', 'job search', 'job hunting',
    'unemployment', 'employment', 'fired', 'terminated', 'downsizing', 'restructuring',
    'hiring freeze', 'headcount', 'workforce',
    
    # Roles and career
    'software engineer', 'software developer', 'developer', 'engineer', 'programmer',
    'swe', 'sde', 'devops', 'fullstack', 'backend', 'frontend', 'data scientist',
    'ml engineer', 'career', 'internship', 'new grad', 'entry level', 'senior engineer',
    
    # Job seeking
    'offer', 'rejected', 'interview', 'technical interview', 'leetcode', 'resume',
    'recruiter', 'recruiting', 'job offer', 'compensation', 'salary', 'tc', 'total comp',
    
    # Industry trends
    'tech industry', 'big tech', 'faang', 'startup', 'remote work', 'return to office',
    'rto', 'ai replacing', 'automation', 'outsourcing', 'h1b', 'visa',
    
    # Sentiment indicators
    'burned out', 'burnout', 'overworked', 'underpaid', 'toxic', 'culture',
    'work life balance', 'mental health', 'quit', 'resignation', 'great resignation'
]
    

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
    response = requests.get('https://dev.to/api/articles?tag=career&per_page=100')
    for article in response.json():
        article['title'] = article['title'].lower()
    data = response.json()
    return data

#Scraper functions for Lobsters
def scrape_top_stories_Lobsters():
    response = requests.get('https://lobste.rs/hottest.json')
    data = response.json()
    return data

def filter_relevant_stories_Lobsters(story):
    title = story.get('title', '').lower()
    return any(keyword in title for keyword in keywords)