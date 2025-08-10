import requests
import json
import time
import os               # to check files and there path
import pandas as pd


# Configuration for Scraping Data
API_KEY = '755b5d711b4eb243a756e61906f05052'  # API key Of TMDB
BASE_URL = 'https://api.themoviedb.org/3'

MOVIE_FILE = 'tmdb_movies.json'
LANGUAGE_FILE = 'tmdb_languages.json'
RATINGS_FILE = 'CineSage/Data Collection/ml-32m/ratings.csv'  #  real MovieCine rating data




# 1. Fetch TMDb language mappings 

def fetch_language_mapping():
    url = f"{BASE_URL}/configuration/languages"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    return {lang['iso_639_1']: lang['english_name'] for lang in response.json()}

if not os.path.exists(LANGUAGE_FILE):
    lang_map = fetch_language_mapping()
    with open(LANGUAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(lang_map, f, ensure_ascii=False, indent=2)
else:
    with open(LANGUAGE_FILE, 'r', encoding='utf-8') as f:
        lang_map = json.load(f)



# 2. Fetch genre mapping
def get_genre_mapping():
    url = f"{BASE_URL}/genre/movie/list"
    params = {'api_key': API_KEY, 'language': 'en-US'}
    response = requests.get(url, params=params)
    return {g['id']: g['name'] for g in response.json().get('genres', [])}

genre_map = get_genre_mapping()

# Fetch TMDb movie data
movie_dict = {}
years = range(2015, 2026)    # Scraping movies realeased between 1980 and 2025

for year in years:
    for page in range(1, 101):
        url = f"{BASE_URL}/discover/movie"
        params = {
            'api_key': API_KEY,
            'sort_by': 'popularity.desc',
            'primary_release_year': year,
            'page': page
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            break
        results = response.json().get('results', [])
        if not results:
            break

        for movie in results:
            if movie['id'] not in movie_dict:
                movie['genre_names'] = [genre_map.get(gid, 'Unknown') for gid in movie.get('genre_ids', [])]
                movie['original_language_full'] = lang_map.get(movie.get('original_language', ''), 'Unknown')
                movie_dict[movie['id']] = movie

        print(f"{year} Page {page} — Total Movies: {len(movie_dict)}")
        time.sleep(0.50)  # adding delay to stay within TMDb's rate limits


print("Scraping done Successfully....!")




# Loading existing movies if file exists
if os.path.exists(MOVIE_FILE):
    with open(MOVIE_FILE, 'r', encoding='utf-8') as f:
        try:
            existing_movies = json.load(f)
        except json.JSONDecodeError:
            existing_movies = []
else:
    existing_movies = []

# Combining existing + new without duplicates
existing_ids = {movie['id'] for movie in existing_movies}
new_movies = [movie for movie in movie_dict.values() if movie['id'] not in existing_ids]
combined_movies = existing_movies + new_movies

# Saves updated movie list
with open(MOVIE_FILE, 'w', encoding='utf-8') as f:
    json.dump(combined_movies, f, ensure_ascii=False, indent=2)

print("File saved Succesfully....!")


# Load MovieCine ratings
if not os.path.exists(RATINGS_FILE):
    raise FileNotFoundError("MovieCine ratings file not found!")

ratings_df = pd.read_csv(RATINGS_FILE)
print(f"Loaded {len(ratings_df)} ratings from MovieCine")

