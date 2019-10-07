from helpers import *

class Room:
    ''' Class for single cinema room '''
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.__seating = [None] + [[None] + list(range(1, self.size[1] + 1)) for _ in range(self.size[0])]
        self.occupated_places = 0 # field keep number of already occupied seats

    def parse_seat(self, row, col):
        '''Method parse passed row and col into ints and validate it'''
        try:
            int_row, int_col= parse_str_to_int(row), parse_str_to_int(col)
            if int_row not in range(1, self.size[0]+1):
                raise Exception(f'Row {int_row} is not in range 1-{self.size[0]}')
            if int_col not in range(1, self.size[1]+1):
                raise Exception(f'Place {int_col} is not in range 1-{self.size[1]}')
        except ValueError as e:
            raise Exception(f'Unappropiate types of co-ordinates.Both need to be int:\n{e}')
        return int_row, int_col

    def allocate_seat(self, name, row, col):
        '''Method allocate client to seat'''
        try:
            int_row, int_col = self.parse_seat(row, col)
            if isinstance(self.__seating[int_row][int_col], int):
                self.__seating[int_row][int_col] = name
                self.occupated_places += 1
                print(f'Alocation successfull Name: {name} Row: {int_row} Place: {int_col}') # to trash?
            else:
                raise Exception(f'Seat {int_row}, {int_col} is already occuppated')
        except Exception as e:
            raise Exception(f'Occur some problem during allocation:\n{e}')

    def relocate_seat(self, from_row, from_col, to_row, to_col):
        '''Method relocate client from one seat to another'''
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
        '''Method release client from seat'''
        try:
            int_row, int_col = self.parse_seat(row, col)
            if isinstance(self.__seating[int_row][int_col], int):
                raise Exception(f'Seat {int_row},{int_col} is free!!!')
            self.__seating[int_row][int_col] = int_col
            self.occupated_places -= 1
            print(f'Releasing place {int_row},{int_col} successfull')  # to trash?
        except Exception as e:
            raise Exception(f'Occur some problem during releasing seat:\n{e}')

    def show_seating(self):
        '''Method show room seat in readable format'''
        print_seating = [['{0:2s}'.format(str(col)) if isinstance(col, int) else '{0:2s}'.format('X') for col in row[1:]] for row in self.__seating if row is not None]
        for i, row in enumerate(print_seating, 1):
            print('{}\t|  {}  |'.format(i, '  '.join(row)))

    def cilent_seats(self):
        '''Method generate information about all occupied seats'''
        for row in range(1,self.size[0]+1):
            for col in range(1,self.size[1]+1):
                client = self.__seating[row][col]
                if isinstance(client, str) :
                    yield (client, row, col)

    def num_of_total_places(self):
        '''Method return number of total seats'''
        return self.size[0] * self.size[1]

    def num_of_free_places(self):
        '''Method return number of free seats'''
        return self.num_of_total_places()- self.occupated_places

    def __copy__(self):
        '''Method create copy of existing instance'''
        return Room(self.name, self.size)