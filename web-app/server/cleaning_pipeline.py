# Import 
import numpy as np
import pandas as pd
from textblob import TextBlob
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# Removing Redundant Columns
def select_cols(df):
    '''
    Select useful columns
    '''
    
    return df[['artist_name', 'id', 'track_name', 'danceability', 'energy', 'key',
             'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
             'liveness', 'valence', 'tempo', 'artist_pop', 'genres', 'track_pop']]


# Creating genre list
def genre_list(df):
    '''
    Preprocess genre data
    '''
    
    return df['genres'].apply(lambda x: list(x.split()))


# Create Features
def get_subjectivity(text):
    '''
    Returns subjectivity of text
    Input:
    text (str): String to be analyzed
    
    Output:
    str
    '''
    
    return TextBlob(text).sentiment.subjectivity

def get_polarity(text):
    '''
    Returns polarity of text
    Input:
    text (str): String to be analyzed
    
    Output:
    str
    '''
    
    return TextBlob(text).sentiment.polarity

def get_analysis(x, task = 'polarity'):
    '''
    Categorize scores
    '''
    
    if task == 'subjectivity':
        if x > 1/3:
            return 'high'
        elif x < 1/3:
            return 'low'
        else:
            return 'medium'
    else:
        if x > 0:
            return 'positive'
        elif x < 0:
            return 'negative'
        else:
            return 'neutral'


def sentiment_analysis(df, col):
    '''
    Creates sentiment columns
    Input: 
    df (pandas dataframe): Spotify Dataframe
    col (str): Column to be processed
        
    Output: 
    df (pandas dataframe): Sentiment features
    '''
    
    df['subjectivity'] = df[col].apply(lambda x: get_analysis(get_subjectivity(x), 'subjectivity'))
    df['polarity'] = df[col].apply(lambda x: get_analysis(get_polarity(x)))
    return df


# One-hot Encoder
def ohe(df, col, new_name):
    ''' 
    Create One Hot Encoded features of a specific column
    ---
    Input: 
    df (pandas dataframe): Dataframe
    col (str): Column to be processed
    new_name (str): new column name to be used
        
    Output: 
    dummies (pandas dataframe): One-hot encoded features 
    '''
    
    dummies = pd.get_dummies(df[col])
    columns = dummies.columns
    dummies.columns = [new_name + '|' + str(name) for name in columns]
    return dummies


# Vectorize column
def vectorize(df, col, new_name):
    ''' 
    Create TFIDF-Vectorized features of a specific column
    ---
    Input: 
    df (pandas dataframe): Dataframe
    col (str): Column to be processed
    new_name (str): new column name to be used
        
    Output: 
    vector_df (pandas dataframe): TFIDF features 
    '''
    
    tfidf = TfidfVectorizer()
    vector = tfidf.fit_transform(df[col])
    vector_df = pd.DataFrame(vector.toarray())
    vector_df.columns = [new_name + '|' + i for i in tfidf.get_feature_names_out()]
    return vector_df


# Normalize
def normalize(column):
    ''' 
    Create Normalized features of a specific column
    ---
    Input: 
    column (pandas dataframe): Dataframe
   
    Output: 
    norm_feature (pandas dataframe): Normalized features 
    '''
    
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(column)
    norm_feature = pd.DataFrame(scaled, columns = column.columns)
    return norm_feature


def preprocessing_pipeline(df):
    '''
    Preprocesses Spotify-dataset for recommendation system
    ---
    Input:
    df (pandas dataframe): Spotify-dataset DataFrame
    
    Output:
    final_df (pandas dataframe): Preprocessed DataFrame
    '''
    
    # Select Columns
    df = select_cols(df)
    
    # Float columns
    float_cols = df.dtypes[df.dtypes == 'float64'].index.values
    
    # Sentiment Analysis
    df = sentiment_analysis(df, 'track_name')
    
    # OHE
    subject_ohe = ohe(df, 'subjectivity', 'subject')
    polar_ohe = ohe(df, 'polarity', 'polar')
    mode_ohe = ohe(df, 'mode', 'mode')
    key_ohe = ohe(df, 'key', 'key')
    
    # TFIDF
    genre_vector = vectorize(df, 'genres', 'genre')
    
    # Normalization
    norm_pop = normalize(df[['artist_pop', 'track_pop']])
    norm_floats = normalize(df[float_cols])
    
    # Concatenate
    final_df = pd.concat([subject_ohe, polar_ohe, mode_ohe, key_ohe,
                          genre_vector, norm_pop, norm_floats],
                         axis = 1)
    
    # Give ID col
    final_df['id'] = df['id']
    
    return final_df