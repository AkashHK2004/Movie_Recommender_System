import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# Load movies and similarity matrix
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))




# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# Streamlit app
st.header('Movie Recommender System')

movies_list = movies['title'].values

selected_movie_name = st.selectbox(
    'Type or select a movie name',
    movies_list
)

if st.button('Show Recommendation'):
    recommended_movies, recommended_posters = recommend(selected_movie_name)

    # Display recommendations
    if len(recommended_movies) > 0:
        col1, col2, col3, col4, col5 = st.columns(5)

        for i in range(min(5, len(recommended_movies))):
            with locals()[f"col{i + 1}"]:
                st.text(recommended_movies[i])
                st.image(recommended_posters[i])
    else:
        st.warning("No recommendations found for this movie.")

