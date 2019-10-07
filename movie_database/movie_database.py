import os
import shutil

class Movie_database:
    ''' Class for storage movies available in single cinema'''
    def __init__(self, cinema):
        self.movie_database = os.path.join(os.getcwd(), 'data', f'{cinema}_movies.txt')
        self.create_movie_database()
        self.read_movies_from_disk()

    # TODO add try except
    def create_movie_database(self):
        '''Method create cinema_movie_database from list of movie in .txt file'''
        source_database = os.path.join(os.getcwd(), 'data', 'movies.txt')
        shutil.copy(source_database, self.movie_database)

    # TODO add try except
    def read_movies_from_disk(self):
        '''Method read list of movie from .txt file and save it in instance field self.movie_of_list'''
        self.list_of_movies = [] # Relocate it to init?
        with open(self.movie_database) as file_read:
            for movie in file_read:
                self.list_of_movies.append(movie.strip())

    # TODO add try except
    def save_movies_to_disk(self):
        '''Method save list of movie to .txt file'''
        with open(self.movie_database, 'w') as file_write:
            for movie in self.list_of_movies:
                file_write.write(f'{movie}\n') # how remove last '\n' in pythonic way?

    # TODO add try except
    def add_movie(self, movie):
        '''Method add movie to the field list_of_movie and update txt file'''
        self.list_of_movies.append(movie)
        self.save_movies_to_disk()

    # TODO add try except
    def delete_movie(self, movie):
        '''Method remove movie from the field list_of_movie and update txt file'''
        try:
            self.list_of_movies.remove(movie)
        except ValueError:
            print(f'Movie {movie} dont exist in cinema database' )
        else:
            self.save_movies_to_disk()