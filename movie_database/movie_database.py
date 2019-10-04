import os
import shutil

class Movie_database:
    ''' Class for storage movies available in single cinema'''
    def __init__(self, cinema):
        self.movie_database = os.path.join(os.getcwd(), 'data', f'{cinema}_movies.txt')
        self.create_movie_database()
        self.read_movies_from_disk()

    def create_movie_database(self):
        source_database = os.path.join(os.getcwd(), 'data', 'movies.txt')
        shutil.copy(source_database, self.movie_database)

    def read_movies_from_disk(self): # add try except
        self.list_of_movies = []
        with open(self.movie_database) as file_read:
            for movie in file_read:
                self.list_of_movies.append(movie.strip())

    def save_movies_to_disk(self): # add try except
        with open(self.movie_database, 'w') as file_write:
            for movie in self.list_of_movies:
                file_write.write(f'{movie}\n') # how remove last '\n' in pythonic way?

    def add_movie(self, movie):
        self.list_of_movies.append(movie)
        self.save_movies_to_disk()

    def delete_movie(self, movie):
        try:
            self.list_of_movies.remove(movie)
        except ValueError:
            print(f'Movie {movie} dont exist in cinema database' )
        else:
            self.save_movies_to_disk()