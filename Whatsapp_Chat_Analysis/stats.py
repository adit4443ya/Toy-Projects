from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['Sender'].value_counts().head()
    df = round((df['Sender'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'Sender': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]


    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df['Cleaned MSG'] = df['Cleaned MSG'].apply(remove_stop_words)
    df_wc = wc.generate(df['Cleaned MSG'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    temp = df[df['Sender'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend(emoji.distinct_emoji_list(message))
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.rename(columns={'0':'Emojis','1':'Counts'})
    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'months']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['months'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    daily_timeline = df.groupby('Date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    return df['days'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    return df['months'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    user_heatmap = df.pivot_table(index='days', columns='period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap
