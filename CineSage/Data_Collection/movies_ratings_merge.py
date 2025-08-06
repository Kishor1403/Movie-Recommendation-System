import pandas as pd
import json

# File Paths
MOVIE_FILE = 'tmdb_movies.json'
RATINGS_FILE = 'CineSage/Data Collection/ml-32m/ratings.csv'
MERGED_FILE = 'merged_moviecine_tmdb.csv'

# 1 Loading TMDb Movies JSON
with open(MOVIE_FILE, 'r', encoding='utf-8') as f:
    tmdb_movies = json.load(f)

# Converting to DataFrame
movies_df = pd.DataFrame(tmdb_movies)

# Rename 'id' to 'movie_id' to match ratings
movies_df.rename(columns={'id': 'movie_id'}, inplace=True)

# Keeping only relevant columns
movies_df = movies_df[['movie_id', 'title', 'release_date', 'genre_names', 'original_language_full']]

print(f"Loaded {len(movies_df)} TMDb movies.")


# 2 Loading MovieCine Ratings CSV
ratings_df = pd.read_csv(RATINGS_FILE)

# Renameing column for merge compatibility
ratings_df.rename(columns={'movieId': 'movie_id', 'userId': 'user_id'}, inplace=True)

print(f"Loaded {len(ratings_df)} user ratings.")

# 3 Merging Ratings with Movie Metadata
merged_df = ratings_df.merge(movies_df, on='movie_id', how='inner')

# Droping rows without titles or ratings (if exists)
merged_df.dropna(subset=['title', 'rating'], inplace=True)

# 4 Save Merged Data
merged_df.to_csv(MERGED_FILE, index=False)

print(f"Final merged dataset saved: {MERGED_FILE}")
print(f"Rows: {len(merged_df)}, Users: {merged_df['user_id'].nunique()}, Movies: {merged_df['movie_id'].nunique()}")
