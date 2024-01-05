import streamlit as st
import preprocessor,stats
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.textPreProcessor(data)
    st.dataframe(df)
    # fetch unique users
    user_list = df['Sender'].unique().tolist()
    # user_list.remove('group_notification')
    # user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = stats.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = stats.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        # st.title("Daily Timeline")
        # daily_timeline = stats.daily_timeline(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.plot(daily_timeline['Date'], daily_timeline['Message'], color='black')
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)
        
        # hour timeline
        msg_count = df['hours'].value_counts().sort_index()
        # Plot the graph
        fig=plt.figure(figsize=(10, 8))
        msg_count.plot(kind='bar')
        st.title('Number of Messages Exchanged at Different Hours')
        plt.xlabel('Hour')
        plt.ylabel('Number of Messages')
        plt.xticks(rotation=45)  # Rotates x-axis labels for better visibility
        plt.show()
        # fig,ax = plt.subplots()
        st.pyplot(fig)

        # Count the total number of messages exchanged for each month
        msg_count_per_month = df['datet'].dt.to_period('M').value_counts().sort_index()

        # Count the number of messages exchanged for each sender and each month
        sender_msg_counts = df.groupby([df['datet'].dt.to_period('M'), 'Sender']).size().unstack(fill_value=0)

        # Plot the graph
        fig, ax = plt.subplots(figsize=(15, 6))
        bar_width = 0.3
        index = range(len(msg_count_per_month))

        bar1 = ax.bar(index,sender_msg_counts.iloc[:,1], bar_width, label=sender_msg_counts.columns[1])
        bar2 = ax.bar([i + bar_width for i in index], sender_msg_counts.iloc[:,0], bar_width, label=sender_msg_counts.columns[0])
        bar3 = ax.bar([i + 2*bar_width for i in index], msg_count_per_month, bar_width, label='Total')
        if selected_user=='Overall':
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of Messages')
            ax.set_title('Number of Messages Exchanged in Different Months')
            ax.set_xticks([i + bar_width for i in index])
            ax.set_xticklabels([month.strftime('%b, %y') for month in msg_count_per_month.index], rotation=45)
            ax.legend()
            plt.show()
            st.title('Number of Messages Exchanged in Different Months')
            # fig,ax = plt.subplots()
            st.pyplot(fig)
            
            # activity map
            st.title('Activity Map')
            col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = stats.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = stats.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = stats.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = stats.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = stats.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = stats.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = stats.emoji_stats(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            # fig,ax = plt.subplots()
            # sns.set_theme()  # Set Seaborn theme
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)




