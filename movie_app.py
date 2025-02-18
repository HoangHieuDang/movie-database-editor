from colorama import Fore, Style
import random
from thefuzz import process
import re
import sys
import os
import matplotlib.pyplot as plt
from storage_json import StorageJson
from storage_csv import StorageCsv
import requests
from dotenv import load_dotenv

#loading environment variables
load_dotenv()
OMDB_KEY = os.getenv('OMDB_API_KEY')
"""
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Generate website
"""


class MovieApp:
    def __init__(self, storage):
        if isinstance(storage, StorageJson) or isinstance(storage, StorageCsv):
            self._storage = storage
        else:
            raise Exception("Can not init movie app object!")

    def _command_list_movies(self):
        """
        handles the listing of all movies from database
        """
        print(Fore.YELLOW + "\n----------------------------")
        print(Fore.YELLOW + "---  List of all movies  ---")
        print(Fore.YELLOW + "----------------------------\n")
        data = self._storage.list_movies()
        print_output = ""
        print_output += f"{len(data)} movies in total\n\n"
        for movie in data:
            print_output += f"{movie} ({data[movie]['year']}): {data[movie]['rating']}\n"
        print(print_output)
        print(Fore.YELLOW + "----------------------------\n")
        print(Style.RESET_ALL)

    def _command_add_movie(self):
        """
        Handles the task of adding a movie into the database
        Getting the movie from OMDB API and add the movie to the database
        """
        print(Fore.YELLOW + "\n---------------------------")
        print(Fore.YELLOW + "---  Add a movie title  ---")
        print(Fore.YELLOW + "---------------------------\n")

        input_title = input(Fore.GREEN + "Please enter the movie title:")
        REQUEST_URL = f"https://www.omdbapi.com/?apikey={OMDB_KEY}&t={input_title}"
        try:
            response = requests.get(REQUEST_URL)
        except Exception as e:
            print("Connection to OMDB API failed!" + str(e))
        else:
            res_dict = response.json()
            if 'Error' in res_dict.keys():
                print("Error message:" + str(res_dict['Error']))
            else:
                input_title = str(res_dict["Title"])
                input_year = str(res_dict["Year"])
                input_rating = str(res_dict["imdbRating"])
                input_poster_url = str(res_dict["Poster"])
        print(Fore.YELLOW)
        self._storage.add_movie(input_title, input_year, input_rating, input_poster_url)
        print(Fore.YELLOW + "---------------------------\n")
        print(Style.RESET_ALL)

    def _command_delete_movie(self):
        """
        handles delete tasks of a movie from database
        """
        print(Fore.YELLOW + "\n------------------------")
        print(Fore.YELLOW + "---  Delete a movie  ---")
        print(Fore.YELLOW + "------------------------\n")
        input_title = input(Fore.GREEN + "Please enter the movie title you want to delete:")
        print(Fore.YELLOW)
        self._storage.delete_movie(input_title)
        print(Fore.YELLOW + "------------------------\n")
        print(Style.RESET_ALL)

    def _command_update_movie(self):
        """
        handles the update movie task
        """
        print(Fore.YELLOW + "\n------------------------")
        print(Fore.YELLOW + "---  Update a movie  ---")
        print(Fore.YELLOW + "------------------------\n")
        input_title = input(Fore.GREEN + "Please enter the title to update:")
        """
        Check whether a movie title exists in the database
        """
        data = self._storage.list_movies()
        if input_title in data:
            while True:
                try:
                    rating = float(input(Fore.GREEN + "Please enter a new rating [1,10]:"))
                    if rating < 1 or rating > 10:
                        raise ValueError(Fore.RED + "the input rating is out of range [0,10]")
                except Exception as error_msg:
                    print(Fore.RED + "Something is wrong:" + str(error_msg))
                else:
                    break
            self._storage.update_movie(input_title, rating)
        else:
            raise FileNotFoundError(Fore.RED + "The movie title doesn't exist in the database")
        print(Fore.YELLOW + "------------------------\n")
        print(Style.RESET_ALL)

    def _command_movie_stats(self):
        """
        displaying stats feature
        """
        print(Fore.YELLOW + "\n-------------------")
        print(Fore.YELLOW + "-----  Stats  -----")
        print(Fore.YELLOW + "-------------------\n")
        """
        Print statistics about the movies in the database:
        1) Average rating
        2) Median rating
        3) The best movie by rating
        4) The worst movie by rating
        """
        data = self._storage.list_movies()
        rating_list = [info["rating"] for title, info in data.items()]
        # calculate average rating
        avg_rating = round(sum(rating_list) / len(rating_list), 1)
        # sort the rating list from lowest to highest
        sorted_rating_list = sorted(rating_list)
        # calculate median rating
        med_rating = 0
        if len(rating_list) % 2 == 0:
            med_sum = sorted_rating_list[len(sorted_rating_list) // 2] + sorted_rating_list[
                len(sorted_rating_list) // 2 - 1]
            med_rating = round(med_sum / 2, 1)
        else:
            med_rating = sorted_rating_list[len(sorted_rating_list) // 2]
        # The best movie
        best_rating = sorted_rating_list[-1]
        best_movies_list = [[title, info] for title, info in data.items() if info["rating"] == best_rating]
        # The worst movie
        worst_rating = sorted_rating_list[0]
        worst_movies_list = [[title, info] for title, info in data.items() if info["rating"] == worst_rating]
        # Displaying the result
        display_str = ""
        display_str += f"Average rating: {avg_rating}\n"
        display_str += f"Median rating: {med_rating}\n"
        display_str += f"\n<-----Best movies list----->\n"
        for k in best_movies_list:
            display_str += f" {k[0]}:\n   year: {k[1]['year']}\n   rating: {k[1]['rating']}\n"
        display_str += f"<-------------------------->\n"
        display_str += f"\n<-----Worst movies list---->\n"
        for k in worst_movies_list:
            display_str += f" {k[0]}:\n   year: {k[1]['year']}\n   rating: {k[1]['rating']}\n"
        display_str += f"<-------------------------->\n"
        print(display_str)
        print(Fore.YELLOW + "-------------------\n")
        print(Style.RESET_ALL)

    def _command_random_movie(self):
        """
        Print a random movie from database
        """
        print(Fore.YELLOW + "\n----------------------")
        print(Fore.YELLOW + "---  Random movie  ---")
        print(Fore.YELLOW + "----------------------\n")
        data = self._storage.list_movies()
        film, info = random.choice(list(data.items()))
        movie_display = f"\n{film} ({info['year']}): rating: {info['rating']}\n"
        print(movie_display)
        print(Fore.YELLOW + "----------------------\n")
        print(Style.RESET_ALL)

    def _command_search_movie(self):
        """
        Searching a movie and print out its name and rating
        Using fuzzy matching to improve the search engine
        """
        print(Fore.YELLOW + "\n------------------------")
        print(Fore.YELLOW + "---  Search a movie  ---")
        print(Fore.YELLOW + "------------------------\n")
        search_term = input(Fore.GREEN + "Enter part of movie name:")
        print(Fore.YELLOW)
        data = self._storage.list_movies()
        # calculate matching point between the search term and each item in the database
        result_print = process.extract(search_term, [film for film in data])
        # if it is not a 100% match
        if result_print[0][1] != 100:
            print(f"\nThe movie '{search_term}' doesn't exist")
            # if there is no match result point above 80
            # the question "did you mean" should not be printed
            # only print suggestions with the match point above 80
            print_question_flag = False
            for result in result_print:
                if result[1] >= 80:
                    if not print_question_flag:
                        print("Did you mean:")
                        print_question_flag = True
                    print(result[0])
        print(result_print)
        print(Fore.YELLOW + "------------------------\n")
        print(Style.RESET_ALL)

    def _command_sort_movies_by_rating(self):
        """
        Sort a movie according to its rating in descending order
        """
        print(Fore.YELLOW + "\n---------------------------------")
        print(Fore.YELLOW + "---  Movies sorted by rating  ---")
        print(Fore.YELLOW + "---------------------------------\n")
        data = self._storage.list_movies()
        movies_rating_list = sorted(data, key=lambda k: data[k]["rating"], reverse=True)
        result_print = ""
        for film in movies_rating_list:
            result_print += f"{film}, {data[film]['rating']}\n"
        print(result_print)
        print(Fore.YELLOW + "-----------------------------------\n")
        print(Style.RESET_ALL)

    def _command_movie_sorted_by_year(self):
        """
        Handle sorting movies by year in descending order
        """
        print(Fore.YELLOW + "\n---------------------------------")
        print(Fore.YELLOW + "---  Movies sorted by year  ---")
        print(Fore.YELLOW + "---------------------------------\n")
        while True:
            try:
                user_input = input(Fore.GREEN + "Do you want to watch the latest movies first? (Yes or No)\n")
                if user_input.lower() == "yes":
                    is_latest_first = True
                elif user_input.lower() == "no":
                    is_latest_first = False
                else:
                    raise ValueError(Fore.RED + "Please only answer with either 'yes' or 'no'")
            except ValueError as e:
                print(Fore.RED + str(e))
            except Exception as e:
                print(Fore.RED + "Something is wrong!" + str(e))
            else:
                break
        """
        sort the move by year in
        descending or ascending order
        depending on the boolean argument
        """
        data = self._storage.list_movies()
        movies_rating_list = sorted(data, key=lambda k: data[k]["year"], reverse=is_latest_first)
        result_print = "\n"
        for film in movies_rating_list:
            result_print += f"{film}, {data[film]['year']}\n"
        print(result_print)
        print(Fore.YELLOW + "-----------------------------------\n")
        print(Style.RESET_ALL)

    def _command_filter_movie(self):
        """
           Handle sorting movies by year in descending order
           """
        print(Fore.YELLOW + "\n---------------------------------")
        print(Fore.YELLOW + "---  Movies sorted by year  ---")
        print(Fore.YELLOW + "---------------------------------\n")
        while True:
            try:
                user_input = input(Fore.GREEN + "Do you want to watch the latest movies first? (Yes or No)\n")
                if user_input.lower() == "yes":
                    is_latest_first = True
                elif user_input.lower() == "no":
                    is_latest_first = False
                else:
                    raise ValueError(Fore.RED + "Please only answer with either 'yes' or 'no'")
            except ValueError as e:
                print(Fore.RED + str(e))
            except Exception as e:
                print(Fore.RED + "Something is wrong!" + str(e))
            else:
                break
        print(Fore.YELLOW)
        # sort the move by year in
        # descending or ascending order
        # depending on the boolean argument
        data = self._storage.list_movies()
        movies_rating_list = sorted(data, key=lambda k: data[k]["year"], reverse=is_latest_first)
        result_print = "\n"
        for film in movies_rating_list:
            result_print += f"{film}, {data[film]['year']}\n"
        print(result_print)
        print(Fore.YELLOW + "-----------------------------------\n")
        print(Style.RESET_ALL)

    def _command_rating_histogram(self):
        """
        handling rating_histogram user input and display
        """
        print(Fore.YELLOW + "\n--------------------------")
        print(Fore.YELLOW + "---  Rating histogram  ---")
        print(Fore.YELLOW + "--------------------------\n")
        # Make sure that user only inputs names with underscores without any other special characters
        while True:
            try:
                regexp = re.compile('[^0-9a-zA-Z_]+')
                save_file = input(Fore.GREEN + "Enter a file name to save the histogram: ")
                if regexp.search(save_file):
                    raise Exception(Fore.RED + "Sorry, no special characters other than underscores and strings")
            except Exception as e:
                print(Fore.RED + str(e))
            else:
                break
        save_file += ".png"
        print(Fore.YELLOW)
        # create a histogram of the films ratings
        # get data from database

        data = self._storage.list_movies()
        rating_list = [film["rating"] for film in data.values()]

        # Plotting a basic histogram
        plt.hist(rating_list, bins=30, color='skyblue', edgecolor='black', stacked=True, align='mid', histtype='bar')

        # Adding labels and title
        plt.xlabel('Film Ratings')
        plt.ylabel('Frequency')
        plt.title('Histogram of the film ratings')

        # Display the plot
        plt.tight_layout()
        plt.show()
        plt.savefig(save_file)

        print(f"The rating histogram was saved under {save_file}")
        print(Fore.YELLOW + "--------------------------\n")
        print(Style.RESET_ALL)
        sys.exit(0)

    def _generate_website(self):
        pass

    def run(self):
        """
        displaying menu options
        Handling User Input for the menu option
        call the chosen function
        """
        # Print menu
        menu_options_print = Fore.CYAN + '''
         0. Exit
         1. List movies
         2. Add movie
         3. Delete movie
         4. Update movie
         5. Stats
         6. Random movie
         7. Search movie
         8. Movies sorted by rating
         9. Movies sorted by year
         10. Filter movies
         11. Create Rating Histogram\n'''
        print(menu_options_print)

        # Create a menu dispatcher dictionary

        menu_dispatch_dict = {
            "0": exit,
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_movie_stats,
            "6": self._command_random_movie,
            "7": self._command_search_movie,
            "8": self._command_sort_movies_by_rating,
            "9": self._command_movie_sorted_by_year,
            "10": self._command_filter_movie,
            "11": self._command_rating_histogram
        }
        # Get use command
        # Handle user input for choosing the operation options
        while True:
            try:
                user_input = int(input(Fore.GREEN + "Please choose an option by entering a number between 0 to 11: "))
                if user_input < 0 or user_input > 11:
                    raise ValueError(Fore.RED + "The number must be in range of [0,11]")
            except ValueError as error_msg:
                print(Fore.RED + str(error_msg))
                print(Style.RESET_ALL)
            except Exception as error_msg:
                print(Fore.RED + "Error: " + str(error_msg))
                print(Style.RESET_ALL)
            else:
                break
        print(Style.RESET_ALL)
        # Invoke the chosen function from the dispatcher
        # Execute command
        chosen_function = menu_dispatch_dict[str(user_input)]
        chosen_function()
