from data.istorage import IStorage
import json
import os
from colorama import Fore


class StorageJson(IStorage):
    """
    Class StorageJson is a child class from IStorage
    which handles CRUD Operation on JSON database
    """
    def __init__(self, file_path):
        try:
            if not os.path.exists(file_path):
                if file_path.endswith(".json"):
                    with open(file_path, 'x') as fileobj:
                        fileobj.close()
                else:
                    raise Exception("File name is not valid")

            if file_path.endswith(".json") and os.path.exists(file_path):
                self._file_path = file_path
            else:
                raise Exception(".json file only and make sure that the file exists in current directory!")
        except Exception as e:
            print("Can not create Json Storage: " + str(e))

    def list_movies(self):
        """
        list all movies from database
        """
        movies_dict = open_database(self._file_path)
        return movies_dict

    def add_movie(self, title, year, rating, poster_url):
        """
        add movies into database
        """
        data = open_database(self._file_path)
        if title not in data:
            data[title] = {
                "rating": rating,
                "year": year,
                "poster_url": poster_url
            }
            write_database(data, self._file_path)
            print(f"Movie {title} was added to the database")
        else:
            print("The title already exists in the database")

    def delete_movie(self, title):
        """
        delete a movie from database
        """
        data = open_database(self._file_path)
        if title in data:
            del data[title]
            write_database(data, self._file_path)
            print(f"The movie '{title}' was deleted from the database")
            return True
        else:
            print(Fore.RED + "The movie doesn't exist in the database!")
            return False


    def update_movie(self, title, rating):
        """
        Update the movie information
        """
        data = open_database(self._file_path)
        if title in data:
            data[title]["rating"] = rating
            write_database(data, self._file_path)
            print(f"the movie '{title}' was updated with the rating of {rating}")
        else:
            print(Fore.RED + "The movie title doesn't exist in the database")


def open_database(file_path):
    """
    open json database and return the pythonic data
    """
    try:
        with open(file_path, "r") as fileobj:
            data = json.load(fileobj)
            if data:
                return data
            else:
                return {}
    except FileNotFoundError:
        print(Fore.RED + f"Error: Database file '{file_path}' not found.")
        return {}  # Return an empty dictionary if the file is not found
    except json.JSONDecodeError:
        print(Fore.RED + f"Error: Database file '{file_path}' contains invalid JSON.")
        return {}  # Return an empty dictionary if JSON is invalid
    except Exception as e:
        print(Fore.RED + "Something went wrong when connecting to the database!\n" + str(e))
        return {}  # Return empty dictionary for any other unexpected errors


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
