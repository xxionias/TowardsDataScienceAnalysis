# DROP TABLES
users_table_drop = "DROP TABLE IF EXISTS users"
articles_table_drop = "DROP TABLE IF EXISTS articles"

# CREATE TABLES
users_table_create = ("""CREATE TABLE IF NOT EXISTS users(
    user_id SERIAL CONSTRAINT userid_pk PRIMARY KEY,
	user_name TEXT, 
    description TEXT,
    followers INT
)""")

articles_table_create = ("""CREATE TABLE IF NOT EXISTS articles(
    article_id SERIAL CONSTRAINT articleid_pk PRIMARY KEY,
	title TEXT NOT NULL,
    user_id INT REFERENCES users(user_id),
    posting_time DATE NOT NULL,
    length_in_min INT NOT NULL,
    recommendations INT,
    responses INT
)""")

# INSERT RECORDS
users_table_insert = ("""INSERT INTO users VALUES (DEFAULT, %s, %s, %s)
""")


# Updating the user level on conflict
articles_table_insert = ("""INSERT INTO articles VALUES (DEFAULT, %s, %s, %s, %s, %s, %s) 
""")

# ON CONFLICT (user_id) DO NOTHING

# FIND ARTICLES
article_select = ("""
    SELECT song_id, artists.artist_id
    FROM articles a JOIN users u ON a.user_id = u.user_id
""")

    #WHERE a.title = %s
    # AND a.name = %s
    # AND a.duration = %s

# QUERY LISTS
create_table_queries = [users_table_create, articles_table_create]
drop_table_queries = [articles_table_drop, users_table_drop]