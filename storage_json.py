from istorage import IStorage
import json
from colorama import Fore, Back, Style


class StorageJson(IStorage):
    def __init__(self, file_path):
        try:
            if file_path.endswith(".json"):
                self._file_path = file_path
            else:
                raise Exception(".json file only!")
        except Exception as e:
            print("Can not create Json Storage: " + str(e))

    def list_movies(self):
        data = open_database(self._file_path)
        print_output = ""
        print_output += f"{len(data)} movies in total\n\n"
        for movie in data:
            print_output += f"{movie} ({data[movie]['year']}): {data[movie]['rating']}\n"
        return print_output

    def add_movie(self, title, year, rating):
        data = open_database(self._file_path)
        if title not in data:
            data[title] = {
                "rating": rating,
                "year": year
            }
            write_database(data, self._file_path)
            print(f"Movie {title} was added to the database")
        else:
            print("The title already exists in the database")

    def delete_movie(self, title):
        data = open_database(self._file_path)
        if title in data:
            del data[title]
            write_database(data, self._file_path)
            print(f"The movie '{title}' was deleted from the database")
            return True
        else:
            raise FileNotFoundError(Fore.RED + "The movie doesn't exist in the database!")
            return False

    def update_movie(self, title, rating):
        data = open_database(self._file_path)
        if title in data:
            data[title]["rating"] = rating
            write_database(data, self._file_path)
            print(f"the movie '{title}' was updated with the rating of {rating}")
        else:
            raise FileNotFoundError(Fore.RED + "The movie title doesn't exist in the database")


def open_database(file_path):
    """
    open json database and return the pythonic data
    """
    try:
        with open(file_path, "r") as fileobj:
            data = json.load(fileobj)
        return data
    except Exception as e:
        error_msg = Fore.RED + "Something went wrong when connecting to the database!\n" + str(e)
        return error_msg


def write_database(input_data, file_path):
    """
    write data into json database
    """
    with open(file_path, "w") as fileobj:
        fileobj.write(json.dumps(input_data))


"""
# ------------------------Sanity Test--------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
new_storage = StorageJson("movie_database.json")
print("__________list movies_______________")
print("____________________________________")
print(new_storage.list_movies())
print("__________add movies_______________")
print("____________________________________")
new_storage.add_movie("Long legs", 2023, 7.5)
print("__________list movies_______________")
print("____________________________________")
print(new_storage.list_movies())
print("__________delete movies_______________")
print("____________________________________")
new_storage.delete_movie("Long legs")
print("__________list movies_______________")
print("____________________________________")
print(new_storage.list_movies())
print("__________add movies_______________")
print("____________________________________")
new_storage.add_movie("PS I love you", year=2002, rating=0.5)
print("__________list movies_______________")
print("____________________________________")
print(new_storage.list_movies())
print("__________update movies_______________")
print("____________________________________")
print(new_storage.update_movie("PS I love you", 1.0))
print("__________list movies_______________")
print("____________________________________")
print(new_storage.list_movies())
"""