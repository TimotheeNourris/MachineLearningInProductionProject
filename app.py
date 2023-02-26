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


app = Flask(__name__)


# Let's load the trained model
model = tf.keras.models.load_model('model_anime_1.h5', compile=False)


@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        Title = request.form['title']
        Genre = request.form['genre']
        Description = request.form['description']
        Anime_type = request.form['type']
        Producer = request.form['producer']
        Studio = request.form['studio']

        X = {'Title' : Title, 
            'Genre' : Genre,
            'Description' : Description,
            'Anime_type' : Anime_type,
            'Producer' : Producer,
            'Studio' : Studio
            }
    X = pd.DataFrame.from_dict(X)   
    # make the prediction
    #prediction = model.predict(X)    
    return f'X: {X}'
    #return f'Title: {title}, Genre: {genre}, Description: {description}, Type: {anime_type}, Producer: {producer}, Studio: {studio}'


    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)