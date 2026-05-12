import scraper as sc
import sentiment as sm
import database as db

def run():
    db.create_table()
    top_stories_HN = sc.scrape_top_stories_HN()
    top_stories_DEV = sc.scrape_top_stories_DEV()

    # Process Hacker News stories
    for id in top_stories_HN:
        story = sc.get_story_HN(id)
        if sc.filter_relevant_stories_HN(story):
            filtered_story = sc.filter_story_HN(story)
            story_sentiment = sm.run_sentiment(filtered_story["title"])
            sentiment_dict = {}

            for result in story_sentiment[0]:
                sentiment_dict[result['label']] = result['score']

            db.insert_post(
                filtered_story["title"], 
                filtered_story["source"], 
                story_sentiment[0][0]['label'], 
                sentiment_dict.get('positive', 0), sentiment_dict.get('neutral', 0), sentiment_dict.get('negative', 0), 
                filtered_story["time"])
            
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
        