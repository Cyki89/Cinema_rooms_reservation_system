import os
import time
from helpers import *

# TODO Corect all method in user interface
def show_interface(cinema):
    ''' Method responsible to interaction with user'''
    os.system('clear')
    print(f'Welceome to {cinema.name} Cinema')
    cinema.show_schedule()
    print('Select a movie_id to go further or press x to exit')
    user_input = input()
    if user_input.upper() == 'X':
        exit()
    try:
        selected_movie = cinema.select_movie(user_input)
        show_seating_plan(selected_movie)
    except Exception as e:
        os.system('clear')
        print('Something go wrong ... ')
        print(f'Details: {e}')
        print('Back to Main Menu')
        time.sleep(3)
        show_interface(cinema)
    else:
        print('Back to Main Menu')
        time.sleep(3)
        os.system('clear')
        show_interface(cinema)


def show_seating_plan(movie):
    os.system('clear')
    print(f'Seating plan for Movie "{movie.name}" at Room {movie.room.name} at {movie.time}')
    movie.room.show_seating()
    print(f'Total places: {movie.room.num_of_total_places()} Available places: {movie.room.num_of_free_places()}\n')
    show_actions(movie)


def show_actions(movie):
    print('Select a action, press "x" to exit or press "b" go back')
    for i, action in enumerate(movie.list_of_action):
        if action is not None:
            print(f'{i}. {action}')
    user_input = input()
    if user_input.upper() == 'X':
        exit()
    if user_input.upper() == 'B':
        show_interface(movie.cinema)
    try:
        movie.select_action(user_input)
    except Exception as e:
        os.system('clear')
        print('Something go wrong ... ')
        print(f'Details: {e}')
        print('Back to Movie Menu')
        time.sleep(3)
        show_seating_plan(movie)


def make_reservation_interface(movie):
    '''Method redirects to room.allocate_seat method'''
    print('Enter a full name to make reservation, press "x" to exit or press "b" go back')
    user_name = input()
    if user_name.upper() == 'X':
        exit()
    if user_name.upper() == 'B':
        show_seating_plan(movie)
    print('Enter the row where you want to sit:')
    row = input()
    print('Enter the place where you want to sit:')
    col = input()
    try:
        movie.room.allocate_seat(user_name, row, col)
        ticket_printer(movie.cinema.name, movie.name, movie.time, movie.room.name, user_name, row, col)
    except Exception as e:
        os.system('clear')
        print('Something go wrong ... ')
        print(f'Details: {e}')
        print('Try to make reservation again')
        time.sleep(3)
        show_seating_plan(movie)


def change_reservation_interface(movie):
    '''Method redirects to room.relocate_seat method'''
    print('Enter "x" to exit, press "b" to go back or press any other key to continue...')
    response = input()
    if response.upper() == 'X':
        exit()
    if response.upper() == 'B':
        show_seating_plan(movie)
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
        movie.room.relocate_seat(from_row, from_col, to_row, to_col)
        ticket_printer(movie.cinema.name, movie.name, movie.time, movie.room.name, movie.room._Room__seating[int(to_row)][int(to_col)], to_row, to_col)
    except Exception as e:
        os.system('clear')
        print('Something go wrong ... ')
        print(f'Details: {e}')
        print('Try to make relocation again')
        time.sleep(3)
        show_seating_plan(movie)


def refuse_reservation_interface(movie):
    '''Method redirects to room.release_seat method'''
    print('Enter "x" to exit, press "b" to go back or press any other key to continue...')
    response = input()
    if response.upper() == 'X':
        exit()
    if response.upper() == 'B':
        show_seating_plan(movie)
    print('Enter the row in which you took place:')
    row = input()
    print('Enter the place in which you took place:')
    col = input()
    try:
        movie.room.release_seat(row, col)
    except Exception as e:
        os.system('clear')
        print('Something go wrong ... ')
        print(f'Details: {e}')
        print('Try to refuse reservation again')
        time.sleep(3)
        show_seating_plan(movie)

