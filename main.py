import scraper as sc
import sentiment as sm
import database as db

def run():
    db.create_table()
    top_stories_HN = sc.scrape_top_stories_HN()
    top_stories_DEV = sc.scrape_top_stories_DEV()
    top_stories_Lobsters = sc.scrape_top_stories_Lobsters()
    hn_counter = 0
    dev_counter = 0
    lobster_counter = 0

    # Process Hacker News stories
    for id in top_stories_HN:
        story = sc.get_story_HN(id)

        if sc.filter_relevant_stories_HN(story):
            filtered_HN = sc.filter_story_HN(story)
            story_sentiment = sm.run_sentiment(filtered_HN["title"])
            sentiment_dict = {}

            for result in story_sentiment[0]:
                sentiment_dict[result['label']] = result['score']

            db.insert_post(
                filtered_HN["title"], 
                filtered_HN["source"], 
                story_sentiment[0][0]['label'], 
                sentiment_dict.get('positive', 0), sentiment_dict.get('neutral', 0), sentiment_dict.get('negative', 0), 
                filtered_HN["time"])
            
    # Process DEV stories
    for story in top_stories_DEV:
        story["source"] = 'DEV'
        story_sentiment = sm.run_sentiment(story["title"])
        sentiment_dict = {}

        for result in story_sentiment[0]:
            sentiment_dict[result['label']] = result['score']

        db.insert_post(
            story["title"], 
            story["source"], 
            story_sentiment[0][0]['label'], 
            sentiment_dict.get('positive', 0), sentiment_dict.get('neutral', 0), sentiment_dict.get('negative', 0), 
            story["published_at"])
    
    # Process Lobsters stories
    for story_lobster in top_stories_Lobsters:
        story_lobster["source"] = 'Lobsters'

        if sc.filter_relevant_stories_Lobsters(story_lobster):
            story_sentiment = sm.run_sentiment(story_lobster["title"])
            sentiment_dict = {}

            for result in story_sentiment[0]:
                sentiment_dict[result['label']] = result['score']

            db.insert_post(
                story_lobster["title"], 
                story_lobster["source"], 
                story_sentiment[0][0]['label'], 
                sentiment_dict.get('positive', 0), sentiment_dict.get('neutral', 0), sentiment_dict.get('negative', 0), 
                story_lobster["created_at"])