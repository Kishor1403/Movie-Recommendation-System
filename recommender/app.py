import pickle
import streamlit as st
import requests
from langchain_ollama import ChatOllama

# Initialize LLaMA 3.2
llama = ChatOllama(model='llama3.2')

# TMDb movie detail fetcher
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
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_descriptions = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, overview = fetch_movie_details(movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(poster)
        recommended_movie_descriptions.append(overview)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions

# Load data once
movies = pickle.load(open('D:/Movie_Recommendation_1.1/recommender/movies_list.pkl', 'rb'))
similarity = pickle.load(open('D:/Movie_Recommendation_1.1/recommender/similarity.pkl', 'rb'))

st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Initialize session state to hold recommendations
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
    st.session_state.posters = []
    st.session_state.descriptions = []

# Show Recommendations button
if st.button('Show Recommendation'):
    names, posters, descriptions = recommend(selected_movie)
    st.session_state.recommendations = names
    st.session_state.posters = posters
    st.session_state.descriptions = descriptions

# Display recommended posters and titles (if available)
if st.session_state.recommendations:
    st.subheader("📌 Top 5 Recommendations")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(st.session_state.recommendations[i])
            st.image(st.session_state.posters[i])

# Select a movie to summarize
st.subheader("🔍 Get More Info on Recommended Movie")

selected_index = st.selectbox(
    "Choose a recommended movie", 
    st.session_state.recommendations if st.session_state.recommendations else ["-- No movie selected --"]
)

if st.button("Generate Summary...") and selected_index and selected_index != "-- No movie selected --":
    prompt = f"""You are a movie expert.

Generate a short and engaging 3-4 line summary for the movie titled "{selected_index}".
Include the release year, lead actor, director, and what the movie is about.
Avoid making up fictional facts or content."""

    with st.spinner("Generating LLaMA 3.2 summary..."):
        llm_response = llama.invoke(prompt)

        st.markdown(f"### 🎞️ {selected_index}")
    
    summary_text = llm_response.content if hasattr(llm_response, 'content') else str(llm_response)

    st.markdown(f"""
**LLaMA 3.2 Generated Summary:**

{summary_text.replace("Directed by", "**Directed by**")
             .replace("starring", "**Starring**")
             .replace("Released in", "**Released in**")
             .replace("follows", "—")
             .replace("With its", "\n\n**With its**")
             .replace("Along the way", "\n\n**Along the way**")}
    """)
