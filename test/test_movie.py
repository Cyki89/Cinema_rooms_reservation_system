import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
import movie


MOVIE_NAME = 'XXX'
MOVIE_TIME = '15:00'
LIST_OF_ACTION = [None, 'make_reservation', 'change_reservation', 'refuse_reservation']


class MyTestCase(unittest.TestCase):

    @classmethod
    @patch('cinema.Cinema') # mock cinema object
    @patch('room.Room') # mock room object
    def setUpClass(cls, cinema, room):
        ''' create instance of Movie class '''
        room.__copy__ = MagicMock()
        cls.obj = movie.Movie(cinema, MOVIE_NAME, room, MOVIE_TIME)
        room.__copy__.stop()

    def test_create_instance(self):
        ''' check if instance was correctly created '''
        self.assertEqual(self.obj.name, MOVIE_NAME)
        self.assertEqual(self.obj.time, MOVIE_TIME)
        self.assertEqual(self.obj.list_of_action, LIST_OF_ACTION)

    @patch('user_interface.refuse_reservation_interface')
    @patch('user_interface.change_reservation_interface')
    @patch('user_interface.make_reservation_interface')
    def test_select_action(self, mock_make_reservation_interface, mock_change_reservation_interface,
                             mock_refuse_reservation_interface):
        ''' test 3 edge cases for select_action method '''

        # not convertible as input
        with self.assertRaises(ValueError):
            self.obj.select_action('1.0')

        # user action out of range
        with self.assertRaises(Exception):
            self.obj.select_action(0)

        # pack all all interface methods to the one list
        interface_methods = [mock_make_reservation_interface, mock_change_reservation_interface,
                             mock_refuse_reservation_interface]

        # check if the correct method was called with correct input
        for i, method in enumerate(interface_methods,1):
            self.obj.select_action(i)
            method.assert_called_once()


if __name__ == '__main__':

    unittest.main()
