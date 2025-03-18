from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import re
import emoji
from textblob import TextBlob
from textstat import flesch_reading_ease
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import timedelta

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df

def monthly_timeline(selected_user, df):
    if not all(col in df.columns for col in ['year', 'month_num', 'month']):
        return pd.DataFrame()  # Prevent KeyError if columns are missing

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    month_timeline = [f"{row['month']}-{row['year']}" for _, row in timeline.iterrows()]
    timeline['time'] = month_timeline

    return timeline

def daily_timeline(selected_user, df):
    if 'only_date' not in df.columns:
        return pd.DataFrame()  # Prevent error if 'only_date' is missing

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def deleted_message_analysis(df):
    return df[df['message'].str.contains('This message was deleted')].shape[0]

def media_content_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df[df['message'] == '<Media omitted>\n'].groupby('only_date').size()

def top_shared_links(selected_user, df):
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return pd.Series(links).value_counts().head(10)

def calculate_response_time(df):
    df['response_time'] = df['date'].diff().fillna(timedelta(seconds=0)).dt.total_seconds()
    return df['response_time'].describe()

def analyze_message_length(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['message_length'] = df['message'].apply(len)
    return df['message_length'].describe()

def extract_keywords(messages, top_n=10):
    vectorizer = TfidfVectorizer(max_features=top_n)
    X = vectorizer.fit_transform(messages)
    return vectorizer.get_feature_names_out()
