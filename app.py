import streamlit as st
import database

st.title("Streamlit App for Sentiment Analysis")

# Create a dropdown to select a subreddit for filtering the displayed data
selected_subreddit = st.selectbox("Select a subreddit to filter by:", options=["All","cscareerquestions", "learnprogramming", "csjobs", 
    "programming", "technology", "csprojects", "csmajors", "softwareengineering"])

selected_sentiment = st.selectbox("Select a sentiment to filter by:", options=["All", "positive", "neutral", "negative"])

# Fetch data from the database and convert it to a DataFrame
data = database.db_to_dataframe()

# Filter the DataFrame based on the selected subreddit
if selected_subreddit != "All":
    data = data[data['subreddit'] == selected_subreddit]

# Filter the DataFrame based on the selected sentiment
if selected_sentiment != "All":
    data = data[data['sentiment'] == selected_sentiment]

# Display the DataFrame in the Streamlit app
st.dataframe(data)

# Group the data by timestamp and calculate the mean of the confidence scores for each sentiment category
data = data.groupby('timestamp')[['confidence_pos', 'confidence_neu', 'confidence_neg']].mean().reset_index() # Reset the index to make 'timestamp' a column again

# Create a mapping of sentiment labels to their corresponding confidence score columns
data_dict = {
    "positive": 'confidence_pos',
    "neutral": 'confidence_neu',
    "negative": 'confidence_neg'
}

st.line_chart(data[[data_dict.get(selected_sentiment), 'timestamp']], x="timestamp", width=0, use_container_width=True)
