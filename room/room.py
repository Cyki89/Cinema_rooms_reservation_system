from helpers import *

class Room:
    ''' Class for single cinema room '''
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.occupated_place = 0
        self.create_seating()

    def create_seating(self):
        try:
            if self.validate_room():
                self.__seating = [None] + [[None] + list(range(1, self.size[1] + 1)) for _ in range(self.size[0])]
        except Exception as e:
            raise Exception(f'Creating a new room failed:\n{e}')

    def validate_room(self):
        if not isinstance(self.name, str):
            raise Exception(f'Name need to be string, not {type(self.name)}')
        if len(self.size) != 2:
            raise Exception (f'Unappropiate numebrs of dimentions {self.size}. Need to be two.')
        if not isinstance(self.size[0], int) or not isinstance(self.size[1], int):
            raise Exception(f'Unappropiate types of dimentions.\nRows: {type(self.size[0])} Cols: {type(self.size[1])}. Both need to be int.')
        if self.size[0] <= 0 or self.size[1] <= 0:
            raise Exception(f'Both dimentions have to be grater than 0.\nRows: {self.size[0]} Cols: {self.size[1]}.')
        return True

    def parse_seat(self, row, col):
        try:
            int_row = parse_str_to_int(row)
            if int_row <= 0 or int_row > self.size[0]:
                raise Exception(f'Row {int_row} is not in range 1-{self.size[0]}')
            int_col = parse_str_to_int(col)
            if int_col <= 0 or int_col > self.size[1]:
                raise Exception(f'Place {int_col} is not in range 1-{self.size[1]}')
        except ValueError as e:
            raise Exception(f'Unappropiate types of co-ordinates.Both need to be int:\n{e}')
        return int_row, int_col

    def allocate_seat(self, name, row, col):
        try:
            int_row, int_col = self.parse_seat(row, col)
            if isinstance(self.__seating[int_row][int_col], int):
                self.__seating[int_row][int_col] = name
                self.occupated_place += 1
                print(f'Alocation successfull Name: {name} Row: {int_row} Place: {int_col}') # to trash?
            else:
                raise Exception(f'Seat {int_row}, {int_col} is already occuppated')
        except Exception as e:
            raise Exception(f'Occur some problem during allocation:\n{e}')

    def relocate_seat(self, from_row, from_col, to_row, to_col):
        try:
            int_from_row, int_from_col = self.parse_seat(from_row, from_col)
            if isinstance(self.__seating[int_from_row][int_from_col], int):
                raise Exception(f'Seat {int_from_row},{int_from_col} is free!!!')
            int_to_row, int_to_col = self.parse_seat(to_row, to_col)
            if isinstance(self.__seating[int_to_row][int_to_col], str):
                raise Exception(f'Seat {int_to_row},{int_to_col} already occupied!!!')
            self.__seating[int_to_row][int_to_col] = self.__seating[int_from_row][int_from_col]
            self.__seating[int_from_row][int_from_col] = int_from_col
            print(f'Relocation place successfull for place {int_from_row},{int_from_col} to {int_to_row},{int_to_col}')
        except Exception as e:
            raise Exception(f'Occur some problem during relocation:\n{e}')

    def release_seat(self, row, col):
        try:
            int_row, int_col = self.parse_seat(row, col)
            if isinstance(self.__seating[int_row][int_col], int):
                raise Exception(f'Seat {int_row},{int_col} is free!!!')
            self.__seating[int_row][int_col] = int_col
            self.occupated_place -= 1
            print(f'Releasing place {int_row},{int_col} successfull')  # to trash?
        except Exception as e:
            raise Exception(f'Occur some problem during releasing seat:\n{e}')

    def show_seating(self):
        print_seating = [['{0:2s}'.format(str(col)) if isinstance(col, int) else '{0:2s}'.format('X') for col in row[1:]] for row in self.__seating if row is not None]
        for i, row in enumerate(print_seating, 1):
            # print(f'{i}\t{row}')
            print('{}\t|  {}  |'.format(i, '  '.join(row)))

    def cilent_seats(self):
        for row in range(1,self.size[0]+1):
            for col in range(1,self.size[1]+1):
                client = self.__seating[row][col]
                if isinstance(client, str) :
                    yield (client, (row, col))

    def num_of_total_places(self):
        return self.size[0] * self.size[1]

    def num_of_free_places(self):
        return self.num_of_total_places()- self.occupated_place

    def __copy__(self):
        return Room(self.name, self.size)