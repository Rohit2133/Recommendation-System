import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import requests
import os


# Load the pre-trained model and movies data
movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = joblib.load('similarity.pkl')

# omdb api key
OMDB_API_KEY = os.environ.get("OMDB_API_KEY")


# Function to fetch poster from OMDb using title
def fetch_omdb_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster', 'https://via.placeholder.com/300x450?text=No+Poster+Found')


# Function to get movie recommendations
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse = True,key = lambda x : x[1])[1:6]
    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        poster_url = fetch_omdb_poster(title)
        recommended_posters.append(poster_url)

    return recommended_movies , recommended_posters



# Streamlit app setup
# App Title
st.markdown("""
    <h1 style='text-align: center; color: #F39C12;'>🎬 Movie Recommendation System</h1>
    <p style='text-align: center;'>Get your next favorite movie based on what you love!</p>
    """, unsafe_allow_html=True)

option = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)
if st.button('Recommend'):
    names, posters = recommend(option)
    st.write("### Recommended Movies:")

    # Display in a row using columns
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], caption=names[i], use_container_width=True)
    st.write("### Enjoy your movie night! 🍿")

# Sidebar Info
st.sidebar.header("About")
st.sidebar.info("This is a content-based movie recommendation system using Python, Streamlit, Multiple Python Libraries(like Pandas, Numpy, Scikit-learn, Pickle, Requests) and TMDB Data & OMDb API.")
st.sidebar.markdown("Made with ❤️ by [Rohit Aggarwal](https://github.com/Rohit2133)")

# Footer
st.markdown("""
    <hr>
    <p style='text-align:center; color:gray;'>Built with ❤️ using Streamlit</p>
    """, unsafe_allow_html=True)
