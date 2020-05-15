import os
import time
import inspect
import sys
from helpers import *


def exit_go_back(user_input, curr_method):
    '''Method use to exit from aplication or go back to previous screen'''
    if user_input.upper() == 'X':
        sys.exit()
    if user_input.upper() == 'B':
        return interface_methods[curr_method][1]
    return user_input


def parse_user_input(curr_method, user_input=None):
    '''Method use to interprete user input'''
    print(f'{interface_methods[curr_method][0]}')
    if user_input == None:
        user_input = input()
    return exit_go_back(user_input, curr_method)


def handling_exception(e, curr_method, curr_object):
    ''' Method use to hanling exception'''
    os.system('clear')
    print('Something go wrong ... ')
    print(f'Details: {e}')
    print('Try again')
    time.sleep(3)
    func = interface_methods[curr_method][1]
    if func.__name__ == 'show_interface':
        return show_interface(curr_object)
    else:
        return show_seating_plan(curr_object)


def select_seat(target = 'to'):
    ''' Method use to pull seat co-ordinates from user'''
    print_statement = {
        'to' : 'where you want to sit:',
        'from' : 'in which you took place:'
    }
    print(f'Enter the row {print_statement[target]}')
    row = input()
    print(f'Enter the place {print_statement[target]}')
    col = input()
    return row, col


def show_interface(cinema):
    ''' Method responsible to interaction with user'''
    os.system('clear')
    print(f'Welceome to {cinema.name} Cinema')
    cinema.show_schedule()
    curr_method = inspect.stack()[0][3]
    user_input = parse_user_input(curr_method)
    print(user_input)
    if callable(user_input):
        return user_input(cinema)
    try:
        selected_movie = cinema.select_movie(user_input)
        show_seating_plan(selected_movie)
    except Exception as e:
        print('excpet block')
        return handling_exception(e, curr_method, cinema)
    else:
        return back_to_main_menu(cinema)


def back_to_main_menu(cinema):
    ''' function return user screen to main_menu '''
    print('Back to Main Menu')
    time.sleep(3)
    os.system('clear')
    return show_interface(cinema)


def show_seating_plan(movie):
    ''' Method showing information about selected movie'''
    os.system('clear')
    print(f'Seating plan for Movie "{movie.name}" at Room {movie.room.name} at {movie.time}')
    movie.room.show_seating()
    print(f'Total places: {movie.room.num_of_total_places()} Available places: {movie.room.num_of_free_places()}\n')
    show_actions(movie)


def show_actions(movie):
    # print('Select a action, press "x" to exit or press "b" go back')
    for i, action in enumerate(movie.list_of_action):
        if action is not None:
            print(f'{i}. {action}')
    curr_method = inspect.stack()[0][3]
    user_input = parse_user_input(curr_method)
    if callable(user_input):
        return user_input(movie.cinema)
    try:
        movie.select_action(user_input)
    except Exception as e:
        handling_exception(e, curr_method, movie)


def make_reservation_interface(movie):
    '''Method redirects to room.allocate_seat method'''
    curr_method = inspect.stack()[0][3]
    user_input = parse_user_input(curr_method)
    if callable(user_input):
        return user_input(movie)
    to_row, to_col = select_seat('to')
    try:
        movie.room.allocate_seat(user_input, to_row, to_col)
        ticket_printer(movie.cinema.name, movie.name, movie.time, movie.room.name, user_input, to_row, to_col)
    except Exception as e:
        handling_exception(e, curr_method, movie)


def change_reservation_interface(movie):
    '''Method redirects to room.relocate_seat method'''
    curr_method = inspect.stack()[0][3]
    user_input = parse_user_input(curr_method)
    if callable(user_input):
        return user_input(movie)
    from_row, from_col = select_seat('from')
    to_row, to_col = select_seat('to')
    try:
        movie.room.relocate_seat(from_row, from_col, to_row, to_col)
        ticket_printer(movie.cinema.name, movie.name, movie.time, movie.room.name,
                       movie.room._Room__seating[int(to_row)][int(to_col)], to_row, to_col)
    except Exception as e:
        handling_exception(e, curr_method, movie)


def refuse_reservation_interface(movie):
    '''Method redirects to room.release_seat method'''
    curr_method = inspect.stack()[0][3]
    user_input = parse_user_input(curr_method)
    if callable(user_input):
        return user_input(movie)
    from_row, from_col = select_seat('from')
    try:
        movie.room.release_seat(from_row, from_col)
    except Exception as e:
        handling_exception(e, curr_method, movie)


interface_methods = {
    'show_interface': ('Select a movie_id press "b" to refresh screen or press "x" to exit', show_interface),
    'show_actions': ('Select an action, press "x" to exit or press "b" go back', show_interface),
    'make_reservation_interface': ('Enter a full name to make reservation, press "x" to exit or press "b" go back', show_seating_plan),
    'change_reservation_interface': ('Enter "x" to exit, press "b" to go back or press any other key to continue...', show_seating_plan),
    'refuse_reservation_interface': ('Enter "x" to exit, press "b" to go back or press any other key to continue...', show_seating_plan)
}