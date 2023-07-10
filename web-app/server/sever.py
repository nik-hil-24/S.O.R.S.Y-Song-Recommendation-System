# Imports
import pandas as pd
from utils import recommend
from features import extract
from flask import Flask, request, jsonify
from cleaning_pipeline import preprocessing_pipeline

# App
app = Flask(__name__)


# Route
@app.route('/Recommend_Songs', methods=['GET', 'POST'])
def recommend_playlist():
    # Get Form Data
    playlist_id = str(request.form['id'])
    n = int(request.form['num_songs'])
    
    # Get Features From Playlist
    df = extract(playlist_id)

    # Preprocess the data
    playlist_df = preprocessing_pipeline(df)
    
    # Pass Through The Model
    html = recommend(playlist_df, n).replace('table ', "table style='color: white;'")
    
    # Server Response
    response = jsonify({
        'recommendations': html
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response


# For running the server
if __name__ == "__main__":
    print("Starting Python Flask Server...")
    app.run()