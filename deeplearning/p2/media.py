#coding:utf-8
import webbrowser


class Movie():
    '''A class stores messages of a movie, \
       like title, poster image and trail url'''

    def __init__(self, move_tile,
                 poster_image, trailer_youku):
        '''init the Move instance, and value the \
           instance variables'''
        self.title = move_tile
        self.poster_image_url = poster_image
        self. trailer_url = trailer_youku

    def show_trailer(self):
        '''show the movie's trailer'''
        webbrowser.open(self.trailer_url)
