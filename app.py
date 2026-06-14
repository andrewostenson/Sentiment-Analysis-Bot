import streamlit as st
import database
import datetime
import analytics as an

database.create_table()


# Variable initialization
today = datetime.date.today()
today_week_start = today - datetime.timedelta(days=7)
last_week_start = today - datetime.timedelta(days=14)
year_ago = today - datetime.timedelta(days=365)

st.title("Job Market Sentiment Analysis and Health")

this_week_sentiment = an.average_sentiment(start_date=today_week_start, end_date=today)
last_week_sentiment = an.average_sentiment(start_date=last_week_start, end_date=today_week_start)

if this_week_sentiment is not None and last_week_sentiment is not None:
    col1, col2, col3 = st.columns(3)

    sentiment_change = this_week_sentiment - last_week_sentiment
    percent_change = (sentiment_change / abs(last_week_sentiment)) * 100 if last_week_sentiment != 0 else 0

    with col1:
        st.metric(label="Last Week's Average Sentiment", value=f"{last_week_sentiment:.4f}")
    with col2:
        st.metric(label="This Week's Average Sentiment", value=f"{this_week_sentiment:.4f}")
    with col3:
        st.metric(label="Sentiment Change (%)", value=f"{percent_change:.2f}%")
else:
    st.write("Not enough data to calculate sentiment change from last week.")

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
    sentiment_filter= None,
    keyword_filter=keyword_search if keyword_search else None
)

view = st.toggle("Advanced View")

# Fetch data from the database and convert it to a DataFrame, then create a copy of the DataFrame for display purposes
chart_data = filtered_data.copy()
table_data = chart_data.copy()


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
