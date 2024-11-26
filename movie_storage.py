import json
import random
import matplotlib.pyplot as plt
import numpy as np
from thefuzz import fuzz
from thefuzz import process
from colorama import Fore, Back, Style

def open_database():
    """
    open json database and return the pythonic data
    """
    try:
      with open("movie_database.json", "r") as fileobj:
        data = json.load(fileobj)
      return data
    except Exception as e:
      error_msg = Fore.RED + "Something went wrong when connecting to the database!\n" + str(e)
      return error_msg
      
def write_database(input_data):
    """
    write data into json database
    """
    with open("movie_database.json", "w") as fileobj:
      fileobj.write(json.dumps(input_data))
    
def is_title_in_database(title):
    """
    Check whether a movie title exists in the database
    """
    data = open_database()
    if title in data:
      return True
    else:
      return False

def list_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 
    """
    data = open_database()
    # list out the total of movies
    print_output = ""
    print_output += f"{len(data)} movies in total\n\n" 
    for movie in data:
      print_output += f"{movie} ({data[movie]['year']}): {data[movie]['rating']}\n"
    return print_output

def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    data = open_database()
    if title not in data:
      data[title] = {
                "rating": rating,
                "year": year
      }
      write_database(data)
      print(f"Movie {title} was added to the database")
    else: print("The title already exists in the database")
    

def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    data = open_database()
    if title in data:
      del data[title]
      write_database(data)
      print(f"The movie '{title}' was deleted from the database")
      return True
    else:
      raise FileNotFoundError (Fore.RED + "The movie doesn't exist in the database!")
      return False

def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    data = open_database()
    if title in data:
      data[title]["rating"] = rating
      write_database(data)
      print(f"the movie '{title}' was updated with the rating of {rating}")
    else:
      raise FileNotFoundError(Fore.RED + "The movie title doesn't exist in the database")
  
def stats():
    """
    Print statistics about the movies in the database:
    1) Average rating
    2) Median rating
    3) The best movie by rating
    4) The worst movie by rating
    """
    data = open_database()
    rating_list = [info["rating"] for title, info in data.items()]
    #calculate average rating
    avg_rating = round(sum(rating_list)/len(rating_list),1)
    #sort the rating list from lowest to highest
    sorted_rating_list = sorted(rating_list)
    #calculate median rating
    med_rating = 0
    if len(rating_list) % 2 == 0:
      med_sum = sorted_rating_list[len(sorted_rating_list)//2] + sorted_rating_list[len(sorted_rating_list)//2-1]
      med_rating = round(med_sum/2, 1)
    else:
      med_rating = sorted_rating_list[len(sorted_rating_list)//2]
    #The best movie
    best_rating = sorted_rating_list[-1]
    best_movies_list = [[title, info] for title, info in data.items() if info["rating"] == best_rating]
    #The worst movie
    worst_rating = sorted_rating_list[0]
    worst_movies_list = [[title, info] for title, info in data.items() if info["rating"] == worst_rating]
    #Displaying the result
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
    return display_str

def random_movie():
    data = open_database()
    film, info = random.choice(list(data.items()))
    movie_display = f"\n{film} ({info['year']}): rating: {info['rating']}\n"
    return movie_display

def search_movie(search_term):
    """
    Searching a movie and print out its name and rating
    Using fuzzy matching to improve the search engine
    """
    data = open_database()
    #calculate matching point between the search term and each item in the database
    result_print = process.extract(search_term, [film for film in data])
    #if it is not a 100% match
    if result_print[0][1] != 100:
      print(f"\nThe movie '{search_term}' doesn't exist")
    #if there is no match result point above 80
    #the question "did you mean" should not be printed
    #only print suggestions with the match point above 80
      print_question_flag = False
      for result in result_print:
        if result[1] >= 80:
          if not print_question_flag:
            print("Did you mean:")
            print_question_flag = True
          print(result[0])
    return result_print

def movies_sorted_by_rating():
    """
    Sort a movie according to its rating in descending order
    """
    data = open_database()
    movies_rating_list = sorted(data, key = lambda k: data[k]["rating"], reverse = True)
    result_print = ""
    for film in movies_rating_list:
      result_print += f"{film}, {data[film]['rating']}\n"
    return result_print

def movies_sorted_by_year(is_latest_first = True):
    """
    sort the move by year in 
    descending or ascending order 
    depending on the boolean argument
    """
    data = open_database()
    movies_rating_list = sorted(data, key = lambda k: data[k]["year"], reverse = is_latest_first)
    result_print = "\n"
    for film in movies_rating_list:
      result_print += f"{film}, {data[film]['year']}\n"
    return result_print

def filter_movies(min_rating, start_year, end_year):
    """
    Movie filter function with following possible criterias:
    Minimum rating, start year, end year
    Print out the filtered movies titles, release years and ratings
    """
    data = open_database()
    criteria = []
    
    if start_year and end_year and start_year > end_year:
      raise ValueError ("end year is not greater than start year!")
    if start_year:
      criteria.append(lambda x, y: x >= start_year) 
    if end_year:  
      criteria.append(lambda x, y: x <= end_year)
    if min_rating:
      criteria.append(lambda x, y: y >= min_rating)

    filtered_list = [film for film in data if all(crit(data[film]["year"], data[film]["rating"]) for crit in criteria)]
    result_print = "\nFiltered Movies:\n"
    for film in filtered_list:
      result_print += f"{film} ({data[film]['year']}): {data[film]['rating']}\n"
    return result_print

def rating_histogram(save_file):
    """
    create a histogram of the films ratings
    """
    # get data from database
    data = open_database()
    rating_list = [film["rating"] for film in data.values()]
    # Plotting a basic histogram
    plt.hist(rating_list, bins=30, color='skyblue', edgecolor='black', stacked = True, align = 'mid', histtype = 'bar')
    
    # Adding labels and title
    plt.xlabel('Film Ratings')
    plt.ylabel('Frequency')
    plt.title('Histogram of the film ratings')
    
    # Display the plot
    plt.tight_layout()
    plt.show()
    plt.savefig(save_file)
    print(f"The rating histogram was saved under {save_file}")