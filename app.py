import streamlit as st
import database
import main
import datetime
import time

database.create_table()

# Variable initialization
today = datetime.date.today()
year_ago = today - datetime.timedelta(days=365)

st.title("Job Market Sentiment Analysis and Health")

cols = st.columns(3)

with cols[0]:
    if st.button("Run Scraper and Sentiment Analysis"):
        # Run the scraper and sentiment analysis
        start = time.perf_counter()
        main.run()
        end = time.perf_counter()
        st.toast(f"Scraping and sentiment analysis completed in {end - start:.2f} seconds")

with cols[1]:
    # Clear all posts if the clear data button is clicked
    if st.button("Clear Data"):
        database.delete_all_posts()

with cols[2]:
     view = st.toggle("Advanced View")

selected_sentiment = st.selectbox("Select a sentiment to filter by:", options=["All", "positive", "neutral", "negative"])

date_range = st.date_input(
    "Select a date range to filter the data:",
    (year_ago, today),
    format="MM.DD.YYYY",
)

keyword_search = st.text_input("Search by title or source:")



filtered_data = database.fetch_filtered_posts(
    start_date=date_range[0],
    end_date=date_range[1],
    sentiment_filter=selected_sentiment if selected_sentiment != "All" else None,
    keyword_filter=keyword_search if keyword_search else None
)

# Fetch data from the database and convert it to a DataFrame, then create a copy of the DataFrame for display purposes
chart_data = filtered_data.copy()
table_data = chart_data.copy()

# Filter the DataFrame based on the selected sentiment
if selected_sentiment != "All":
    chart_data = chart_data[chart_data['sentiment'] == selected_sentiment]

if not view:
     table_data = table_data.drop(columns=['id', 'confidence_pos', 'confidence_neu', 'confidence_neg', 'timestamp'])
    

# Display the DataFrame in the Streamlit app
st.dataframe(table_data)

# Group the data by timestamp and calculate the mean of the confidence scores for each sentiment category
chart_data = chart_data.groupby('timestamp')[['confidence_pos', 'confidence_neu', 'confidence_neg']].mean().reset_index() # Reset the index to make 'timestamp' a column again


# Create a mapping of sentiment labels to their corresponding confidence score columns
chart_data_dict = {
    "positive": 'confidence_pos',
    "neutral": 'confidence_neu',
    "negative": 'confidence_neg'
}

if selected_sentiment == 'All':
        st.line_chart(chart_data[
             ['confidence_pos', 
              'confidence_neu', 
              'confidence_neg', 
              'timestamp']
              ], x = "timestamp", width = 0, use_container_width=True)

else:
    st.line_chart(chart_data[[chart_data_dict.get(selected_sentiment), 'timestamp']], x = "timestamp", width = 0, use_container_width = True)
