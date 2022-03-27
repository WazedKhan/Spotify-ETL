
import datetime
import requests
import pandas as pd


DATABASE_LOCATION = "sqlite:///tracks_list.sqlite"
USER_ID = "314zhyszvimzwwdaq5ehbsalknri"
TOKEN = "BQDdztbpsBImL1t-LkOelmi013GBVJqXQE2-GtJnBfZa_PyQpxYS5of-uWBxwwsUaY68YcMQ7BWvue-7Jz7edhOu1hJdt5tOSTbtc8Lds1KgyIcuBcDezQSIe-X7TzE8i7fybR2SU8hxl53t5-chITgDsk6G3jURWE2vuWOh"

if __name__ == "__main__":
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }


def data_validation(df: pd.DataFrame):
    # if df is empty
    if df.empty:
        print("No Song Lisented yesterday")
        return False
    # check if data duplicate
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception('Dulicated Song')
    # chcek is 
    if df.isnull().values.any():
        raise Exception('Null Value Found')
    
    print(df)


today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
yesterday_unix_timestamp = int(yesterday.timestamp())*1000

r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers=headers)

data = r.json()
song_name = []
artist_name = []
played_at_list = []
timestamps = []
  
try:
    for song in data['items']:
        song_name.append(song['track']['name'])
        artist_name.append(song['track']['album']['artists'][0]['name'])
        played_at_list.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])
except KeyError:
    print('Spotify Token Expired')


song_dic = {
    'song_name':song_name,
    'artist_name':artist_name,
    'played_at':played_at_list,
    'timestamp':timestamps,
}


df = pd.DataFrame(song_dic, columns=['song_name','artist_name','played_at','timestamp'])
data_validation(df)