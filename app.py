import streamlit as st
import pickle
import pandas as pd
import requests
import lz4.frame  # For loading compressed similarity file


def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d704d0412d19b5ae8e990d1d4c8eaff7')
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_posters


# Load movie dictionary
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load compressed similarity file (.lz4)
with lz4.frame.open('compressed_similarity.pkl.lz4', 'rb') as f:
    similarity = pickle.load(f)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    with cols[0]:
        st.text(names[0])
        st.image(posters[0])

    with cols[1]:
        st.text(names[1])
        st.image(posters[1])

    with cols[2]:
        st.text(names[2])
        st.image(posters[2])

    with cols[3]:
        st.text(names[3])
        st.image(posters[3])

    with cols[4]:
        st.text(names[4])
        st.image(posters[4])

  

