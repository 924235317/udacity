#coding:utf-8

import media
from fresh_tomatoes import open_movies_page
import json


def load_movie_file(movie_file_path):
    '''Load movies info from a txt'''

    movies_info_list = []
    #open the json file and load infomation
    try:
        with open(movie_file_path) as movies_file:
            movies_list = json.load(movies_file)
            for movie in movies_list:
                info = media.Movie(movie['name'],
                                   movie['poster_url'],
                                   movie['trail_url'])
                movies_info_list.append(info)
    #If the json file does not exist
    except IOError, e:
        print("[ERROR]: ", e)
    finally:
        return movies_info_list


if __name__ == '__main__':
    movie_list = load_movie_file("movies.json")
    open_movies_page(movie_list)
