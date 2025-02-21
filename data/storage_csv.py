from data.istorage import IStorage
import csv
import os
from colorama import Fore

class StorageCsv(IStorage):
    """
    Class StorageCsv is a child class from IStorage
    which handles CRUD Operation on CSV database
    """
    def __init__(self, file_path):
        try:
            if not os.path.exists(file_path):
                if file_path.endswith(".csv"):
                    with open(file_path, 'x') as fileobj:
                        fileobj.close()
                else:
                    raise Exception("File name is not valid")
            if file_path.endswith(".csv") and os.path.exists(file_path):
                self._file_path = file_path
            else:
                raise Exception(".csv file only and make sure that the file exists in current directory!")
        except Exception as e:
            print("Can not create csv Storage: " + str(e))
    def list_movies(self):
        """
        List all movies from database
        """
        movies_dict = open_database(self._file_path)
        return movies_dict
    def add_movie(self, title, year, rating, poster_url):
        """
        Add a movie into database
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
    open csv database and return the dictionary structure {"Titanic": {"rating": 9.8, "year": 2001}}
    """
    try:
        with open(file_path, "r") as fileobj:
            data = csv.reader(fileobj)
            if data:
                movie_dict = dict()
                list_of_lines = []
                for lines in data:
                    list_of_lines.append(lines)
                for line in list_of_lines[1:]:
                    if line:
                        movie_dict[line[0]] = {"rating": line[1], "year": line[2], "poster_url": line[3]}
                return movie_dict
            else:
                raise Exception("csv file is empty")
    except Exception as e:
        print(Fore.RED + "Something went wrong when connecting to the database!\n" + str(e))
        return []
def write_database(input_data, file_path):
    """
    write data into csv database
    """
    list_data = []
    for data in input_data:
        list_data.append([data, input_data[data]["rating"], input_data[data]["year"], input_data[data]["poster_url"]])
    with open(file_path, "a", newline="") as fileobj:
        writer = csv.writer(fileobj)
        if os.path.getsize(file_path) == 0:
            writer.writerow(["title", "rating", "year", "poster_url"])
        writer.writerows(list_data)
