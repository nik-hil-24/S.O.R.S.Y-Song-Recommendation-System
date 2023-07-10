import re
import json
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

def artist_data(sp, t):
    # Artist, Popularity, Genres
    artist = t['artists'][0]['id']
    artist_name = t['artists'][0]['name']
    artist_dict = sp.artist(artist)
    artist_pop = artist_dict['popularity']
    artist_genres = ' '.join([re.sub(' ','_',i) for i in artist_dict['genres']])
    
    return artist_name, artist_pop, artist_genres
    

def extract(URL):
    client_id = "2536f0cd9d324071b94aeb48dcdd5557" 
    client_secret = "60593dd53bec4a0c86c5e04dbcc09751"

    #use the clint secret and id details
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # the URI is split by ':' to get the username and playlist ID
    playlist_id = URL.split("/")[4].split("?")[0]
    playlist_tracks_data = sp.playlist_tracks(playlist_id)

    #lists that will be filled in with features
    playlist_tracks_id = []
    playlist_artist_pops = []
    playlist_tracks_pops = []
    playlist_artist_names = []
    playlist_artist_genres = []
    playlist_tracks_titles = []

    #go through the dictionary to extract the data
    for track in playlist_tracks_data['items']: 
        t = track['track']
        
        if t is not None:
            # Artist Data
            artist_name, artist_pop, artist_genres = artist_data(sp, t)
            # Track Name, Popularity, Id
            track_name = t['name']
            track_pop = t['popularity']
            track_id = t['uri'].replace('spotify:track:', '')
            
            playlist_tracks_id.append(track_id)
            playlist_artist_pops.append(artist_pop)
            playlist_tracks_pops.append(track_pop)
            playlist_artist_names.append(artist_name)
            playlist_artist_genres.append(artist_genres)
            playlist_tracks_titles.append(track_name)
        
        
        
    # Track Features
    features = sp.audio_features(playlist_tracks_id)
    
    features = sp.audio_features(playlist_tracks_id)
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df['track_name'] = playlist_tracks_titles
    features_df['id'] = playlist_tracks_id
    features_df['artist_pop'] = playlist_artist_pops
    features_df['track_pop'] = playlist_tracks_pops
    features_df['artist_name'] = playlist_artist_names
    features_df['genres'] = playlist_artist_genres


    return features_df