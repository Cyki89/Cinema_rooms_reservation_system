import unittest

import room

ROOM_NAME = 'Room Test'
ROOM_SIZE = (10, 12)
ROOM_SEATING = [None] + [[None] + list(range(1, ROOM_SIZE[1] + 1)) for _ in range(ROOM_SIZE[0])]
ROOM_SEATING[1][1] = 'RESERVED'
TOTAL_PLACES = ROOM_SIZE[0] * ROOM_SIZE[1]
OCCUPATED_PLACES = 10
USER_NAME = 'TEST_USER'


class MyTestCase(unittest.TestCase):

    def setUp(self):
        ''' create instance of Movie class '''
        self.room = room.Room(ROOM_NAME, ROOM_SIZE)
        # change number of occupated places
        self.room.occupated_places = OCCUPATED_PLACES
        # reserve one place in cinema room
        self.room._Room__seating[1][1] = ROOM_SEATING[1][1]

    def tearDown(self):
        ''' create instance of Movie class '''
        del self.room

    def test_create_instance(self):
        ''' check if instance was correctly created '''
        self.assertEqual(self.room.name, ROOM_NAME)
        self.assertEqual(self.room.size, ROOM_SIZE)
        self.assertEqual(self.room._Room__seating, ROOM_SEATING)
        self.assertEqual(self.room.occupated_places, OCCUPATED_PLACES )

    def test_parse_seat(self):
        ''' test 4 edge cases for parse_seat method '''

        # test casses for wrong input
        places = [ ('11', '10'),
                   ('10', '13'),
                   ('10.0', '12')
        ]

        # expected error messages
        err_msg_1 = f'Row {places[0][0]} is not in range 1-{self.room.size[0]}' # row out of range
        err_msg_2 = f'Place {places[1][1]} is not in range 1-{self.room.size[1]}' # place out of range
        err_msg_3 = ("Unappropiate types of co-ordinates.Both need to be int:\n" 
                     "Cannot convert string to integer!\n"
                     f"invalid literal for int() with base 10: '{places[2][0]}'") # not convertible string to int

        # put all message on the one list
        err_messages = [err_msg_1, err_msg_2, err_msg_3]

        # test 3 wrong inputs in a loop
        for place, err_msg in zip(places, err_messages):
            with self.assertRaises(Exception) as err:
                self.room.parse_seat(*place)
            self.assertEqual(str(err.exception), err_msg)

        # test correct input
        self.assertEqual(self.room.parse_seat(10, 10), (10, 10) )

    def test_allocate_set(self):
        ''' test 3 edge cases for allocate_seat method '''

        # test casses for wrong input
        places = [
            ('11', '12'), # row out of range
            ('1', '1'), # seat is aleady occupated

        ]

        # expected error messages
        err_messages = [ ('Occur some problem during allocation:\n'
                          f'Row {int(places[0][0])} is not in range 1-{self.room.size[0]}'),

                         ('Occur some problem during allocation:\n'
                          f'Seat {int(places[1][0])}, {int(places[1][1])} is already occuppated')
        ]

        # test wrong inputs in a loop
        for place, err_msg in zip(places, err_messages):
            with self.assertRaises(Exception) as err:
                self.room.allocate_seat(USER_NAME, *place)
            self.assertEqual(str(err.exception), err_msg)

        # correct input
        place = ('1', '2')
        self.room.allocate_seat(USER_NAME, *place)
        self.assertEqual(self.room.occupated_places, OCCUPATED_PLACES+1)
        self.assertEqual(self.room._Room__seating[int(place[0])][int(place[1])], USER_NAME)

    def test_relocate_set(self):
        ''' test 4 edge cases for parse_seat method '''

        # test casses for wrong input
        places = [
            ( ('11', '12'), ('10', '10') ), # 'seat_from' row out of range
            ( ('10', '10'), ('10', '10') ), # 'seat_from' is free
            ( ('1', '1'), ('1', '1') ),  # 'seat_to' is already occupated
        ]

        # expected error messages
        err_messages = [ ('Occur some problem during relocation:\n'
                          f'Row {int(places[0][0][0])} is not in range 1-{self.room.size[0]}'),

                         ('Occur some problem during relocation:\n'
                          f'Seat {int(places[1][0][0])},{int(places[1][0][1])} is free!!!'),

                         ('Occur some problem during relocation:\n'
                          f'Seat {int(places[2][1][0])},{int(places[2][1][1])} already occupied!!!')
        ]

        # test wrong inputs in a loop
        for place, err_msg in zip(places, err_messages):
            with self.assertRaises(Exception) as err:
                self.room.relocate_seat(*place[0], *place[1])
            self.assertEqual(str(err.exception), err_msg)

        # correct input
        place = ( ('1', '1'), ('2', '2') )
        self.room.relocate_seat( *place[0], *place[1])

        self.assertEqual(self.room._Room__seating[int(place[1][0])][int(place[1][1])], ROOM_SEATING[1][1])
        self.assertEqual(self.room._Room__seating[int(place[0][0])][int(place[0][1])], int(place[0][1]))

    def test_release_set(self):
        ''' test 3 edge cases for release_seat method '''

        # test casses for wrong input
        places = [
            ('11', '12'),  # row out of range
            ('2', '2'),  # seat is aleady free

        ]

        # expected error messages
        err_messages = [('Occur some problem during releasing seat:\n'
                         f'Row {int(places[0][0])} is not in range 1-{self.room.size[0]}'),

                        ('Occur some problem during releasing seat:\n'
                         f'Seat {int(places[1][0])},{int(places[1][1])} is free!!!')
                        ]

        # test wrong inputs in a loop
        for place, err_msg in zip(places, err_messages):
            with self.assertRaises(Exception) as err:
                self.room.release_seat(*place)
            self.assertEqual(str(err.exception), err_msg)

        # correct input
        place = ('1', '1')
        self.room.release_seat(*place)
        self.assertEqual(self.room.occupated_places, OCCUPATED_PLACES - 1)
        self.assertEqual(self.room._Room__seating[int(place[0])][int(place[1])], int(place[1]))

    def test_client_seats(self):
        ''' check client_seats method '''
        self.assertEqual( list(self.room.cilent_seats() ), [ (ROOM_SEATING[1][1], 1, 1) ] )

    def test_num_of_total_places(self):
        ''' check if num of total places was correct calculated '''
        self.assertEqual(self.room.num_of_total_places(), TOTAL_PLACES)

    def test_num_of_free_places(self):
        ''' check if num of free places was correct calculated '''
        self.assertEqual(self.room.num_of_free_places(), TOTAL_PLACES-OCCUPATED_PLACES)

    def test_copy(self):
        ''' check __copy__ method'''
        room_copy = self.room.__copy__()
        self.assertEqual(self.room.name, room_copy.name)
        self.assertEqual(self.room.size, room_copy.size)


if __name__ == '__main__':
    unittest.main()
