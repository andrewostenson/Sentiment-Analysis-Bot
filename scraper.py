import pandas as pd
import praw
import requests
import bs4
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="YOUR_USER_AGENT"
)

def scrape_data(url):
    response = requests.get(url, verify=False) # Disable SSL verification, get the response from the URL
    soup = bs4.BeautifulSoup(response.text, 'html.parser') # Parse the HTML content using BeautifulSoup
    print(soup.find_all(class_="text"))  # Example: Print all elements with the class "text"

if __name__ == "__main__":
    scrape_data('https://quotes.toscrape.com')  # Example URL, replace with the actual URL you want to scrape
    print(reddit.read_only)

