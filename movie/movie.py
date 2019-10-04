import os
import time
from helpers import *

class Movie:
    ''' Class for single cinema movie '''
    def __init__(self, cinema, name, room, time):
        self.cinema = cinema
        self.name = name
        self.room = room.__copy__()
        self.time = time
        self.list_of_action = [None, 'make_reservation', 'change_reservation', 'refuse_reservation']

    def show_menu(self):
        os.system('clear')
        print(f'Seating plan for Movie "{self.name}" at Room {self.room.name} at {self.time}')
        self.room.show_seating()
        print(f'Total places: {self.room.num_of_total_places()} Available places: {self.room.num_of_free_places()}\n')
        print('Select a action, press "x" to exit or press "b" go back')
        for i, action in enumerate(self.list_of_action):
            if action is not None:
                print(f'{i}. {action}')
        user_input = input()
        if user_input.upper() == 'X':
            exit()
        if user_input.upper() == 'B':
            self.cinema.show_main_menu()
        try:
            self.select_action(user_input)
        except Exception as e:
            os.system('clear')
            print('Something go wrong ... ')
            print(f'Details: {e}')
            print('Back to Movie Menu')
            time.sleep(3)
            self.show_menu()

    def select_action(self, user_input):
        try:
            int_user_input = parse_str_to_int(user_input)
        except ValueError as e:
            raise ValueError(e)
        if int_user_input in range(1, len(self.list_of_action)):
            exec(f'self.{self.list_of_action[int_user_input]}()')
        else:
            raise Exception(f'Action number {int_user_input} not found...')

    def make_reservation(self):
        print('Enter a full name to make reservation, press "x" to exit or press "b" go back')
        user_name = input()
        if user_name.upper() == 'X':
            exit()
        if user_name.upper() == 'B':
            self.show_menu()
        print('Enter the row where you want to sit:')
        row = input()
        print('Enter the place where you want to sit:')
        col = input()
        try:
            self.room.allocate_seat(user_name, row, col)
            ticket_printer(self.cinema.name, self.name, self.time, self.room.name, user_name, row, col)
        except Exception as e:
            os.system('clear')
            print('Something go wrong ... ')
            print(f'Details: {e}')
            print('Try to make reservation again')
            time.sleep(3)
            self.show_menu()

    def refuse_reservation(self):
        print('Enter "x" to exit, press "b" to go back or press any other key to continue...')
        response = input()
        if response.upper() == 'X':
            exit()
        if response.upper() == 'B':
            self.show_menu()
        print('Enter the row in which you took place:')
        row = input()
        print('Enter the place in which you took place:')
        col = input()
        try:
            self.room.release_seat(row, col)
        except Exception as e:
            os.system('clear')
            print('Something go wrong ... ')
            print(f'Details: {e}')
            print('Try to refuse reservation again')
            time.sleep(3)
            self.show_menu()

    def change_reservation(self):
        print('Enter "x" to exit, press "b" to go back or press any other key to continue...')
        response = input()
        if response.upper() == 'X':
            exit()
        if response.upper() == 'B':
            self.show_menu()
        print('Enter the row in which you took place:')
        from_row = input()
        print('Enter the place in which you took place:')
        from_col = input()
        print('-'*30)
        print('Enter the row where you want to sit:')
        to_row = input()
        print('Enter the place where you want to sit:')
        to_col = input()
        try:
            self.room.relocate_seat(from_row, from_col, to_row, to_col)
            ticket_printer(self.cinema.name, self.name, self.time, self.room.name, self.room._Room__seating[int(to_row)][int(to_col)], to_row, to_col)
        except Exception as e:
            os.system('clear')
            print('Something go wrong ... ')
            print(f'Details: {e}')
            print('Try to make relocation again')
            time.sleep(3)
            self.show_menu()