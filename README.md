## **Demonstration**
[![](https://j.gifs.com/gpLYrk.gif)](https://youtu.be/ePhAuf2jVTQ)


:point_right: Choose one of sample keywords:  
[![](https://j.gifs.com/579nmY.gif)](https://youtu.be/ePhAuf2jVTQ)


:point_right: Or input your own keyword:  
[![](https://j.gifs.com/x6vqPB.gif)](https://youtu.be/ePhAuf2jVTQ)


:point_right: Showing relevant articles:  
[![](https://j.gifs.com/r2RZJp.gif)](https://youtu.be/ePhAuf2jVTQ)


:point_right: Analyze reading length:  
[![](https://j.gifs.com/MZQDMG.gif)](https://youtu.be/ePhAuf2jVTQ)


:point_right: Analyze Recommendations:  
[![](https://j.gifs.com/WP7OZx.gif)](https://youtu.be/ePhAuf2jVTQ)


:point_right: Analyze Responses:  
[![](https://j.gifs.com/Z8VO35.gif)](https://youtu.be/ePhAuf2jVTQ)


:point_right: Generate Recommendated User(s):  
[![](https://j.gifs.com/jYqQyv.gif)](https://youtu.be/ePhAuf2jVTQ)


## **Overview**
Hey there!:wave: Welcome to Xinyi's TowardsDataScience Data Analysis App. This app connectes to a Postgres database that contains data [web scraped](https://github.com/xxionias/webscraping/tree/master/mediumstories) from [TowardsDataScience](https:towardsdatascience.com) and analyzes data about your interests from published articles, including the distribution of the recommendations and responses of the articles and lengths of aricles. After some nice graphs, it tries to recommend an author that contributes the most to the topic that you are interested in. Give it a go!


## **Stories Dataset**
[Stories dataset](https://github.com/xxionias/webscraping/tree/master/mediumstories) were 43185 stories web scraped from [TowardsDataScience](http://towardsdatascience.com). The articles were published from 2016/02 to 2021/05.

Sample Record :
```
{"author": "Luuk Derksen", "linkOfAuthorProfile": "https://towardsdatascience.com/@luckylwk?source=collection_archive---------0-----------------------", "articleTitle": "Visualising high-dimensional datasets using PCA and t-SNE in Python", "articleLink": "https://towardsdatascience.com/visualising-high-dimensional-datasets-using-pca-and-t-sne-in-python-8ef87e7915b?source=collection_archive---------0-----------------------", "postingTime": "Oct 29, 2016", "minToRead": "10 min read", "recommendations": "5.4K", "responses": "23 responses"}
```

## **Profile Dataset**
[Profile dataset](https://github.com/xxionias/webscraping/tree/master/mediumprofile) were web scraped from user profiles link from the stories dataset.

Sample Record :
```
{"user_name": "Luuk Derksen", "desc": "Co-founder / CTO of @orbiit_ai. Data (Scientist) junky. All views my own.", "followers": "691 Followers"}
```


#### Dimension Tables
**users**  - users profiles
```
user_id, user_name, description, followers
```
**articles**  - songs in music database
```
article_id, title, user_id, posting_time, length_in_min, recommendations, responses
```


## Project Files

```sql_queries.py``` -> contains sql queries for dropping and creating fact and dimension tables. Also, contains insertion query template.

```create_tables.py``` -> contains code for setting up database. Running this file creates **medium_data** and also creates the dimension tables.

```etl.py``` -> read and process **stories_data** and **profile_data**

```app.py``` -> contains code to generate the [**Streamlit**](https://streamlit.io) web app

## Output Postgres Database  
| ![](images/users_sample.png) |
|:--:|
| <b>The `users` table has 16529 entries</b> |

| ![](images/articles_sample.png) |
|:--:|
| <b>The `articles` table has 3908 entries</b> |

GUI Tool Used Here - [Postico](https://eggerapps.at/postico/)

## Environment 
Python 3.6 or above

PostgresSQL 9.5 or above

psycopg2 - PostgreSQL database adapter for Python


## How to run

Run the drive program ```main.py``` as below.
```
python main.py
``` 

The ```create_tables.py``` and ```etl.py``` file can also be run independently as below:
```
python create_tables.py 
python etl.py 
```

Run the ```app.py``` as below.
```
streamlit run app.py
```

It should displays the following messages and pops out the web app:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.155:8501

  For better performance, install the Watchdog module:

  $ xcode-select --install
  $ pip install watchdog
```
