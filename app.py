import streamlit as st
import pickle
import pandas as pd
import requests

movies = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies)

sim = pickle.load(open('similarity.pkl', 'rb'))

def fetch_posters(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6cf07d7428089335d21c00f4e4577822'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    dist = sim[movie_index]
    sim_movies = sorted(list(enumerate(dist)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []

    for i in sim_movies:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
    
    return recommended_movies, recommended_movies_posters

st.title('TMDB Movie Recommendation System')

selected_movie = st.selectbox('Enter the name of a movie you like:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(spec=5, gap='small')
    with col1:
        st.subheader(names[0])
        st.image(posters[0])
    with col2:
        st.subheader(names[1])
        st.image(posters[1])
    with col3:
        st.subheader(names[2])
        st.image(posters[2])
    with col4:
        st.subheader(names[3])
        st.image(posters[3])
    with col5:
        st.subheader(names[4])
        st.image(posters[4])