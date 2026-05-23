import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocess as process
import helper as helper
import streamlit as st
import pandas as pd
import nltk

# data = process.preprocess(open('./data/raw/WhatsApp Chat with Competitive Programmers.txt', encoding='utf-8').read())

st.sidebar.title("WhatsApp Chat Analysis")

sns.set_theme(style='darkgrid', palette='muted', font='sans-serif', rc={'figure.figsize': (10, 6)})

uploaded_file = st.sidebar.file_uploader('choose a file')

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode('utf-8')

    data = process.preprocess(data)

    user_list = data['user'].unique().tolist()
    user_list.remove('user-notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis data ", user_list)

    if (st.sidebar.button('Show Analysis')):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(
            selected_user, data)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header(':blue[Total Message]')
            st.title(num_messages)
        with col2:
            st.header(':blue[Total Words] ')
            st.title(words)
        with col3:
            st.header(':blue[Media shared]')
            st.title(num_media_messages)
        with col4:
            st.header(':blue[Links shared]  ')
            st.title(num_links)

        # Monthly timeline

        st.title(':blue[Monthly Timeline]')
        timeline = helper.monthly_timeline(selected_user, data)
        fig, ax = plt.subplots(1, figsize=(18, 9))
        ax.plot(timeline['monthly_timeline'], timeline['message'],
                alpha=0.8,  linestyle='-.', marker='*')

        ax.set_xticklabels(ax.get_xticklabels(), rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        # Daily timeline

        st.title(':blue[Daily Timeline]')
        timeline = helper.daily_timeline(selected_user, data)
        fig, ax = plt.subplots(1, figsize=(18, 9))
        ax.plot(timeline['date'], timeline['message'],
                alpha=0.8,  linestyle='-')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=15)
        plt.tight_layout()
        st.pyplot(fig)

        # Day-based Activity Map

        st.title(':blue[Day-based Activity Map]')
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Busy day ")
            fig, ax = plt.subplots(1, figsize=(12, 8))
            busy_day = helper.day_based_activity(selected_user, data)
            ax.bar(busy_day.index, busy_day.to_numpy())
            plt.xticks(rotation=45, fontsize=15)
            st.pyplot(fig)

        with col2:
            st.subheader("Busy month")
            fig, ax = plt.subplots(1, figsize=(12, 8))
            busy_month = helper.month_based_activity(selected_user, data)
            ax.bar(busy_month.index, busy_month.to_numpy())
            plt.xticks(rotation=45, fontsize=15)
            st.pyplot(fig)

        # activity_heatmap
        st.title(":blue[Weekly Activity Map]")
        fig, ax = plt.subplots(1, figsize=(22, 8))
        activity_heatmap = helper.activity_heatmap(selected_user, data)
        ax = sns.heatmap(activity_heatmap)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=15)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=45, fontsize=15)

        plt.tight_layout()
        st.pyplot(fig)

        # Most busy_users

        if selected_user == 'Overall':
            st.title(":blue[Most busy users]")
            most_busy, stats = helper.most_busy_users(data)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Most busy User")
                ax = plt.bar(most_busy.index,
                             most_busy.to_numpy(), color='green')
                plt.xticks(rotation=360, fontsize=15)
                plt.yticks(fontsize=15)
                st.pyplot(fig)

            with col2:
                st.subheader("User's stats")
                # fig, ax = plt.subplots(figsize=(12, 8))
                # stats.head()
                # ax = plt.bar(stats.index , stats.user, color='blue')
                # plt.xticks(rotation=90)
                # plt.tight_layout()
                st.dataframe(stats)

        # Word Cloud

        st.title(":blue[Word Cloud]")
        fig, ax = plt.subplots(figsize=(4, 16))
        wc = helper.wordcloud(selected_user, data)
        ax.set_axis_off()
        ax.imshow(wc)
        st.pyplot(fig)

       
        st.title(":blue[Most Common Words]")
        fig, ax = plt.subplots(figsize=(16, 10))
        most_common_words = helper.most_common_words(selected_user, data)
        sns.barplot(data=most_common_words, x='common_words',
                    y='count', palette='viridis', ax=ax)
        plt.xticks(rotation=45, fontsize=15)
        plt.yticks(fontsize=15)
        plt.tight_layout()
        st.pyplot(fig)

        # emoji_helper

        st.title(":blue[Emoji Analysis]")
        fig, ax = plt.subplots(figsize=(12, 8))
        emoji_helper = helper.emoji_helper(selected_user, data)
        col1, col2 = st.columns(2)

        if emoji_helper.shape[0] > 0:
            with col1:
                st.dataframe(emoji_helper.head(10))
            with col2:
                ax.pie(emoji_helper['count'].head(10), labels=emoji_helper['emoji'].head(10), autopct="%0.2f%%")
                st.pyplot(fig)

        else:
            st.write(":red[No Emojis Send by this user]")
