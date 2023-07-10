# Imports
import re
import spotipy
import pandas as pd
from tqdm import tqdm
from spotipy.oauth2 import SpotifyClientCredentials


# Tester
test_extractor = True

# API Key
ids = pd.read_csv('/Users/nikhil/Desktop/spotify_million_playlist_dataset/id.csv')
cid = ids['Cid'][0]
secret = ids['Secret'][0]

# Authentication
client_credentials_manager = SpotifyClientCredentials(client_id = cid, client_secret = secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# Dataset
df = pd.read_csv('../raw-data.csv')
df['track_uri'] = df['track_uri'].apply(lambda x: x.replace('spotify:track:', ''))


# Feature Extractor
def feature_from_uri(t, uri):
    try:
        # Audio Features
        features = sp.audio_features(uri)[0]
        
        # Artist, Popularity, Genres
        artist = t['artists'][0]['id']
        artist_dict = sp.artist(artist)
        artist_pop = artist_dict['popularity']
        artist_genres = artist_dict['genres']
        
        # Track popularity
        track_pop = t['popularity']
        
        # Add in extra features
        features['artist_pop'] = artist_pop
        if artist_genres:
            features['genres'] = ' '.join([re.sub(' ','_',i) for i in artist_genres])
        else:
            features['genres'] = 'unknown'
        features['track_pop'] = track_pop
    
        return features
    except:
        return None

# Extractor
def extract(chunk):
    
    tracks = sp.tracks(chunk)
    
    output = []
    for t, uri in zip(tracks['tracks'], chunk):
        item = feature_from_uri(t, uri)
        if item is not None:
            output.append(item)
        
    return output


if test_extractor:
    uri = df['track_uri'][:49]
    op = extract(uri)
    columns = list(op[0].keys())
    print(op)
    

rows = df.shape[0]
j = 0
for i in tqdm(range(-1,rows,50)):
    start = i+1
    end = i+50
    if end >= rows:
        end = rows-1
    batch = df['track_uri'][start:end]
    data = extract(batch)
    features = pd.DataFrame(data, columns = columns)
    features.to_csv(f'../feature-data/features-raw{j}.csv', index = False)
    j = j + 1
    (df[~df['track_uri'].isin(batch)]).to_csv('../pending-data.csv', index = False)