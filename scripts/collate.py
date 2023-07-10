# Imports
import os
import json
import pandas as pd

# Data Folder
folder = 'data'

# List of all songs
ls = []

# Reading each json file
for file in os.listdir(folder):
    if file[-5:] == '.json':
        path = folder + '/' + file
        f = open(path, 'r')
        data = json.loads(f.read())
        
        # Extracting list of tracks
        tracks = (data['playlists'][0])['tracks']
        for i in tracks:
            ls.append(i)

# Creating DataFrame from list of tracks
df = pd.DataFrame.from_dict(ls)
df.to_csv('raw-data.csv', index = False)