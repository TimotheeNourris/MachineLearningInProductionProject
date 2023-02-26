from flask import Flask, render_template, request
import ast
import os
import json
import numpy as np
from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask.json import jsonify
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import fashion_mnist 
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MultiLabelBinarizer


app = Flask(__name__)


# Let's load the trained model
model = tf.keras.models.load_model('model_anime_3.h5', compile=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Title = request.form['title']
        Genre = request.form['genre']
        Synopsis = request.form['synopsis']
        Anime_type = request.form['type']
        Producer = request.form['producer']
        Studio = request.form['studio']

        data_input = pd.DataFrame({
            'Title' : Title, 
            'Genre' : Genre,
            'Synopsis' : Synopsis,
            'Type' : Anime_type,
            'Producer' : Producer,
            'Studio' : Studio,
            'Rating' : 0
            }, index=[0]) 


        df = pd.read_csv('Anime_data.csv')


        # We do pre-processing
        ratings = df['Rating']
        df['Rating'] = ratings.fillna(0)
        df = df.dropna()
        df = df.reset_index(drop=True)
        df = df.drop(columns=['Anime_id','ScoredBy','Popularity','Members','Episodes','Source','Aired','Link'])
        df = df.append(data_input)
        df = df.append(data_input)
        
        df = df.reset_index(drop = True)

        # encoding genre
        df_genre = df[["Genre","Rating"]]
        df_genre = df_genre.dropna()
        df_genre['Genre'] = df_genre.Genre.apply(lambda x: x[1:-1].split(','))
        mlb = MultiLabelBinarizer()
        df_genre = df_genre.join(pd.DataFrame(mlb.fit_transform(df_genre.pop('Genre')),
                                  columns=mlb.classes_,
                                  index=df_genre.index))


        x_train_genre = df_genre.iloc[0:-1, 1:-1]
        y_train_genre = df_genre['Rating']

        # encoding producer 
        df_Producer = df[["Producer","Rating"]]
        df_Producer = df_Producer.dropna()

        df_Producer['Producer'] = df_Producer.Producer.apply(lambda x: x[1:-1].split(','))
        mlb = MultiLabelBinarizer()
        df_Producer = df_Producer.join(pd.DataFrame(mlb.fit_transform(df_Producer.pop('Producer')),
                                  columns=mlb.classes_,
                                  index=df_Producer.index))

        x_train_Producer = df_Producer.iloc[0:-1, 1:-1]
        y_train_Producer = df_Producer['Rating']


        # encoding studio

        df_Studio = df[["Studio","Rating"]]
        df_Studio = df_Studio.dropna()

        df_Studio['Studio'] = df_Studio.Studio.apply(lambda x: x[1:-1].split(','))
        mlb = MultiLabelBinarizer()
        df_Studio = df_Studio.join(pd.DataFrame(mlb.fit_transform(df_Studio.pop('Studio')),
                                  columns=mlb.classes_,
                                  index=df_Studio.index))

        x_train_Studio = df_Studio.iloc[0:-1, 1:-1]
        y_train_Studio = df_Studio['Rating']

        # encoding type
        from sklearn.preprocessing import OneHotEncoder

        df_Type = df[["Type","Rating"]]
        df_Type = df_Type.dropna()

        encoder = OneHotEncoder()
        Type = encoder.fit_transform(df_Type.Type.values.reshape(-1,1)).toarray()
        df_OH = pd.DataFrame(Type, columns = [str(encoder.categories_[0][i]) 
                                             for i in range(len(encoder.categories_[0]))])
        df_Type = pd.concat([df_Type['Rating'], df_OH], axis=1)
        df_Type = df_Type.dropna()

        x_train_Type = df_Type.iloc[0:-1, 1:-1]
        y_train_Type = df_Type['Rating']


        # we concatenate all the results in one
        df_end = pd.concat([x_train_genre,x_train_Producer,x_train_Studio,x_train_Type], axis=1)
        df_end = pd.concat([df['Rating'],df_end], axis=1)
        df_end = df_end.dropna()

        topred = df_end.drop(columns=['Rating']).iloc[-1]
        topred = pd.DataFrame(topred)
        topred = topred.transpose()

        # let's do the prediction

        prediction = model.predict(topred)
   
        #return f'Title: {Title}, Genre: {Genre}, Description: {Description}, Type: {Anime_type}, Producer: {Producer}, Studio: {Studio}, Rating: {Rating}'
        return f'prediction: {prediction}'

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
