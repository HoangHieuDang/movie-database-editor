# Copy your code from the previous Movies project
import movie_storage as mvst
import sys
import re
from colorama import Fore, Back, Style

def menu_display():
  """
  displaying menu options
  """
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
  return menu_options_print

def menu_dispatcher():
    """
    Menu dispatcher to select functionalities
    """
    #Create a menu dispatcher dictionary
    menu_dispatch_dict = {
      "0": exit,
      "1": list_movies_handler,
      "2": add_movie_input_handler,
      "3": delete_movie_handler,
      "4": update_movie_handler,
      "5": stats_handler,
      "6": random_movie_handler,
      "7": search_movie_handler,
      "8": movies_sorted_by_rating_handler,
      "9": movie_sorted_by_year_handler,
      "10": filter_movies_handler,
      "11": rating_histogram_handler
    }
    #Handle user input for choosing the operation options
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
      else: break
    print(Style.RESET_ALL)
    #Invoke the chosen function from the dispatcher
    chosen_function = menu_dispatch_dict[str(user_input)]
    chosen_function()

def add_movie_input_handler():
    """
    Handles the task of adding a movie into the database
    """
    print(Fore.YELLOW + "\n---------------------------")
    print(Fore.YELLOW + "---  Add a movie title  ---")
    print(Fore.YELLOW + "---------------------------\n")
    input_title = input(Fore.GREEN + "Please enter the movie title:")
    while True:
      try: 
        input_rating = float(input(Fore.GREEN + "Please enter the rating:"))
        input_year = int(input(Fore.GREEN + "Please enter the year:"))
        if input_rating < 1 or input_rating > 10:
          raise ValueError (Fore.RED + "input_rating out of range [1,10]")
      except (TypeError, ValueError):
        print(Fore.RED + "Please enter a rating number between 1 to 10")
        print(Fore.RED + "Please enter a number for the year")
      except Exception as error_msg:
        print(Fore.RED + "Something is wrong!" + str(error_msg))
      else: break
    print(Fore.YELLOW)
    mvst.add_movie(input_title, input_year, input_rating)
    print(Fore.YELLOW + "---------------------------\n")
    print(Style.RESET_ALL)

def list_movies_handler():
    """
    handles the listing of all movies from database
    """
    print(Fore.YELLOW + "\n----------------------------")
    print(Fore.YELLOW + "---  List of all movies  ---")
    print(Fore.YELLOW + "----------------------------\n")
    print(mvst.list_movies())
    print(Fore.YELLOW + "----------------------------\n")
    print(Style.RESET_ALL)
def delete_movie_handler():
    """
    handles delete tasks of a movie from database
    """
    print(Fore.YELLOW + "\n------------------------")
    print(Fore.YELLOW + "---  Delete a movie  ---")
    print(Fore.YELLOW + "------------------------\n")
    input_title = input(Fore.GREEN + "Please enter the movie title you want to delete:")
    print(Fore.YELLOW)
    mvst.delete_movie(input_title)
    print(Fore.YELLOW + "------------------------\n")
    print(Style.RESET_ALL)
def update_movie_handler():
    """
    handles the update movie task
    """
    print(Fore.YELLOW + "\n------------------------")
    print(Fore.YELLOW + "---  Update a movie  ---")
    print(Fore.YELLOW + "------------------------\n")
    input_title = input(Fore.GREEN + "Please enter the title to update:")
    if mvst.is_title_in_database(input_title):
      while True:
          try:
            rating = float(input(Fore.GREEN + "Please enter a new rating [1,10]:"))
            if rating < 1 or rating > 10:
              raise ValueError (Fore.RED + "the input rating is out of range [0,10]")
          except Exception as error_msg:
            print(Fore.RED + "Something is wrong:" + str(error_msg))
          else: break 
      mvst.update_movie(input_title, rating)
    else: raise FileNotFoundError(Fore.RED + "The movie title doesn't exist in the database")
    print(Fore.YELLOW + "------------------------\n")
    print(Style.RESET_ALL)

def stats_handler():
    """
    displaying stats feature
    """
    print(Fore.YELLOW + "\n-------------------")
    print(Fore.YELLOW + "-----  Stats  -----")
    print(Fore.YELLOW + "-------------------\n")
    print(mvst.stats())
    print(Fore.YELLOW + "-------------------\n")
    print(Style.RESET_ALL)
def random_movie_handler():
    """
    Print a random movie from database
    """
    print(Fore.YELLOW + "\n----------------------")
    print(Fore.YELLOW + "---  Random movie  ---")
    print(Fore.YELLOW + "----------------------\n")
    print(mvst.random_movie())
    print(Fore.YELLOW + "----------------------\n")
    print(Style.RESET_ALL)
    
def search_movie_handler():
    """
    Handle search function with movie database
    """
    print(Fore.YELLOW + "\n------------------------")
    print(Fore.YELLOW + "---  Search a movie  ---")
    print(Fore.YELLOW + "------------------------\n")
    search_term = input(Fore.GREEN + "Enter part of movie name:")
    print(Fore.YELLOW)
    mvst.search_movie(search_term)
    print(Fore.YELLOW + "------------------------\n")
    print(Style.RESET_ALL)

def movies_sorted_by_rating_handler():
    """
    Handle sorting movies by rating in descending order
    """
    print(Fore.YELLOW + "\n---------------------------------")
    print(Fore.YELLOW + "---  Movies sorted by rating  ---")
    print(Fore.YELLOW + "---------------------------------\n")
    print(mvst.movies_sorted_by_rating())
    print(Fore.YELLOW + "-----------------------------------\n")
    print(Style.RESET_ALL)

def movie_sorted_by_year_handler():
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
          raise ValueError (Fore.RED + "Please only answer with either 'yes' or 'no'")
      except ValueError as e:
          print(Fore.RED + str(e))
      except Exception as e:
          print(Fore.RED + "Something is wrong!" + str(e))
      else: break
    print(Fore.YELLOW)
    print(mvst.movies_sorted_by_year(is_latest_first))
    print(Fore.YELLOW + "-----------------------------------\n")
    print(Style.RESET_ALL)

def filter_movies_handler():
    """
    Handle filtering movies according to users criterias 
    Handle the user inputs
    """
    print(Fore.YELLOW + "\n-----------------------")
    print(Fore.YELLOW + "---  Filter Movies  ---")
    print(Fore.YELLOW + "-----------------------\n")
    while True:
      try:
        min_rating = input(Fore.GREEN + "Enter Minimum rating (leave blank for no minimum rating): ")
        start_year = input(Fore.GREEN + "Enter start year (leave blank for no start year): ")
        end_year = input(Fore.GREEN + "Enter end year (leave blank for no end year): ")
        if start_year:
          start_year = int(start_year)
        if end_year:
          end_year = int(end_year)
        if min_rating:
          min_rating = round(float((min_rating)),1)
        if start_year and end_year and start_year > end_year:
          raise ValueError (Fore.RED + "Error! Start year can't be greater than end year")
      
      except TypeError as e:
          print(Fore.RED + "Please enter numbers only " + str(e))
      except ValueError as e:
          print(Fore.RED + "Please enter numbers only " + str(e))
      except Exception as e:
          print(Fore.RED + "Someting is wrong! Please try again with numbers only " + str(e))
      else: break
    print(Fore.YELLOW)
    print(mvst.filter_movies(min_rating,start_year,end_year))
    print(Fore.YELLOW + "-----------------------\n")
    print(Style.RESET_ALL)

def rating_histogram_handler():
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
      else: break
    save_file += ".png"
    print(Fore.YELLOW)
    mvst.rating_histogram(save_file)
    print(Fore.YELLOW + "--------------------------\n")
    print(Style.RESET_ALL)
    sys.exit(0)

def exit ():
    """
    exit the program
    """
    print(Fore.YELLOW + "\n-----------------------------")
    print(Fore.YELLOW + "---  Exiting the program  ---")
    print(Fore.YELLOW + "-----------------------------\n")
    print(Fore.YELLOW + "Goodbye! See you next time!\n\n")
    print(Style.RESET_ALL)
    sys.exit(0)
    
def main():
    """
    Main program
    """
    print(Fore.YELLOW + "\n***************************************")
    print(Fore.YELLOW + "***  Welcome to my movie database!  ***")
    print(Fore.YELLOW + "***************************************\n")
    while True:
      print(menu_display())
      menu_dispatcher()
      user_input = input(Fore.GREEN + "\n***  Press Enter to continue  ***\n")
      print(Style.RESET_ALL)

if __name__ == "__main__":
  main()

