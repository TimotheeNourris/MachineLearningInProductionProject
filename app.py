from flask import Flask, render_template, request
from keras.models import load_model
import pandas as  pd
import numpy as  np
from sklearn.preprocessing import MultiLabelBinarizer
from tensorflow import keras
import gensim

app = Flask(__name__)

# Model ML ------------------------------------------------------------

model = load_model('model_anime_final.h5')

df = pd.read_csv('Anime_data.csv')

ratings = df['Rating']
df['Rating'] = ratings.fillna(0)

df = df.dropna()

df = df.reset_index(drop=True)

df = df.drop(columns=['Anime_id','ScoredBy','Popularity','Members','Episodes','Source','Aired','Link'])

# Routes --------------------------------------------------------------

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    genre = request.form['genre']
    synopsis = request.form['synopsis']
    type = request.form['type']
    producer = request.form['producer']
    studio = request.form['studio']

    x = pd.DataFrame({'Title': title,  'Genre': genre, 'Synopsis': synopsis,'Type': type, 'Producer': producer,'Studio': studio, 'Rating':0}, index=[0])
    
    df = pd.read_csv('Anime_data.csv')

    ratings = df['Rating']
    df['Rating'] = ratings.fillna(0)

    df = df.dropna()

    df = df.reset_index(drop=True)

    df = df.drop(columns=['Anime_id','ScoredBy','Popularity','Members','Episodes','Source','Aired','Link'])
    df = df.append(x)
    df = df.append(x)

    df = df.reset_index(drop=True)

    """## Encoding Genre"""

    df_genre = df[["Genre","Rating"]]
    df_genre = df_genre.dropna()
    df_genre['Genre'] = df_genre.Genre.apply(lambda x: x[1:-1].split(','))
    mlb = MultiLabelBinarizer()
    df_genre = df_genre.join(pd.DataFrame(mlb.fit_transform(df_genre.pop('Genre')),
                              columns=mlb.classes_,
                              index=df_genre.index))

    #X_train = df_genre
    x_train_genre = df_genre.iloc[0:-1, 1:-1]
    y_train_genre = df_genre['Rating']

    """## Encoding Producer

    """

    df_Producer = df[["Producer","Rating"]]
    df_Producer = df_Producer.dropna()

    df_Producer['Producer'] = df_Producer.Producer.apply(lambda x: x[1:-1].split(','))
    mlb = MultiLabelBinarizer()
    df_Producer = df_Producer.join(pd.DataFrame(mlb.fit_transform(df_Producer.pop('Producer')),
                              columns=mlb.classes_,
                              index=df_Producer.index))

    x_train_Producer = df_Producer.iloc[0:-1, 1:-1]
    y_train_Producer = df_Producer['Rating']

    """## Encoding Studio

    """

    df_Studio = df[["Studio","Rating"]]
    df_Studio = df_Studio.dropna()

    df_Studio['Studio'] = df_Studio.Studio.apply(lambda x: x[1:-1].split(','))
    mlb = MultiLabelBinarizer()
    df_Studio = df_Studio.join(pd.DataFrame(mlb.fit_transform(df_Studio.pop('Studio')),
                              columns=mlb.classes_,
                              index=df_Studio.index))

    x_train_Studio = df_Studio.iloc[0:-1, 1:-1]
    y_train_Studio = df_Studio['Rating']

    """## Encoding Type"""

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

    

    """# all"""

    df_end = pd.concat([x_train_genre,x_train_Producer,x_train_Studio,x_train_Type], axis=1)

    df_end = pd.concat([df['Rating'],df_end], axis=1)

    df_end = df_end.dropna()

    topred = df_end.drop(columns=['Rating']).iloc[-1]
    topred = pd.DataFrame(topred)
    topred = topred.transpose()

    rating = model.predict(topred)
    
    return render_template('result.html', title=title, genre=genre, synopsis=synopsis, type=type, producer=producer, studio=studio, rating=rating)


if __name__ == "__main__":
    app.run(debug=True)