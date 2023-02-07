from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

popular_df = pd.read_pickle(open('popular_saved', 'rb'))
pt = pd.read_pickle(open('pt', 'rb'))
books = pd.read_pickle(open('books', 'rb'))
similarity_score = pd.read_pickle(open('similarity_score', 'rb'))


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=popular_df["Book-Title"].values,
                           author=popular_df["Book-Author"].values,
                           image=popular_df["Image-URL-M"].values,
                           votes=popular_df["num_ratings"].values,
                           ratings=popular_df["avg_ratings"].values
                          )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books["Book-Title"] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))

        data.append(item)
    print(data)
    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

