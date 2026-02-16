import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c55373b6e69eb15a27a0a0597bf5c8dd"
        data = requests.get(url, timeout=10).json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return None

    except requests.exceptions.RequestException:
        return None



def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id   # IMPORTANT

        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System') 

selected_movie_name = st.selectbox(
    'Movies List',
    movies['title'].values
)

st.write("Selected Movie:", selected_movie_name)

if st.button('Recommend'):

    names, posters = recommend(selected_movie_name)

    for i in range(len(names)):
        st.subheader(names[i])
        if posters[i]:
            st.image(posters[i])
        else:
            st.write("Poster not available")

    


