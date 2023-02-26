from flask import Flask, render_template, request
import ast
import os
import json
import numpy as np
from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import abort
from flask.json import jsonify
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import fashion_mnist
import pandas as pd
import tensorflow as tf


app = Flask(__name__)


# Let's load the trained model
model = tf.keras.models.load_model('model_anime_1.h5', compile=False)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        Title = request.form['title']
        Genre = request.form['genre']
        Description = request.form['description']
        Anime_type = request.form['type']
        Producer = request.form['producer']
        Studio = request.form['studio']

        X = {'Title': Title,
             'Genre': Genre,
             'Description': Description,
             'Anime_type': Anime_type,
             'Producer': Producer,
             'Studio': Studio
             }

        X = pd.DataFrame.from_dict(X)
        return redirect(f"/result/{X}")


@app.route('/result/<X>')
def result(X):
    return f"Your anime is: {X}"


if __name__ == '__main__':
    app.run(debug=True)
