import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

# Store the `user_name`: `user_id`
d = {}

def process_profile_file(cur, filepath):
    """
    Process songs files and insert records into the Postgres database.
    :param cur: cursor reference
    :param filepath: complete file path for the file to load
    """

    # open profile file
    df = pd.read_json(filepath)

    # Only keep the entries that have not null `user_name`
    df = df.dropna(subset=['user_name'])

    # Change the 'null' entries to '0 follower'
    df['followers'].fillna('0 follower', inplace=True)

    # Transform the format from "[num] follower(s)" to "num" in integer
    df['followers'] = df['followers'].str.split(' ').str[0]

    # Format "[3.4]K" to "3400" and convert string to integer
    def convert_followers(x):
            if x[-1] == 'K':
                x = int(float(x[:-1]) * 1000)
            else:   
                x = int(x)
            return x
        
    df['followers'] = df['followers'].apply(convert_followers)

    # Keep track of the `user_id`
    idx = 1

    for value in df.values:
        user_name, desc, followers = value

        if user_name and user_name not in d:
            # Insert user record
            users_data = (user_name, desc, followers)
            cur.execute(users_table_insert, users_data)
            d[user_name] = idx
            idx += 1
    
    print(f"Records inserted for file {filepath}")


def process_stories_file(cur, filepath):
    """
    Process Event log files and insert records into the Postgres database.
    :param cur: cursor reference
    :param filepath: complete file path for the file to load
    """
    # Open log file
    df = pd.read_json(filepath)

    # Drop the unnecessary columns
    df = df.drop(['linkOfAuthorProfile', 'articleLink'], axis=1)

    # Keep only entries that have not null values in these columns
    df = df.dropna(subset=['author', 'articleTitle', 'postingTime', 'minToRead'])

    # Convert this year's data format in "[Month] [day]" to "[Month] [day] [2021]"
    def convert_date(x):
        if ',' not in x:
            x += ', 2021'
        return x

    df['postingTime'] = df['postingTime'].apply(convert_date)

    # Convert the data format in "[Month] [day] [year]" to datetime format
    df['postingTime'] = pd.to_datetime(df['postingTime'], format='%b %d, %Y')

    # Fill the null entries in "recommendations" with "0"
    df['recommendations'].fillna('0', inplace=True)

    # Fill the null entries in "responses" with "0 response"
    df['responses'].fillna('0 response', inplace=True)

    # Format "[3.4]K" to "3400"
    def convert_recommendations(x):
        if x[-1] == 'K':
            x = int(float(x[:-1]) * 1000)
        else:   
            x = int(x)
        return x
    
    df['recommendations'] = df['recommendations'].apply(convert_recommendations)

    # Convert both string columns to integer
    df['responses'] = df['responses'].str.split(' ').str[0].astype(int)
    df['minToRead'] = df['minToRead'].str.split(' ').str[0].astype(int)

    # Insert article record
    for value in df.values:
        author, title, date, length, recommendations, responses = value
        if author and author in d:
            # Find `user_id` from the dictionary
            user_id = d[author]
            articles_data = (title, user_id, date, length, recommendations, responses)
            cur.execute(articles_table_insert, articles_data)


def process_data(cur, conn, filepath, func):
    """
    Driver function to load data from songs and event log files into Postgres database.
    :param cur: a database cursor reference
    :param conn: database connection reference
    :param filepath: parent directory where the files exists
    :param func: function to call
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Driver function for loading songs and log data into Postgres database
    """
    conn = psycopg2.connect("host='localhost' dbname='medium_data' user='user0' password='7248'")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/profile', func=process_profile_file)
    process_data(cur, conn, filepath='data/stories', func=process_stories_file)

    conn.close()


if __name__ == "__main__":
    main()
    print("\n\nFinished processing!!!\n\n")