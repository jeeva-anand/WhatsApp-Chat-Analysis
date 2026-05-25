import re
import nltk
import emoji
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
from nltk.corpus import stopwords
from urlextract import URLExtract



try:
    stopwords_list = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    

stopwords_list = set(stopwords.words('english'))

def fetch_stats(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    num_messages = data.shape[0]
    words = []
    for message in data['message']:
        words.extend(message.split())
    media_messages = data[data['message'] == '<Media omitted>\n'].shape[0]
    links = []
    extract = URLExtract()
    for link in data['message']:
        links.extend(extract.find_urls(link))
        
    return num_messages, len(words), media_messages, len(links)


def most_busy_users(data):
    x = data['user'].value_counts().head()
    df = round((data['user'].value_counts() / data.shape[0]) * 100, 2).reset_index()
    print(df.head())
    return x, df.head()


def hindi_stopwords(message):
    with open('./data/processed/hindi_stopwords.txt', 'r') as file:
        stop_words = file.read()
    filtered_message = []
    for word in message.lower().split():
        if word not in stop_words:
            filtered_message.append(word)
    return " ".join(filtered_message)


def english_stopwords(message):
    filtered_message = []
    for word in message.lower().split():
        if word not in stopwords_list:
            filtered_message.append(word)
    return " ".join(filtered_message)


def remove_stopwords(message):
    filtered_message = english_stopwords(message)
    return  hindi_stopwords(filtered_message)

def remove_punctuation(message):
    return re.sub(r'[^\w\s]', '', message)


def wordcloud(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
        
    temp = data[data['user'] != 'user-notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp['message'] = temp['message'].apply(hindi_stopwords)
    temp['message'] = temp['message'].apply(english_stopwords)
    temp['message'] = temp['message'].apply(remove_punctuation)
    wc = WordCloud(width=1400, height=700, min_font_size=20, random_state=21,
                    max_font_size=100).generate(temp['message'].str.cat(sep=' '))
    return wc

def most_common_words(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    words = []
    temp = data[data['user'] != 'user-notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp['message'] = temp['message'].apply(hindi_stopwords)
    temp['message'] = temp['message'].apply(english_stopwords)
    temp['message'] = temp['message'].apply(remove_punctuation)     
    for msg in temp['message']:
        words.extend(msg.split())
    common_words = pd.DataFrame(Counter(words).most_common(10))
    common_words.rename(columns={0: 'common_words', 1: 'count'}, inplace=True)
    return common_words




def monthly_timeline(selected_user, data):    
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]        
    timeline = data.groupby(['month', 'month_name', 'year'])[
        'message'].count().reset_index()
    month_timeline = []
    for i in range(timeline.shape[0]):
        month_timeline.append(timeline['month_name']
                            [i] + ' - ' + str(timeline['year'][i]))
    timeline['monthly_timeline'] = month_timeline    
    return timeline


def daily_timeline(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    daily =  data.groupby('date')['message'].count().reset_index()
    return daily
    
def day_based_activity(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    return data['day_name'].value_counts()

def month_based_activity(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    return data['month_name'].value_counts()
        
        
def activity_heatmap(selected_user, data):  
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]       
    map =  data.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return map


def emoji_helper(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    temp = data[data['user'] != 'user-notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    emoji_list = []
    for msg in data['message']:
        emoji_list.extend([c for c in msg if c in emoji.EMOJI_DATA])
    common_emoji = pd.DataFrame(
        Counter(emoji_list).most_common(len(Counter(emoji_list))))
    common_emoji.rename(columns={0: 'emoji', 1: 'count'}, inplace=True)
    print(common_emoji.head())
    return common_emoji


