from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load movie data and similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('movie_list.pkl', 'rb'))
movie_list = movies['title'].values

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    return [movies['title'][i[0]] for i in movie_indices]

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    selected_movie = None

    if request.method == 'POST':
        selected_movie = request.form['movie']
        recommendations = recommend(selected_movie)

    return render_template('index.html', movies=movie_list, selected_movie=selected_movie, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
