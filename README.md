# 🎬 Movie Recommendation System

## Overview

This project is a **hybrid movie recommendation system** that combines **Content-Based Filtering** and **Neural Collaborative Filtering** to deliver personalized movie recommendations. The system also integrates **Meta’s LLaMA 3.2** (a Large Language Model) to generate short summaries of the recommended movies, enhancing user experience with contextual insights.

---

## Output Snippets 
<img width="974" height="651" alt="Screenshot 2025-07-30 201616" src="https://github.com/user-attachments/assets/93894e5b-1dd8-4d51-a1fb-ef42d13e940c" />

<img width="979" height="377" alt="Screenshot 2025-07-30 201632" src="https://github.com/user-attachments/assets/7acc99ac-77a4-499a-b5b2-35f8e8b3d038" />


## Note: Some Movie poster not loaded because sometimes tmdb api not responding

<img width="962" height="721" alt="Screenshot 2025-07-30 201324" src="https://github.com/user-attachments/assets/ffd9c021-f60f-4255-9dad-1c2509556c11" />

## Key Features

- 🔍 **Data Collection via TMDb API**  
  Movie metadata is scraped using TMDb's official API, including movie titles, genres, overviews, poster paths, and unique IDs.

- 📊 **Exploratory Data Analysis (EDA)**  
  Performed thorough EDA to clean, transform, and understand the dataset using visualizations and descriptive statistics.

- 🧹 **Data Cleaning & Preparation**  
  Removed missing values, merged metadata with ratings data, extracted key features like genres, tags, and processed them for modeling.

- 🧠 **Content-Based Filtering using TF-IDF**  
  Utilized the TF-IDF model and cosine similarity to recommend movies based on shared textual features such as genres, keywords, and overviews.

- 🤖 **Neural Collaborative Filtering (NCF)**  
  Implemented a deep learning-based recommendation model combining **Generalized Matrix Factorization (GMF)** and **Multi-Layer Perceptron (MLP)** to learn user-item interaction patterns.

- 🧠 **LLM Integration (LLaMA 3.2)**  
  Integrated **Meta’s LLaMA 3.2 model** to automatically generate short and relevant descriptions for the recommended movies.

- 📦 **Streamlit Interface**  
  Built a clean and interactive UI using Streamlit that allows users to select a movie and view recommendations with posters and brief LLM-generated summaries.

---

## Tech Stack

- **Language:** Python 3.x  
- **Libraries:** pandas, numpy, sklearn, keras, tensorflow, streamlit, requests  
- **API Source:** [TMDb API](https://developers.themoviedb.org/)  
- **LLM Integration:** Meta LLaMA 3.2 (local inference or API wrapped)  
- **Text Modeling:**TF-IDF + Cosine Similarity  
- **Visualization & EDA:** matplotlib, seaborn  
- **Deployment:** Streamlit App (local or cloud)

---



