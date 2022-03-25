import json
import sqlite3
import datetime
from time import time
import requests
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker


DATABASE_LOCATION = "sqlite:///tracks_list.sqlite"
USER_ID = "314zhyszvimzwwdaq5ehbsalknri"
TOKEN = "BQC2TUPnm6xRdkv60QJa7gCXHa0QTQd9hdkU6k4uIrzK8IdMFuMbpSdvA1F7vFdnWw9h1eV3lZhhrCb7hsmgSmVma5BTFlohxpv-LTdK_tcGH1Sn-iaYvAi2HQIIibqyBu6ZGHO8kKC4mTh5ft_Ax4irUfmhLUUJjTsEu5fq"

if __name__ == "__main__":
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
yesterday_unix_timestamp = int(yesterday.timestamp())*1000

r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers=headers)

data = r.json()

song_name = []
artist_name = []
played_at_list = []
timestamps = []

for song in data['items']:
    song_name.append(song['track']['name'])
    artist_name.append(song['track']['album']['artists'][0]['name'])
    played_at_list.append(song['played_at'])
    timestamps.append(song['played_at'][0:10])


song_dic = {
    'song_name':song_name,
    'artist_name':artist_name,
    'played_at':played_at_list,
    'timestamp':timestamps,
}


df = pd.DataFrame(song_dic, columns=['song_name','artist_name','played_at','timestamp'])
df.to_csv('songs.csv')