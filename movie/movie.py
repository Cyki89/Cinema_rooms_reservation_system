import user_interface
from helpers import *

class Movie:
    ''' Class for single cinema movie '''
    def __init__(self, cinema, name, room, time):
        self.cinema = cinema
        self.name = name
        self.room = room.__copy__() # to enable run several cinema movie in one room
        self.time = time
        self.list_of_action = [None, 'make_reservation', 'change_reservation', 'refuse_reservation']  # variable use to select method using exec()

    def select_action(self, user_input):
        '''Method redirects to other class method'''
        try:
            int_user_input = parse_str_to_int(user_input)
        except ValueError as e:
            raise ValueError(e)
        if int_user_input in range(1, len(self.list_of_action)):
            return exec(f'user_interface.{self.list_of_action[int_user_input]}_interface(self)')
        else:
            raise Exception(f'Action number {int_user_input} not found...')
