import os
import time
import inspect

from helpers import *

previous_interface_methods = {
    'show_interface': 'show_interface(curr_object)',
    'show_actions': 'show_interface(curr_object.cinema)',
    'make_reservation_interface': 'show_seating_plan(curr_object)',
    'change_reservation_interface': 'show_seating_plan(curr_object)',
    'refuse_reservation_interface': 'show_seating_plan(curr_object)'
}

def exit_go_back(user_input, curr_method, curr_object):
    '''Method use to exit from aplication or go back to previous screen'''
    if user_input.upper() == 'X':
        exit()
    # TODO How to close old method when we go back?
    elif user_input.upper() == 'B':
        return exec(previous_interface_methods[curr_method])
    else:
        return user_input


def parse_user_input(curr_method, curr_object):
    '''Method use to interprete user input'''
    print_statement = {
        'show_interface': 'Select a movie_id or press "x" to exit',
        'show_actions': 'Select an action, press "x" to exit or press "b" go back',
        'make_reservation_interface': 'Enter a full name to make reservation, press "x" to exit or press "b" go back',
        'change_reservation_interface': 'Enter "x" to exit, press "b" to go back or press any other key to continue...',
        'refuse_reservation_interface': 'Enter "x" to exit, press "b" to go back or press any other key to continue...'
    }
    print(f'{print_statement[curr_method]}')
    user_input = input()
    return exit_go_back(user_input, curr_method, curr_object)


def handling_exception(e, curr_method, curr_object):
    ''' Method use to hanling exception'''
    os.system('clear')
    print('Something go wrong ... ')
    print(f'Details: {e}')
    print('Try again')
    time.sleep(3)
    return exec(previous_interface_methods[curr_method])


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
    user_input = parse_user_input(curr_method, cinema)
    try:
        selected_movie = cinema.select_movie(user_input)
        show_seating_plan(selected_movie)
    except Exception as e:
        handling_exception(e, curr_method, cinema)
    else:
        print('Back to Main Menu')
        time.sleep(3)
        os.system('clear')
        show_interface(cinema)


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
    user_input = parse_user_input(curr_method, movie)
    try:
        movie.select_action(user_input)
    except Exception as e:
        handling_exception(e, curr_method, movie)


def make_reservation_interface(movie):
    '''Method redirects to room.allocate_seat method'''
    curr_method = inspect.stack()[0][3]
    user_input = parse_user_input(curr_method, movie)
    to_row, to_col = select_seat('to')
    try:
        movie.room.allocate_seat(user_input, to_row, to_col)
        ticket_printer(movie.cinema.name, movie.name, movie.time, movie.room.name, user_input, to_row, to_col)
    except Exception as e:
        handling_exception(e, curr_method, movie)


def change_reservation_interface(movie):
    '''Method redirects to room.relocate_seat method'''
    curr_method = inspect.stack()[0][3]
    user_input = parse_user_input(curr_method, movie)
    from_row, from_col = select_seat('from')
    to_row, to_col = select_seat('to')
    try:
        movie.room.relocate_seat(from_row, from_col, to_row, to_col)
        ticket_printer(movie.cinema.name, movie.name, movie.time, movie.room.name, movie.room._Room__seating[int(to_row)][int(to_col)], to_row, to_col)
    except Exception as e:
        handling_exception(e, curr_method, movie)


def refuse_reservation_interface(movie):
    '''Method redirects to room.release_seat method'''
    curr_method = inspect.stack()[0][3]
    user_input = parse_user_input(curr_method, movie)
    from_row, from_col = select_seat('from')
    try:
        movie.room.release_seat(from_row, from_col)
    except Exception as e:
        handling_exception(e, curr_method, movie)

