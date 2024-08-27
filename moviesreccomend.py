import streamlit as st
import pickle
import pandas as pd
import difflib
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image


def posters(id):
    post = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=65730a8a46c44d011ee53d2b2db42c43'.format(id))
    po = post.json()

    return 'https://image.tmdb.org/t/p/w500'+po['poster_path'], po['vote_average']


def mo(nm):
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
    list_of_all_titles = mov['title'].tolist()

    find_close_match = difflib.get_close_matches(
        nm, list_of_all_titles)

    close_match = find_close_match[0]

    index_of_the_movie = mov[mov.title ==
                             close_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    sorted_similar_movies = sorted(
        similarity_score, key=lambda x: x[1], reverse=True)

    st.write('Movies suggested for you : \n')

    i = 1
    recmo = []
    recpo = []
    imbd = []
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = mov[mov.index == index]['title'].values[0]
        id_from_index = mov[mov.index == index]['id'].values[0]
        print(id_from_index)
        if (i <= 20):
            # st.write(posters(id_from_index))
            recmo.append(title_from_index)
            pos, imb = posters(id_from_index)
            recpo.append(pos)
            imbd.append(imb)
            # st.write(id_from_index, '.', title_from_index)

        i += 1
        if i == 20:
            break

    return recmo, recpo, imbd


mov = pickle.load(open('movie.pkl', 'rb'))
mov = pd.DataFrame(mov)

st.title("Similar Movies")
options = st.selectbox('ENTER THE NAME OF THE MOVIE',
                       (mov['original_title'].values))

if st.button('Suggest'):

    recm, recp, imbd = mo(options)

    col1, col2, col3 = st.columns(3)
    i = 0
    while i < 6:
        with col1:
            st.write(f"<b>{recm[i]}</b>", unsafe_allow_html=True)
            st.text(f"IMBD RATING : {imbd[i]}/10")

            st.image(recp[i], width=200)
            i = i+1

    while i < 12:
        with col2:
            st.write(f"<b>{recm[i]}</b>", unsafe_allow_html=True)
            st.text(f"IMBD RATING : {imbd[i]}/10")

            st.image(recp[i], width=200)
            i = i+1
    while i < 18:
        with col3:
            st.write(f"<b>{recm[i]}</b>", unsafe_allow_html=True)
            st.text(f"IMBD RATING : {imbd[i]}/10")

            st.image(recp[i], width=200)
            i = i+1
