from coords import *

def check_barrel(x, y):

    with open('map.txt') as file:

        rows = file.readlines()
        
        block = int(rows[y].strip()[x])
        
        return bool(block)           

def gen_blocks():

    for i in range(13):
    
        for j in range(13):

            ends = (i in (0, 12)) or (j in (0, 12))
            
            even = (i % 2 == 0) and (j % 2 == 0)

            if ends or even:

                x, y = coords_pixels((i, j))
                
                yield (x, y, 'ROCK')

            elif check_barrel(i, j):

                x, y = coords_pixels((i, j))

                yield (x, y, 'BARR')

            else:

                x, y = coords_pixels((i, j))
                
                yield (x, y, 'WALK')

def gen_players():

    start_coords = [(1, 1), (11, 11), (1, 11), (11, 1)]
    
    num_players = 4

    for ID in range(num_players):

        i = start_coords[ID][0]
        j = start_coords[ID][1]

        x, y = coords_pixels((i, j))

        yield (x, y, ID)

def gen_rail():

    for i in range(1, 12):

        if i % 2 != 0:

            yield i
