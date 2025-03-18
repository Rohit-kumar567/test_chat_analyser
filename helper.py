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

def remove_stop_words(message):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    y = []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)

def remove_punctuation(message):
    x = re.sub('[%s]' % re.escape(string.punctuation), '', message)
    return x

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'].apply(remove_punctuation)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'].apply(remove_punctuation)
    words = []

    for message in temp['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    month_timeline = []
    for i in range(timeline.shape[0]):
        month_timeline.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = month_timeline
    return timeline

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
