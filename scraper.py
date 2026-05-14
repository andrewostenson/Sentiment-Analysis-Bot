from datetime import datetime
import requests

keywords = ['hiring', 'job', 'career', 'position', 'opportunity', 'vacancy', 'recruiting', 'recruitment', 'employment', 
                'remote', 'onsite', 'full-time', 'part-time', 'contract', 'internship', 'freelance', 'freelancer', 'consultant', 
                'consulting', 'agency', 'headhunter', 'headhunting', 'talent acquisition', 'talent management', 'talent sourcing', 
                'talent scouting', 'layoff', 'firing', 'termination', 'resignation', 'quitting', 'job loss', 'unemployment', 'job market', 
                'job search', 'job hunting', 'career development', 'career growth', 'career advancement', 'career change',
                'Google', 'Microsoft', 'Amazon', 'Facebook', 'Meta', 'Apple', 'Netflix', 'Tesla', 'NVIDIA', 'IBM', 'Intel', 'Salesforce',
                'Oracle', 'SAP', 'Adobe', 'Twitter', 'LinkedIn', 'Uber', 'Airbnb', 'Spotify', 'Dropbox', 'Slack', 'Zoom',
                'GitHub', 'GitLab', 'Atlassian', 'Stripe', 'Square', 'PayPal', 'Shopify', 'Twilio', 'Cloudflare', 'Reddit',
                'AI', 'Artificial Intelligence', 'Machine Learning', 'Deep Learning', 'Data Science', 'Big Data', 'Analytics',
                'Cloud Computing', 'DevOps', 'Cybersecurity', 'Blockchain', 'Cryptocurrency', 'Fintech', 'Healthtech', 'Edtech',
                'SaaS', 'PaaS', 'IaaS', 'Open Source', 'Programming', 'Software Development', 'Web Development', 'Mobile Development', 'Game Development',
                'Python', 'JavaScript', 'Java', 'C#', 'C++', 'Go', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'TypeScript',
                'React', 'Angular', 'Vue', 'Django', 'Flask', 'Spring', 'Node.js', 'Express', 'GraphQL', 'REST API', 'Microservices',
                'Docker', 'Kubernetes', 'AWS', 'Azure', 'Google Cloud', 'Heroku', 'DigitalOcean', 'Vercel', 'Netlify', 'Firebase', 'Serverless',
                'Agile', 'Scrum', 'Kanban', 'Project Management', 'Product Management', 'UX/UI Design', 'Design Thinking', 'User Experience', 'User Interface',
                'Remote Work', 'Work From Home', 'WFH', 'Distributed Teams', 'Virtual Teams', 'Remote Jobs', 'Remote Opportunities', 'Remote Careers', 'Remote Positions', 'Remote Hiring',
                'Diversity', 'Inclusion', 'Equity', 'DEI', 'LLM', 'Large Language Models', 'ChatGPT', 'GPT-3', 'GPT-4', 'AI Ethics', 'AI Bias', 'AI Regulation', 'AI Governance']
    

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

#Scraper functions for Lobsters
def scrape_top_stories_Lobsters():
    response = requests.get('https://lobste.rs/newest.json')
    data = response.json()
    return data

def filter_relevant_stories_Lobsters(story):
    title = story.get('title', '')
    return any(keyword in title for keyword in keywords)