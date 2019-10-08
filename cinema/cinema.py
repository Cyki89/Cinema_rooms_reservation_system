import random
from movie_database import Movie_database
from room import Room
from movie import Movie
from helpers import *

class Cinema:
    '''Main class for single cinema'''
    def __init__(self, name):
        self.name = name
        self.movie_database = Movie_database(name) # reference to cinema movie database
        self.list_of_rooms = []
        self.list_of_movies = [None]
        self.showing_time = ['15:00', '18:00', '21:00']

    def add_room(self, name, size):
        '''Method added new room to cinema'''
        try:
            int_row, int_col = parse_str_to_int(size[0]), parse_str_to_int(size[0])
            if int_row <= 0 or int_col <= 0:
                raise Exception(f'Both dimentions have to be grater than 0.\nRows: {int_row} Cols: {int_col}.')
        except Exception as e:
            print(f'Unsuccessfully added a new room {name} with size: {size} to {self.name} cinema. Details:\n{e}')
        else:
            self.list_of_rooms.append(Room(name, (int_row, int_col)))
            print(f'Successfully added a new room {name} with size: {size} to {self.name} cinema')

    def add_movie(self, name, time, room):
        '''Method added new movie to cinema'''
        if name in self.movie_database.list_of_movies and time in self.showing_time and room in self.list_of_rooms:
            self.list_of_movies.append(Movie(self, name, time, room))
        else:
            print(f'Movie {name} {room} {time} cannot be added to Cinema {self.name}')
            print('It dosent meet the cinema requirements')

    def movie_generator(self):
        '''Helper method to generate random movie in cinema'''
        for time in self.showing_time:
            for room in self.list_of_rooms:
                movie_name = random.choice(self.movie_database.list_of_movies)
                self.list_of_movies.append(Movie(self, movie_name, room, time))

    def allocation_seat_generator(self):
        '''Helper method to generate random clients and allocate theirs in cinema rooms'''
        for movie in self.list_of_movies:
            if movie is not None:
                for i in range (1,80):
                    client_name = f'Client {i}'
                    row, col = random.randint(1, movie.room.size[0]), random.randint(1, movie.room.size[1])
                    try:
                        movie.room.allocate_seat(client_name, row, col)
                    except Exception as e:
                        print(e)

    def show_schedule(self):
        '''Method shows daily movies schedule'''
        print('Today schedule:')
        print('-' * 50)
        for i, movie in enumerate(self.list_of_movies[1:], 1):
            print(f'Movie id {i} Time: {movie.time} Room: {movie.room.name} Title: {movie.name}')
        print('-' * 50)

    def select_movie(self, movie_id):
        '''Method select appropiate movie from passed movie_id'''
        try:
            int_movie_id = parse_str_to_int(movie_id)
        except ValueError as e:
            raise ValueError(e)
        if int_movie_id in range(1, len(self.list_of_movies)):
            return self.list_of_movies[int_movie_id]
        raise Exception(f'Movie with id {int_movie_id} not found...')