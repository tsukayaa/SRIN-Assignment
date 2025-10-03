from pymilvus import connections, Collection

connections.connect("default", host="127.0.0.1", port="19530")
movies = Collection("movies")
print(movies.num_entities)