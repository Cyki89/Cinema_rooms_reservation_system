
from cinema import Cinema

gornik = Cinema('Gornik')
gornik.add_room('A', (11, 11))
gornik.add_room('B', (12, 12))
gornik.movie_generator()
gornik.allocation_seat_generator()
gornik.show_main_menu()
