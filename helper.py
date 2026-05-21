
import emoji
from collections import Counter
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from urlextract import URLExtract
import re
import pandas as pd

nltk.download('stopwords')
stopwords_list = set(stopwords.words('english'))

data = pd.read_csv('./data/processed/data.csv')


def fetch_stats(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    num_messages = data.shape[0]
    words = data['message'].dropna().astype(str).str.replace('\n', '').str.split().sum()
    media_messages = data[data['message'] == '<Media omitted>\n'].shape[0]
    links = []
    extract = URLExtract()
    for link in data['message']:
        links.extend(extract.find_urls(link))
    return num_messages, len(words), media_messages, len(links)


def most_busy_users(data):
    x = data['user'].value_counts().head()
    df = round((data['user'].value_counts() / data.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df




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


    wc = WordCloud(width=1000, height=750, min_font_size=20, random_state=21,
                    max_font_size=100).generate(temp['message'].str.cat(sep=' '))
    return wc

def most_common_words(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
        
    temp = data[data['user'] != 'user-notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    temp['message'] = temp['message'].apply(hindi_stopwords)
    temp['message'] = temp['message'].apply(english_stopwords)
    temp['message'] = temp['message'].apply(remove_punctuation)
    

    words = []
    for msg in temp['message']:
        words.extend(msg.split())


    common_words = pd.DataFrame(Counter(words).most_common(10))

    return common_words


def emoji_helper(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
        
    temp = data[data['user'] != 'user-notification']
    temp = temp[temp['message'] != '<Media omitted>\n']


    emoji_list = []

    for msg in temp['message']:
        emoji_list.extend([c for c in msg if c in emoji.EMOJI_DATA])

    common_emoji = pd.DataFrame(
        Counter(emoji_list).most_common(len(Counter(emoji_list))))
    
    return common_emoji


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

    return data.groupby('date')['message'].count().reset_index()


def day_based_activity(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    return data['day_name'].value_counts().plot.bar(color='purple')

    


def month_based_activity(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    return data['month_name'].value_counts()
    
    
def activity_heatmap(selected_user, data):  
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]       
    return data.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)  
