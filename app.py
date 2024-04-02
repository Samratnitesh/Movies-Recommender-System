import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(
        movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movie_lists = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_lists:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://dnm.nflximg.net/api/v6/BvVbc2Wxr2w6QuoANoSpJKEIWjQ/AAAAQXjDuMwz8AyJ1m0WeGUEHUdVa8YdWS0-NozfIIL-tbz17rNRTQQ37iAJMPe2pTV8cuKVuvSDlBNMO9pSRg8NfIlCh57bwsNUMvg5KlQqvbRfxK5zbQi9kBvNu_U80J6gpRSYbINbBNodncF3N4Q6Rw0lN5k.jpg?r=0d6");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
# st.markdown(page_bg_img, unsafe_allow_html=True)
set_bg_hack_url()

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Which movie do you like best?',
movies['title'].values)

if st.button('Recommend'):
    names, poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])


