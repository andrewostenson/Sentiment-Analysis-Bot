import scraper as sc
import sentiment as sm
import database as db

def run():
    db.create_table()
    top_stories = sc.scrape_top_stories_HN()
    
    for id in top_stories:
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