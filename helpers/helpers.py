def parse_str_to_int(string):
    try:
        integer = int(string)
        return integer
    except ValueError as e:
        raise ValueError(f'Cannot convert string to integer!\n{e}')


def ticket_printer(cinema, title, time, room, client, row, col):
    info = f'Cinema: {cinema} Title: {title} Time: {time} Room: {room} Cilent:{client} Row: {row} Place: {col}'
    frame = f'+{"-" * (len(info) + 2)}+'
    text = f'| {info} |'
    list_of_lines = [frame, frame, frame, text, frame, frame, frame]
    output = '\n'.join(list_of_lines)
    print(f'Here is your ticket:')
    print(f'\n{output}')