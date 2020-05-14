import filecmp
import os
import unittest
import movie_database

CINEMA_NAME = 'TestCinema'
CINEMA_PATH = f'./data/{CINEMA_NAME}_movies.txt'
MOVIES_PATH = './data/movies.txt'
REAL_MOVIE_NAME = 'Zootopia'
TEST_MOVIE_NAME = 'TestMovie'
FICTION_MOVIE_NAME ='FictionMovie'


class MyTestCase(unittest.TestCase):

    def setUp(self):
        ''' create instance of Movie_database class '''
        if os.path.exists(CINEMA_PATH):
            os.remove(CINEMA_PATH)
        self.db = movie_database.Movie_database(CINEMA_NAME)

    def tearDown(cls):
        ''' delete movie file after each test'''
        if os.path.exists(CINEMA_PATH):
            os.remove(CINEMA_PATH)

    def test_create_file(self):
        ''' check if .txt file was created '''
        self.assertTrue(os.path.isfile(CINEMA_PATH))

    def test_create_list(self):
        ''' check if instace field is a list'''
        self.assertTrue(isinstance(self.db.list_of_movies,list))

    def test_create_movie_database(self):
        ''' check if content of movie.txt file was correctly copied to new file'''
        print(self.db.movie_database)
        print(MOVIES_PATH)
        self.assertTrue(filecmp.cmp(self.db.movie_database, MOVIES_PATH))

    def test_read_movies_from_disk(self):
        ''' check the correctness of reading data from disc to list '''
        with open(self.db.movie_database) as file:
            for i, movie in enumerate(file):
                self.assertEqual(movie.strip(), self.db.list_of_movies[i])

    def test_add_movie(self):
        ''' check the correctness of adding new movie to database '''
        self.db.add_movie(TEST_MOVIE_NAME)
        # check if last element is a new added movie
        self.assertEqual(self.db.list_of_movies[-1], TEST_MOVIE_NAME)
        # check save_movies_to_disk method (the same checking like in test_read_movies_from_disk)
        self.test_read_movies_from_disk()

    def test_delete_movie(self):
        ''' check the correctness of removing to database '''
        self.db.delete_movie(REAL_MOVIE_NAME)
        # check if movie was deleted from list
        self.assertTrue(REAL_MOVIE_NAME not in self.db.list_of_movies)
        # check save_movies_to_disk method (the same checking like in test_read_movies_from_disk)
        self.test_read_movies_from_disk()
        # check if program throw up exception for fiction movie
        with self.assertRaises(Exception):
            self.db.delete_movie(FICTION_MOVIE_NAME)


if __name__ == '__main__':

    unittest.main()
