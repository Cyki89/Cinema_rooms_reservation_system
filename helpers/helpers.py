def parse_str_to_int(string):
    try:
        integer = int(string)
        return integer
    except ValueError as e:
        raise ValueError(f'Cannot convert string to integer!\n{e}')


def ticket_printer(cinema, title, time, room, client, row, col):
    '''Method create and print ticket for client'''
    info = f'Cinema: {cinema} Title: {title} Time: {time} Room: {room} Cilent:{client} Row: {row} Place: {col}'
    frame = f'+{"-" * (len(info) + 2)}+'
    text = f'| {info} |'
    list_of_lines = [frame, frame, frame, text, frame, frame, frame]
    output = '\n'.join(list_of_lines)
    print(f'Here is your ticket:')
    print(f'\n{output}\n')


def try_except_decorator(func):
    '''Method adding try/except block to function'''
    # print(f'Adding try_except_decorator to {func.__name__}')
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            raise Exception(e)
    return wrapper


def error_handling_class_decorator(cls):
    '''Method use to add error handling do class method'''
    for k, v in vars(cls).items():
        if callable(v) and v.__name__ is not '__init__':
            setattr(cls, k, try_except_decorator(v))
    return cls