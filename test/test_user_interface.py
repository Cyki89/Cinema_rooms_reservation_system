import unittest
from unittest.mock import patch

import user_interface


class MyTestCase(unittest.TestCase):

    def setUp(self):
        '''create mocks '''
        self.mock_movie = patch('movie.Movie').start()
        self.mock_cinema = patch('cinema.cinema.Cinema').start()
        self.mock_exit_go_back = patch('user_interface.user_interface.exit_go_back').start()
        self.mock_show_seating_plan = patch('user_interface.user_interface.show_seating_plan').start()
        self.mock_show_interface = patch('user_interface.user_interface.show_interface').start()
        self.mock_input = patch('user_interface.user_interface.input').start()
        self.mock_time = patch('user_interface.user_interface.time').start()
        self.mock_print = patch('user_interface.user_interface.print').start()
        self.mock_handling_exception = patch('user_interface.user_interface.handling_exception').start()
        self.mock_parse_user_input = patch('user_interface.user_interface.parse_user_input').start()
        self.mock_show_actions = patch('user_interface.user_interface.show_actions').start()
        self.mock_ticket_printer = patch('user_interface.user_interface.ticket_printer').start()
        self.mock_select_seat = patch('user_interface.user_interface.select_seat').start()
        self.mock_back_to_main_menu = patch('user_interface.user_interface.back_to_main_menu').start()

    def tearDown(self):
        ''' stop all mocks after each test '''
        self.addCleanup(patch.stopall)

    def test_exit_go_back(self):
        ''' test 3 edge case for exit_go_back function '''

        # set a test variable
        curr_method = 'show_interface'

        # unmock a test function
        self.mock_exit_go_back.stop()

        # return to the previous screen
        for curr_method in user_interface.interface_methods.keys():
            self.assertEqual(user_interface.exit_go_back('b', curr_method),
                             user_interface.interface_methods[curr_method][1])

        # exit from program
        with self.assertRaises(SystemExit):
            user_interface.exit_go_back('x', curr_method)

        # normal input
        self.assertEqual(user_interface.exit_go_back('1', curr_method), '1')

    def test_parse_user_input(self):
        ''' test parser user input function '''

        # set a test variables
        user_input = '1'
        curr_method = 'show_actions'

        # check if function exit_go_back was called exactly one time with correct arguments
        user_interface.parse_user_input(curr_method, user_input)
        self.mock_exit_go_back.assert_called_once_with(user_input, curr_method)

    def test_handling_exception(self):
        ''' test handling exception function '''

        # set test variables
        exception = None
        curr_object = None

        # unmock test functions
        self.mock_handling_exception.stop()

        # check if correct function was called correct number of times
        for curr_method in user_interface.interface_methods.keys():
            user_interface.handling_exception(exception, curr_method, curr_object)
        self.assertEqual(self.mock_show_interface.call_count, 2)
        self.assertEqual(self.mock_show_seating_plan.call_count, 3)


    def test_select_seat(self):
        ''' test select seat function '''

        # unmock a test function
        self.mock_select_seat.stop()

        # set a test user_input
        self.mock_input.return_value = None

        self.assertEqual(user_interface.select_seat(), (None, None))


    def test_show_interface(self):
        ''' test show interface function '''

        # set test variables
        place = None
        movie_name = None

        # unmock a test function
        self.mock_show_interface.stop()

        # edge case 1 - back to previous screen
        self.mock_parse_user_input.return_value = self.mock_show_seating_plan # mock function to return callable object
        user_interface.show_interface(self.mock_cinema)
        self.mock_show_seating_plan.assert_called_once_with(self.mock_cinema) # check if function was called with correct argument

        # reset mock calls history
        self.mock_show_seating_plan.reset_mock()

        # edge case 2 - user pass correct movie id

        self.mock_parse_user_input.return_value = place # mock function return to action id
        self.mock_cinema.select_movie.return_value = movie_name # mock function to return example movie name
        self.mock_back_to_main_menu.return_value = None # prevent infinite recursive loop
        user_interface.show_interface(self.mock_cinema)
        self.mock_show_seating_plan.assert_called_once_with(movie_name) # check if function was called with correct argument
        self.mock_back_to_main_menu.assert_called_once() # check if function was exactly one time

        # edge case 3 - bad user input
        self.mock_cinema.select_movie.side_effect = Exception() # mock function to return exception
        user_interface.show_interface(self.mock_cinema)
        self.mock_handling_exception.assert_called_once() # check if function was called exactly one time

    def test_back_to_main_menu(self):
        ''' test back_to_main_menu function '''

        # set a test variable
        user_input = None

        # unmock a test function
        self.mock_show_interface.stop()

        # check if function was called exactly one time with correct arg
        user_interface.back_to_main_menu(user_input)
        self.mock_show_interface.assert_called_once_with(user_input)


    def test_show_seating_plan(self):
        ''' test show_seating_plan function '''

        # unmock a test function
        self.mock_show_seating_plan.stop()

        # check if function was called exactly one time with correct arg
        user_interface.show_seating_plan(self.mock_movie)
        self.mock_show_actions.assert_called_once_with(self.mock_movie)

    def test_show_actions(self):
        ''' test 3 edge cases for show_action function '''

        # unmock a test function
        self.mock_show_actions.stop()

        # edge case 1 - user want to back to previous screen
        self.mock_parse_user_input.return_value = self.mock_show_seating_plan # mock function to return callable object
        user_interface.show_actions(self.mock_movie)
        self.mock_show_seating_plan.assert_called_once_with(self.mock_movie.cinema) # check if function was called with correct argument

        # edge case 2 - user pass correct movie id
        self.mock_parse_user_input.return_value = 1 # mock function return to action id
        user_interface.show_actions(self.mock_movie)
        self.mock_movie.select_action.assert_called_once_with(1)

        # edge case 3 - incorrect user input
        self.mock_movie.select_action.side_effect = Exception() # mock method to raise exception
        user_interface.show_actions(self.mock_movie)
        self.mock_handling_exception.assert_called_once() # check if function was called exactly one time

    def test_make_reservation_interface(self):
        ''' test 3 edge cases for make_reservation_interface function '''

        # edge case 1 - back to previous screen
        self.mock_parse_user_input.return_value = self.mock_show_seating_plan  # mock function to return callable object
        user_interface.make_reservation_interface(self.mock_movie)
        self.mock_show_seating_plan.assert_called_once_with(self.mock_movie) # check if func was called with correct arg

        # edge case 2 - user pass name
        self.mock_parse_user_input.return_value = 'user_name' # mock function return example name
        self.mock_select_seat.return_value = ('row', 'col')
        user_interface.make_reservation_interface(self.mock_movie)
        self.mock_movie.room.allocate_seat.assert_called_once_with('user_name', 'row', 'col')
        self.mock_ticket_printer.assert_called_once_with(self.mock_movie.cinema.name, self.mock_movie.name,
                                                         self.mock_movie.time, self.mock_movie.room.name,
                                                         'user_name', 'row', 'col')

        # edge case 3 - user pass wrong input
        self.mock_movie.room.allocate_seat.side_effect = Exception()
        user_interface.make_reservation_interface(self.mock_movie) # mock function to raise exception
        self.mock_handling_exception.assert_called_once() # check if function was called exactly one time

    def test_change_reservation_interface(self):
        ''' test 3 edge cases for change_reservation_interface function '''

        # edge case 1 - back to previous screen
        self.mock_parse_user_input.return_value = self.mock_show_seating_plan  # mock function to return callable object
        user_interface.change_reservation_interface(self.mock_movie)
        self.mock_show_seating_plan.assert_called_once_with(self.mock_movie)  # check if function was called with correct argument

        # edge case 2 - user pass name and correct places to change reservation
        # set a test variables
        from_row = from_col = 1
        to_row = to_col = 2

        self.mock_parse_user_input.return_value = ''  # mock function to return example user input
        self.mock_select_seat.side_effect = [(from_row, from_col), (to_row, to_col)]
        user_interface.change_reservation_interface(self.mock_movie)
        self.mock_movie.room.relocate_seat.assert_called_once_with(from_row, from_col, to_row, to_col)
        self.mock_ticket_printer.assert_called_once()

        # edge case 3 - user pass wrong input(places)
        self.mock_select_seat.side_effect = [(None, None), (None, None)]
        self.mock_movie.room.relocate_seat.side_effect = Exception()
        user_interface.change_reservation_interface(self.mock_movie)  # mock function to raise exception
        self.mock_handling_exception.assert_called_once()  # check if function was called exactly one time

    def test_refuse_reservation_interface(self):
        ''' test 3 edge cases for refuse_reservation_interface function '''

        # edge case 1 - user want to back to previous screen
        self.mock_parse_user_input.return_value = self.mock_show_seating_plan  # mock function to return callable object
        user_interface.refuse_reservation_interface(self.mock_movie)
        self.mock_show_seating_plan.assert_called_once_with(self.mock_movie)  # check if function was called with correct argument

        # edge case 2 - user pass name and correct places to refuse reservation
        # set a test variables
        from_row = from_col = 1
        self.mock_parse_user_input.return_value = ''
        self.mock_select_seat.return_value = (from_row, from_col)
        user_interface.refuse_reservation_interface(self.mock_movie)
        self.mock_movie.room.release_seat.assert_called_once_with(from_row, from_col)

        # edge case 3 - user pass wrong input(place)
        self.mock_movie.room.release_seat.side_effect = Exception()
        user_interface.refuse_reservation_interface(self.mock_movie)  # mock function to raise exception
        self.mock_handling_exception.assert_called_once()  # check if function was called exactly one time


if __name__ == '__main__':

    unittest.main()

