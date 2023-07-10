# Import 
import numpy as np
import pandas as pd
from textblob import TextBlob
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# Generate Playlist Feature
def playlist_to_feature(complete_feature_set, playlist_df):
    '''
    Creates Feature Vector of the Playlist
    ---
    Input:
    complete_feature_set (pandas DataFrame): Song features data
    playlist_df (pandas DataFrame): Song features data in the playlist
    
    Output:
    in_playlist (pandas Series): Playlist Vector
    non_playlist (pandas DataFrame): Set of all the song features not in the playlist
    '''
    
    # Create a list of the ids of all the songs in the playlist
    ids = list(playlist_df['id'])
    
    # Find song features in the playlist
    in_playlist = complete_feature_set[complete_feature_set['id'].isin(ids)]
    # Remove those ids from the superset
    non_playlist = complete_feature_set[~complete_feature_set['id'].isin(ids)]
    
    # Drop the id
    in_playlist.drop(['id'], axis = 'columns', inplace = True)
    
    return in_playlist.sum(axis = 0), non_playlist


# Generate Recommendations
def generate_recommendation(df, features, non_playlist, n):
    '''
    Generates Recommendation Based on a Given Playlist
    ---
    Input:
    df (pandas DataFrame): All songs DataFrame
    features (pandas DataFrame): Playlist Feature Vector
    non_playlist (pandas DataFrame): Song Features not in the Playlist
    
    Output:
    non_playlist_top_40 (pandas DataFrame): Top 40 Recommendations
    '''
    
    non_playlist_data = df[df['id'].isin(non_playlist['id'].values)]
    
    # Find Cosine Similarity
    non_playlist_data['sim'] = cosine_similarity(non_playlist.drop(['id'], axis = 'columns').values,
                                                [features.values.reshape(-1, 1)[:,0]])
    # Select Top 40
    non_playlist_top_n = non_playlist_data.sort_values('sim',ascending = False).head(n)
    
    return non_playlist_top_n[['artist_name', 'track_name', 'track_uri']]


# Recommend
def recommend(playlist_df, n):
    # Read Data
    song_df = pd.read_csv('feature-data.csv')
    song_db = pd.read_csv('Feature-data-clean.csv')
    
    playlist_vector, non_playlist_vector = playlist_to_feature(song_db, playlist_df)
    
    recommendations = generate_recommendation(song_df, playlist_vector, non_playlist_vector, n)

    return recommendations.to_html(classes='table table-stripped')