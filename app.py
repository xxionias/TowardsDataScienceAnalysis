import streamlit as st
import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib
from matplotlib.figure import Figure
from PIL import Image

sns.set_style('darkgrid')


st.title(':gem:TowardsDataScience Data Analysis:gem:')
st.subheader("by [Xinyi Bian:sparkles:](https://github.com/xxionias)")

image = Image.open('images/tds.png')

st.image(image, caption='As a Data Science lover, TowardsDataScience is one of my fav hubs')

# Initialize connection
# Uses st.cache to only run once
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

st.markdown("Hey there!:wave: Welcome to Xinyi's TowardsDataScience Data Analysis App. This app connectes to a Postgres database that contains data [web scraped](https://github.com/xxionias/webscraping/tree/master/mediumstories) from [TowardsDataScience](https:towardsdatascience.com) and analyzes data about your interests from published articles, including the distribution of the recommendations and responses of the articles and lengths of aricles. After some nice graphs, it tries to recommend an author that contributes the most to the topic that you are interested in. Give it a go!")
st.markdown(
        "**:leaves:To begin, please enter the key words of data science topics that you are interested in (or try sample inputs!).** :point_down:")

row2_spacer1, row2_1, row2_spacer2 = st.beta_columns((.1, 3.2, .1))
with row2_1:
    default_keyword = st.selectbox("Select one of sample keywords", (
        "Machine learning", "Statistics", "Random forest", "Clustering", "Neural Network"))
    st.markdown("**or**")
    user_input = st.text_input(
        "Input your own keywords")
    if not user_input:
        user_input = default_keyword

#conn.rollback()

# Perform query
# Uses st.cache to only rerun when the query changes or after 10 min
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

@st.cache
def get_article_data(user_input):
    sql = f"SELECT title, user_id, posting_time, length_in_min, recommendations, responses FROM articles WHERE title ILIKE '%{user_input}%' ORDER BY posting_time;"
    article = run_query(sql)
    return(article)

article_data = get_article_data(user_input)

# create DataFrame using data
df = pd.DataFrame.from_records(article_data, columns=['title', 'user_id', 'posting_time', 'length_in_min', 'recommendations', 'responses'])
df_with_userid = df['user_id']
df_without_userid = df.drop('user_id', axis=1)

line1_spacer1, line1_1, line1_spacer2 = st.beta_columns((.1, 3.2, .1))

with line1_1:
    if len(df) == 0:
        st.write(f"Looks like there's no such article containing keyword '{user_input}'. Try a different keyword.")
        st.stop()

st.header(f':running::running::running:Analyzing the Article that contains **{user_input}**:running::running::running:')

st.subheader(f':clap:{len(df)} Articles found!(Ordered by posting time from earliest to most recent)')
#st.dataframe(df)
#st.dataframe(df_with_userid)
st.dataframe(df_without_userid)


st.subheader(':star2:Length Distribution:star2:')
fig = Figure()
ax = fig.subplots()
sns.histplot(df_without_userid, x='length_in_min', color='goldenrod', ax=ax)
ax.set_xlabel('length_in_min')
ax.set_ylabel('Counts')
st.pyplot(fig)
    
st.markdown(":musical_note:Of all the **{}** aritcles, they require **{:.2f}** min to read on average.".format(
       len(df), df['length_in_min'].mean()))


st.subheader(':star2:Recommendations Distribution:star2:')
fig = Figure()
ax = fig.subplots()
sns.histplot(df_without_userid, x='recommendations', color='goldenrod', ax=ax)
ax.set_xlabel('Recommendations')
ax.set_ylabel('Counts')
st.pyplot(fig)
    
st.markdown(":musical_note:Of all the **{}** aritcles, they receive **{:.0f}** recommendations on average, and they most likely receive **{}** recommendations.".format(
       len(df), int(df['recommendations'].mean()), df['recommendations'].mode()[0]))

recommendations_df = df.sort_values(by=['recommendations'], ascending=False)
user_id_recommendations = str(recommendations_df['user_id'].iloc[0])

@st.cache
def get_author_data(user_id):
    sql = f"SELECT * FROM users WHERE user_id = {user_id};"
    user = run_query(sql)
    return(user)

user_info_recommendations = get_author_data(user_id_recommendations)

# create DataFrame using data
user_df_recommendations = pd.DataFrame.from_records(user_info_recommendations, columns=['user_id', 'user_name', 'description', 'followers'])
if user_df_recommendations['description'].iloc[0]:
    st.markdown(":musical_note:The article titled **{}** received the most recommendations :point_right: **{}**! The article is written by user **{}** who has **{}** followers! Here is the description about the author: **{}**".format(
       recommendations_df['title'].iloc[0], recommendations_df['recommendations'].iloc[0], user_df_recommendations['user_name'].iloc[0], user_df_recommendations['followers'].iloc[0], user_df_recommendations['description'].iloc[0]))
else:
    st.markdown(":musical_note:The article titled **{}** received the most recommendations :point_right: **{}**! The article is written by user **{}** who has **{}** followers!".format(
       recommendations_df['title'].iloc[0], recommendations_df['recommendations'].iloc[0], user_df_recommendations['user_name'].iloc[0], user_df_recommendations['followers'].iloc[0]))

responses_df = df.sort_values(by=['responses'], ascending=False)
if responses_df['responses'].iloc[0] == 0:
    st.markdown(":exclamation:Unfortunately none of these articles has responses.")
else:
    st.subheader(':star2:Responses Distribution:star2:')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(df_without_userid, x='responses', color='goldenrod', ax=ax)
    ax.set_xlabel('Responses')
    ax.set_ylabel('Counts')
    st.pyplot(fig)
    
    st.markdown(":musical_note:Of all the **{}** aritcles, they receive **{:.0f}** responses on average, and they most likely receive **{}** responses.".format(
       len(df), int(df['responses'].mean()), df['responses'].mode()[0]))
    user_id_responses = str(responses_df['user_id'].iloc[0])
    if user_id_recommendations == user_id_responses:
        st.markdown(":musical_note:The article **{}** also received the most responses :point_right: **{}**!".format(responses_df['title'].iloc[0], responses_df['responses'].iloc[0]))
    else:
        user_info_responses = get_author_data(user_id_responses)

        # create DataFrame using data
        user_df_responses = pd.DataFrame.from_records(user_info_responses, columns=['user_id', 'user_name', 'description', 'followers'])
        
        st.markdown(":musical_note:The article titled **{}** received the most responses :point_right: **{}**! The article is written by user **{}** who has **{}** followers! Here is the description about the author: **{}**".format(
        responses_df['title'].iloc[0], responses_df['responses'].iloc[0], user_df_responses['user_name'].iloc[0], user_df_responses['followers'].iloc[0], user_df_responses['description'].iloc[0]))


@st.cache
def get_most_published():
    sql = "SELECT user_name, counts FROM users u JOIN (SELECT user_id, COUNT(*) AS counts FROM articles GROUP BY user_id ORDER BY counts DESC LIMIT 1) AS a ON u.user_id = a.user_id;"
    user = run_query(sql)
    return(user)

@st.cache
def get_most_recommendations():
    sql = "SELECT user_name, sum FROM users u JOIN (SELECT user_id, SUM(recommendations) AS sum FROM articles GROUP BY user_id ORDER BY sum DESC LIMIT 1) AS a ON u.user_id = a.user_id;"
    user = run_query(sql)
    return(user)

@st.cache
def get_most_responses():
    sql = "SELECT user_name, sum FROM users u JOIN (SELECT user_id, SUM(responses) AS sum FROM articles GROUP BY user_id ORDER BY sum DESC LIMIT 1) AS a ON u.user_id = a.user_id;"
    user = run_query(sql)
    return(user)

user_most_published = pd.DataFrame.from_records(get_most_published(), columns=['user_name', 'counts'])
user_most_recommendations = pd.DataFrame.from_records(get_most_recommendations(), columns=['user_name', 'sum'])
user_most_responses = pd.DataFrame.from_records(get_most_responses(), columns=['user_name', 'sum'])


st.subheader(':sparkling_heart:Your personalized recommendation:sparkling_heart:')

user_df = df.groupby('user_id').size().reset_index(name='counts').sort_values(by="counts", ascending=False)
if len(user_df) == 1 or user_df['counts'].iloc[0] == user_df['counts'].iloc[1]:
    st.markdown(":exclamation:It seems like there aren't enough data existed to provide recommendations. Try another keyword or you can browse the author **{}** who publishes the most articles :point_right: **{}** or the author **{}** who receives the most recommendations :point_right: **{}** and also has the most responses :point_right: **{}**".format(
        user_most_published['user_name'].iloc[0], user_most_published['counts'].iloc[0], user_most_recommendations['user_name'].iloc[0], user_most_recommendations['sum'].iloc[0], user_most_responses['sum'].iloc[0]
    ))
else:
    recommendated_user = pd.DataFrame.from_records(get_author_data(user_df['user_id'].iloc[0]), columns=['user_id', 'user_name', 'description', 'followers'])
    st.markdown(":musical_note:Based on your keyword **{}**, user **{}** contributed the most! :point_right: **{}** articles in total! Check the author's profile on [TowardsDataScience](https://towardsdatascience.com) or have a brief look at the profile :point_right: \"**{}**\"".format(
        user_input, recommendated_user['user_name'].iloc[0], user_df['counts'].iloc[0], recommendated_user['description'].iloc[0]
    ))
    st.subheader(':gift: Bonus :gift:!')
    st.markdown(":musical_note:You can also browse the author **{}** who publishes the most articles :point_right: **{}** or the author **{}** who receives the most recommendations :point_right: **{}** and also has the most responses :point_right: **{}**".format(
        user_most_published['user_name'].iloc[0], user_most_published['counts'].iloc[0], user_most_recommendations['user_name'].iloc[0], user_most_recommendations['sum'].iloc[0], user_most_responses['sum'].iloc[0]
    ))







