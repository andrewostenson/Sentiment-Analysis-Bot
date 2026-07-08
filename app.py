import streamlit as st
import database
import datetime
import analytics as an
import pandas as pd

database.create_table()


# Variable initialization
today = datetime.date.today()
today_week_start = today - datetime.timedelta(days=7)
last_week_start = today - datetime.timedelta(days=14)

week_ago = today - datetime.timedelta(days=7)
month_ago = today - datetime.timedelta(days=30)
year_ago = today - datetime.timedelta(days=365)

this_week_sentiment = an.average_sentiment(start_date=today_week_start, end_date=today)
last_week_sentiment = an.average_sentiment(start_date=last_week_start, end_date=today_week_start)

highest_positive_stories = an.highest_scored_stories(start_date=week_ago, end_date=today, sentiment_type="positive")
highest_negative_stories = an.highest_scored_stories(start_date=week_ago, end_date=today, sentiment_type="negative")

date_range_dict = {
    "Last 7 days": (week_ago, today),
    "Last 30 days": (month_ago, today),
    "Last 365 days": (year_ago, today)
}

chart_data_dict = {
    "positive": 'confidence_pos',
    "neutral": 'confidence_neu',
    "negative": 'confidence_neg'
}

# Display Streamlit app
st.title("Job Market Sentiment Analysis")

st.subheader("Weekly Sentiment Overview")

if this_week_sentiment is not None and last_week_sentiment is not None:
    col1, col2, col3, col4 = st.columns(4)

    sentiment_change = this_week_sentiment - last_week_sentiment
    percent_change = (sentiment_change / abs(last_week_sentiment)) * 100 if last_week_sentiment != 0 else 0

    with col1:
        st.metric(label="Last Week's Average Sentiment", value=f"{last_week_sentiment:.4f}")
    with col2:
        st.metric(label="This Week's Average Sentiment", value=f"{this_week_sentiment:.4f}")
    with col3:
        st.metric(label="Sentiment Change (%)", value=f"{percent_change:.2f}%")
    with col4:
        st.metric(label="Market Health", value="Improving" if sentiment_change > 0.02 else "Declining" if sentiment_change < -0.02 else "Stable")
else:
    st.write("Not enough data to calculate sentiment change from last week.")


st.subheader("Top Positive Stories This Week")

if highest_positive_stories is not None and not highest_positive_stories.empty:
    st.dataframe(highest_positive_stories[['title', 'source', 'confidence_pos']])
else:
    st.write("No positive stories found in the last week.")

st.subheader("Top Negative Stories This Week")

if highest_negative_stories is not None and not highest_negative_stories.empty:
    st.dataframe(highest_negative_stories[['title', 'source', 'confidence_neg']])
else:
    st.write("No negative stories found in the last week.")

st.subheader("Filter and Explore Data")

selected_sentiment = st.selectbox("Select a sentiment to filter by:", options=["All", "positive", "neutral", "negative"])

date_range = st.selectbox("Select a date range:", options=["Last 7 days", "Last 30 days", "Last 365 days"], index=0)

keyword_search = st.text_input("Search by title or source:")

filtered_data = database.fetch_filtered_posts(
    start_date=date_range_dict[date_range][0],
    end_date=date_range_dict[date_range][1],
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
chart_data['timestamp'] = pd.to_datetime(chart_data['timestamp']).dt.date
chart_data = chart_data.groupby('timestamp')[['confidence_pos', 'confidence_neu', 'confidence_neg']].mean().reset_index() # Reset the index to make 'timestamp' a column again


if selected_sentiment == 'All':
        st.line_chart(chart_data[
             ['confidence_pos', 
              'confidence_neu', 
              'confidence_neg', 
              'timestamp']
              ], x = "timestamp", width = 0, use_container_width=True)

else:
    st.line_chart(chart_data[[chart_data_dict.get(selected_sentiment), 'timestamp']], x = "timestamp", width = 0, use_container_width = True)
