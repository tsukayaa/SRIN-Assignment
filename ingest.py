import pandas as pd
from sentence_transformers import SentenceTransformer
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

COLLECTION_NAME = "movies"

# 1. Connect ke Milvus (Docker)
connections.connect(
    "default",
    host="127.0.0.1",  # kalau gagal ganti ke "host.docker.internal"
    port="19530",
    timeout=60
)

# 2. Load dataset
movies = pd.read_csv("data/movies.csv")
movies["text"] = movies["title"] + " " + movies["genres"]

# 3. Generate embeddings
model = SentenceTransformer("intfloat/e5-base-v2")
embs = model.encode(movies["text"].tolist(), show_progress_bar=True)

# 4. Define schema (sekali saja)
if not utility.has_collection(COLLECTION_NAME):
    fields = [
        FieldSchema(name="movie_id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=embs.shape[1]),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="genres", dtype=DataType.VARCHAR, max_length=128)
    ]
    schema = CollectionSchema(fields, description="MovieLens movies collection")
    collection = Collection(COLLECTION_NAME, schema)
else:
    collection = Collection(COLLECTION_NAME)

# 5. Insert data
data = [
    movies["movieId"].tolist(),
    embs.tolist(),
    movies["title"].tolist(),
    movies["genres"].tolist()
]
collection.insert(data)
collection.flush()

print(f"✅ Inserted {collection.num_entities} records into `{COLLECTION_NAME}`.")
