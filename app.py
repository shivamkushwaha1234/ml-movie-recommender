import streamlit as st
import pickle
import pandas as pd
import requests
import lz4.frame
import os


def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d704d0412d19b5ae8e990d1d4c8eaff7')
        data = response.json()
        return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters


# Streamlit page config
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

st.title('🎥 Movie Recommender System')

# Load movie_dict
if os.path.exists('movie_dict.pkl'):
    with open('movie_dict.pkl', 'rb') as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
    st.write(f"✅ Loaded {len(movies)} movies.")
else:
    st.error("❌ movie_dict.pkl not found.")
    st.stop()

# Load compressed similarity
try:
    with lz4.frame.open('compressed_similarity.pkl.lz4', 'rb') as f:
        similarity = pickle.load(f)
    st.write(f"✅ Similarity matrix loaded. Length: {len(similarity)}")
except Exception as e:
    st.error(f"❌ Failed to load similarity matrix: {e}")
    st.stop()

# Movie selection
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

  

