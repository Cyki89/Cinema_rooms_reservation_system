import os
import unittest

import cinema
from movie import Movie
from movie_database import Movie_database
from room import Room

CINEMA_NAME = 'TestCinema'
CINEMA_PATH = f'./data/{CINEMA_NAME}_movies.txt'
ROOM_NAME = 'TestRoom'
ROOM_SIZE = (10, 10)
REALY_MOVIE = 'Planes'


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''create instance of Movie class '''
        cls.cinema = cinema.Cinema(CINEMA_NAME)

    @classmethod
    def tearDownClass(cls):
        ''' delete movie file at the end of testing session'''
        if os.path.exists(CINEMA_PATH):
            os.remove(CINEMA_PATH)

    def pre_test(self):
        ''' setUp method for some tests '''

        # add one example room to cinema
        self.cinema.add_room(ROOM_NAME, ROOM_SIZE)

        # add some movie to cinema
        self.cinema.movie_generator()

    def post_test(self):
        ''' teraDown method for some tests '''

        # clear list of rooms and movies
        self.cinema.list_of_rooms = []
        self.cinema.list_of_movies = [None]

    def test_create_instance(self):
        ''' check if instance was correctly created '''
        self.assertEqual(self.cinema.name, CINEMA_NAME)
        self.assertIsInstance(self.cinema.movie_database, Movie_database)
        self.assertEqual(self.cinema.list_of_rooms, [])
        self.assertEqual(self.cinema.list_of_movies, [None] )
        self.assertEqual(self.cinema.showing_time, ['15:00', '18:00', '21:00'])

    def test_add_room(self):
        ''' test 3 edge cases for add_room method '''

        # test casses for wrong inputs
        sizes = [ ('10.0', '10'), # not convertible string to int
                   ('0', '10') # num of rows can't be 0
        ]

        # test 2 wrong inputs in a loop
        for size in sizes:
            with self.assertRaises(Exception):
                self.cinema.add_room(ROOM_NAME, size)

        # test correct case
        self.cinema.add_room(ROOM_NAME, ROOM_SIZE)
        self.assertIsInstance(self.cinema.list_of_rooms[-1], Room)
        self.assertEqual(self.cinema.list_of_rooms[-1].name, ROOM_NAME)
        self.assertEqual(self.cinema.list_of_rooms[-1].size, ROOM_SIZE)

        # run tearDown method
        self.post_test()

    def test_add_movie(self):
        ''' test 4 edge cases for add_movie method '''

        # run SetUp method
        self.pre_test()

        # test 3 cases for wrong inputs
        inputs = [
            ('WrongMovie', self.cinema.showing_time[0], self.cinema.list_of_rooms[-1]), # wrong movie
            (REALY_MOVIE, self.cinema.showing_time[0], 'WrongRoom'),  # wrong room object
            (REALY_MOVIE, '16:00', self.cinema.list_of_rooms[-1]) # wrong time
        ]

        # test 3 wrong inputs in a loop
        for input in inputs:
            with self.assertRaises(Exception):
                self.cinema.add_movie(input)

        # correct input
        input = (REALY_MOVIE, self.cinema.showing_time[0], self.cinema.list_of_rooms[-1])
        self.cinema.add_movie(*input)
        self.assertIsInstance(self.cinema.list_of_movies[-1], Movie)
        self.assertEqual(self.cinema.list_of_movies[-1].cinema, self.cinema)
        self.assertEqual(self.cinema.list_of_movies[-1].name, REALY_MOVIE)
        self.assertIsInstance(self.cinema.list_of_movies[-1].room, Room)
        self.assertEqual(self.cinema.list_of_movies[-1].time, self.cinema.showing_time[0])

        # run tearDown method
        self.post_test()

    def test_movie_generator(self):
        ''' test for movie generator method'''

        # movie generator method is running in pretest method
        self.pre_test()

        # check len of list of generated movie
        self.assertEqual(len(self.cinema.list_of_movies)-1,
                         len(self.cinema.list_of_rooms)*len(self.cinema.showing_time))

        # check if each movie movie appear in database
        for movie in self.cinema.list_of_movies[1:]:
            self.assertTrue(movie.name in self.cinema.movie_database.list_of_movies)

        # run tearDown method
        self.post_test()

    def test_allocation_seat_generator(self):
        '''  test allocation seat generator'''

        # run SetUp method
        self.pre_test()

        # run alocation seat generator
        self.cinema.allocation_seat_generator()

        # check if some seats are already occupated for each movie
        for movie in self.cinema.list_of_movies[1:]:
            self.assertTrue(movie.room.occupated_places > 0)

        # run tearDown method
        self.post_test()

    def test_select_movie(self):
        ''' test 3 edge cases for select method '''

        # run SetUp method
        self.pre_test()

        # not convertible movie_id to int
        with self.assertRaises(ValueError):
            self.cinema.select_movie('1.0')

        # movie_id out of range
        with self.assertRaises(Exception):
            self.cinema.select_movie(99)

        # correct movie_id
        self.assertIsInstance(self.cinema.select_movie('1'), Movie)

        # run tearDown method
        self.post_test()


if __name__ == '__main__':
    unittest.main()
