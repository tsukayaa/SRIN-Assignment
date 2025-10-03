import pandas as pd

# Load movies
movies = pd.read_csv("data/movies.dat", sep="::", engine="python", 
                     names=["movieId", "title", "genres"], encoding="latin-1")
movies.to_csv("data/movies.csv", index=False)

# Load ratings
ratings = pd.read_csv("data/ratings.dat", sep="::", engine="python", 
                      names=["userId", "movieId", "rating", "timestamp"], encoding="latin-1")
ratings.to_csv("data/ratings.csv", index=False)

# Load users
users = pd.read_csv("data/users.dat", sep="::", engine="python", 
                    names=["userId", "gender", "age", "occupation", "zip"], encoding="latin-1")
users.to_csv("data/users.csv", index=False)

print("✅ Conversion done: movies.csv, ratings.csv, users.csv created.")
