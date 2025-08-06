import streamlit as st
import pickle
import requests
import gdown
import os

from io import BytesIO


# Loading pickled models using gdown
# -------------------------------
@st.cache_data(show_spinner=True)
def load_pkl_from_drive(file_id, filename):
    if not os.path.exists(filename):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, filename, quiet=False)
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Loading movies and similarity matrix from Google Drive
movies = load_pkl_from_drive("1eM8L5xNBu5FGINhdEMR71GxPmSGK2owC", "movies.pkl")
similarity = load_pkl_from_drive("12hrVN_NeqeMOHaYOueAgOlJrwqmr5cbj", "similarity.pkl")


# TMDb movie detail fetcher
# -------------------------------
def fetch_movie_details(movie_id):
    api_key = "755b5d711b4eb243a756e61906f05052"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    image_base_url = "https://image.tmdb.org/t/p/w500"
    fallback_url = "https://via.placeholder.com/500x750?text=No+Poster"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            overview = data.get('overview', 'No description available.')

            if poster_path and isinstance(poster_path, str) and poster_path.strip():
                poster_url = image_base_url + poster_path
            else:
                poster_url = fallback_url

            return poster_url, overview
        else:
            print(f"[WARNING] Error fetching movie details for ID {movie_id}. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Exception while fetching movie_id {movie_id}: {e}")

    return fallback_url, "No description available."


# Recommendation logic
# -------------------------------
def recommend(movie):
    print(f"[DEBUG] Selected movie: {movie}")
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        print("[ERROR] Movie not found in DataFrame.")
        return [], [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_descriptions = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        print(f"[DEBUG] Recommending movie ID: {movie_id}")
        poster, overview = fetch_movie_details(movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(poster)
        recommended_movie_descriptions.append(overview)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions



# Streamlit UI
# -------------------------------
st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
    st.session_state.posters = []
    st.session_state.descriptions = []

if st.button('Show Recommendation'):
    names, posters, descriptions = recommend(selected_movie)
    st.session_state.recommendations = names
    st.session_state.posters = posters
    st.session_state.descriptions = descriptions

if st.session_state.recommendations:
    st.subheader("📌 Top 5 Recommendations")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(st.session_state.recommendations[i])
            st.image(st.session_state.posters[i])


# Groq Summary Generation
# -------------------------------
st.subheader("🔍 Get More Info on Recommended Movie")

selected_index = st.selectbox(
    "Choose a recommended movie", 
    st.session_state.recommendations if st.session_state.recommendations else ["-- No movie selected --"]
)

# Loading Groq API key securely
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def generate_summary_with_groq(movie_title):
    prompt = f"""You are a movie expert.

Generate a short and engaging 3-4 line summary for the movie titled "{movie_title}".
Include the release year, lead actor, director, and what the movie is about.
Avoid making up fictional facts or content."""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a movie expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"[Groq Error] Status Code: {response.status_code} - {response.text}"
    except Exception as e:
        return f"[Exception] {e}"

if st.button("Generate Summary...") and selected_index and selected_index != "-- No movie selected --":
    with st.spinner("Generating Groq summary..."):
        summary_text = generate_summary_with_groq(selected_index)

    st.markdown(f"### 🎞️ {selected_index}")
    st.markdown(f"""
**Groq Generated Summary:**

{summary_text.replace("Directed by", "**Directed by**")
             .replace("starring", "**Starring**")
             .replace("Released in", "**Released in**")
             .replace("follows", "—")
             .replace("With its", "\n\n**With its**")
             .replace("Along the way", "\n\n**Along the way**")}""")
