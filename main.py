from movie_app import MovieApp
from data.storage_json import StorageJson
from data.storage_csv import StorageCsv

if __name__ == "__main__":
    while True:
        storage = StorageJson('data/movie_database.json')
        #storage = StorageCsv('data/movie_storage.csv')
        movie_app = MovieApp(storage)
        movie_app.run()