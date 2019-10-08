import os
import shutil
from helpers import *

@error_handling_class_decorator
class Movie_database:
    ''' Class for storage movies available in single cinema'''
    def __init__(self, cinema):
        self.movie_database = os.path.join(os.getcwd(), 'data', f'{cinema}_movies.txt') #reference to cinema movie txt file
        self.list_of_movies = []
        self.create_movie_database()
        self.read_movies_from_disk()

    def create_movie_database(self):
        '''Method copy list of movie from one txt file to another'''
        source_database = os.path.join(os.getcwd(), 'data', 'movies.txt')
        shutil.copy(source_database, self.movie_database)

    def read_movies_from_disk(self):
        '''Method read list of movie from .txt file and save it in instance field self.movie_of_list'''
        self.list_of_movies.clear()
        with open(self.movie_database) as file_read:
            for movie in file_read:
                self.list_of_movies.append(movie.strip())

    def save_movies_to_disk(self):
        '''Method save list of movie to .txt file'''
        with open(self.movie_database, 'w') as file_write:
            for movie in self.list_of_movies:
                file_write.write(f'{movie}\n') # how remove last '\n' in pythonic way?

    def add_movie(self, movie):
        '''Method add movie to the field list_of_movie and update txt file'''
        self.list_of_movies.append(movie)
        self.save_movies_to_disk()

    def delete_movie(self, movie):
        '''Method remove movie from the field list_of_movie and update txt file'''
        try:
            self.list_of_movies.remove(movie)
        except ValueError as e:
            print (f'Movie {movie} dont exist in cinema database' )
            raise Exception(e)
        else:
            self.save_movies_to_disk()

