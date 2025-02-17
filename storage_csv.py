from istorage import IStorage
import csv
import os
from colorama import Fore

class StorageCsv(IStorage):
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
        movies_dict = open_database(self._file_path)
        return movies_dict

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
            raise FileNotFoundError(Fore.RED + "The movie title doesn't exist in the database")


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
                    if line and len(line) == 3:
                        movie_dict[line[0]] = {"rating":line[1],"year":line[2]}
                return movie_dict
            else:
                raise Exception("csv file is empty")
    except Exception as e:
        error_msg = Fore.RED + "Something went wrong when connecting to the database!\n" + str(e)
        return error_msg

def write_database(input_data, file_path):
    """
    write data into csv database
    """
    list_data = [
        ['Movie', 'Rating', 'Year']
    ]
    for data in input_data:
        list_data.append([data, input_data[data]["rating"], input_data[data]["year"]])
    with open(file_path, "w") as fileobj:
        writer = csv.writer(fileobj)
        writer.writerows(list_data)
