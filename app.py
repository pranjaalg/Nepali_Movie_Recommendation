import os
import re
import pickle
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# -------------------------------------------------------------
# Configuration & Light Styling
# -------------------------------------------------------------
st.set_page_config(
    page_title="Nepali Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    .movie-title {
        font-size: 15px;
        font-weight: 600;
        color: #1a1a1a;
        text-align: center;
        margin-top: 10px;
        min-height: 40px;
    }
    .rating-text {
        text-align: center;
        font-size: 12px;
        color: #495057;
        margin-bottom: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TMDB & IMDb API Integration
# -------------------------------------------------------------
def clean_title(title):
    """Clean title by removing year in brackets and special symbols."""
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'[^a-zA-Z0-9\s]', ' ', title)
    return title.strip()

def get_imdb_rating(imdb_id):
    """Fetch IMDb rating from OMDb API using IMDb ID."""
    if not OMDB_API_KEY or not imdb_id:
        return "N/A"
    try:
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        res = requests.get(url, timeout=3).json()
        return res.get('imdbRating', 'N/A')
    except Exception:
        return "N/A"

def fetch_poster_and_details(movie_title):
    """Fetch poster image, TMDb rating, and IMDb rating."""
    if not TMDB_API_KEY:
        return "https://via.placeholder.com/500x750?text=API+Key+Missing", "N/A", "N/A"

    cleaned_title = clean_title(movie_title)
    queries = [cleaned_title, movie_title]
    
    for query in queries:
        if not query:
            continue
        try:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={requests.utils.quote(query)}"
            response = requests.get(url, timeout=5).json()
            
            results = response.get('results', [])
            if results:
                tmdb_id = results[0].get('id')
                tmdb_rating = str(round(results[0].get('vote_average', 0.0), 1))
                poster_path = results[0].get('poster_path')
                
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"

                # Fetch IMDb ID from TMDb external endpoints
                ext_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids?api_key={TMDB_API_KEY}"
                ext_res = requests.get(ext_url, timeout=3).json()
                imdb_id = ext_res.get('imdb_id')

                # Fetch real IMDb Rating
                imdb_rating = get_imdb_rating(imdb_id) if imdb_id else "N/A"

                return poster_url, tmdb_rating, imdb_rating
        except Exception:
            continue

    return "https://via.placeholder.com/500x750?text=Poster+Not+Found", "N/A", "N/A"

# -------------------------------------------------------------
# Model & Data Loader
# -------------------------------------------------------------
@st.cache_resource
def load_data():
    movies = pickle.load(open('nepali_movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

# -------------------------------------------------------------
# Recommendation Function
# -------------------------------------------------------------
def recommend(movie_title, top_n=5):
    try:
        idx = movies[movies['Title'] == movie_title].index[0]
        distances = similarity[idx]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:top_n+1]
        
        recommended_titles = []
        recommended_posters = []
        tmdb_ratings = []
        imdb_ratings = []
        
        for i in movie_list:
            title = movies.iloc[i[0]]['Title']
            poster, tmdb_r, imdb_r = fetch_poster_and_details(title)
            
            recommended_titles.append(title)
            recommended_posters.append(poster)
            tmdb_ratings.append(tmdb_r)
            imdb_ratings.append(imdb_r)
            
        return recommended_titles, recommended_posters, tmdb_ratings, imdb_ratings
    except IndexError:
        return [], [], [], []

# -------------------------------------------------------------
# Header & Input Section
# -------------------------------------------------------------
st.title("🎬 Nepali Movie Recommender")
st.write("Find similar Nepali movies using Content-Based Recommendation.")

selected_movie = st.selectbox(
    "Choose or type a movie name:",
    movies['Title'].values
)

if st.button("Get Recommendations 🚀", type="primary"):
    with st.spinner('Fetching recommendations, posters, and IMDb ratings...'):
        names, posters, tmdb_r, imdb_r = recommend(selected_movie)
        
        if names:
            st.markdown("### 🍿 Recommended Movies")
            cols = st.columns(5)
            
            for col, name, poster, t_rating, i_rating in zip(cols, names, posters, tmdb_r, imdb_r):
                with col:
                    st.image(poster, use_container_width=True)
                    st.markdown(f"<div class='movie-title'>{name}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='rating-text'>⭐ TMDb: {t_rating}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='rating-text'>🟡 IMDb: {i_rating}</div>", unsafe_allow_html=True)
        else:
            st.error("No recommendations found.")

st.divider()

with st.expander("📌 View Details of Selected Movie"):
    selected_info = movies[movies['Title'] == selected_movie].iloc[0]
    st.write(f"**Title:** {selected_info['Title']}")
    if 'Description' in selected_info:
        st.write(f"**Description:** {selected_info['Description']}")
    if 'Tags' in selected_info:
        st.write(f"**Tags:** {selected_info['Tags']}")