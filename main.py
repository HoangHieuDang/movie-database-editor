from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

if __name__ == "__main__":
    while True:
        storage = StorageJson('movie_database.json')
        #storage = StorageCsv('movie_storage.csv')
        movie_app = MovieApp(storage)
        movie_app.run()