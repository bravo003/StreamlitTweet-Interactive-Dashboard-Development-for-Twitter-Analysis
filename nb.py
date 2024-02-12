import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Give the Title
st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")
st.markdown(" This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown(" This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")


@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv("Tweets.csv")
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

# sets up a sidebar in a web app where users can select a sentiment ('positive', 'neutral', or 'negative') using a radio button
st.sidebar.subheader("Show random tweets")
random_tweet = st.sidebar.radio('Sentiment', ('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

# bar chart and pie chart
st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie Chart'], key = '1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown('### Number of tweets by sentiment')
    if select == "Histogram":
        fig = px.bar(sentiment_count, x = "Sentiment", y = "Tweets", color = "Tweets", height = 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values = 'Tweets', names = 'Sentiment')
        st.plotly_chart(fig)


st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect('Pick Airline', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key = '0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc = 'count', color = 'airline_sentiment', facet_col ='airline_sentiment', labels = {'airline_sentiment':'tweets'}, height = 600, width = 800)
    st.plotly_chart(fig_choice)

# Display sentiment analysis statistics
st.subheader("Sentiment Analysis Statistics")
st.write("Total Tweets:", len(data))
st.write("Positive Tweets:", len(
    data[data['airline_sentiment'] == 'positive']))
st.write("Neutral Tweets:", len(data[data['airline_sentiment'] == 'neutral']))
st.write("Negative Tweets:", len(
    data[data['airline_sentiment'] == 'negative']))


# Word Cloud
st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
st.set_option('deprecation.showPyplotGlobalUse', False)

if not st.sidebar.checkbox("Close", True, key='3'):
        st.header('Word cloud for %s sentiment' % (word_sentiment))
        df = data[data['airline_sentiment'] == word_sentiment]
        words = ' '.join(df['text'])
        processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
        wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white', height = 640, width = 800).generate(processed_words)
        plt.imshow(wordcloud)
        plt.xticks([])
        plt.yticks([])
        st.pyplot()