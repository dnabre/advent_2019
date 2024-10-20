import heapq
from collections import defaultdict, deque
from string import ascii_lowercase, ascii_uppercase

# AoC 2019 Day 18
# Part 1:
# Part 2:
#

part1_correct= 4042
part2_correct= 2014

CURRENT_FILE = 'aoc_18_input.txt'


GRID_SIZE = 81
WALL = '#'
EMPTY= '.'


def print_grid(g):
    for y in range(len(g[0])):
        for x in range(len(g)):
            ch = g[x][y]
            print(ch, end = "")
        print()

neighbor_deltas = [(1,0), (-1,0), (0,1), (0,-1)]

def uneighbors(grid,x,y,):
    result = []
    if grid[x][y] == WALL:
        return result
    n_coords =  map(lambda d: (x+d[0],y+d[1]), neighbor_deltas)
    result = list(n_coords)
    return tuple(result)

def neighbors(grid,x,y,):
    result = []
    if grid[x][y] == WALL:
        return result
    n_coords = filter(lambda coord: grid[coord[0]][coord[1]] != WALL, map(lambda d: (x+d[0],y+d[1]), neighbor_deltas))
    result = list(n_coords)
    return tuple(result)




POI_CHARACTERS = set(['@'] + list(ascii_lowercase) + list(ascii_uppercase))

def reachable_keys(grid,sx, sy, keys):
    q = deque([(sx, sy, 0)])
    seen = set()
    d = ( (-1, 0), (1, 0), (0, -1), (0, 1) )
    while q:
        cx, cy, l = q.popleft()
        if grid[cx][cy].islower() and grid[cx][cy] not in keys:
            yield l, cx, cy, grid[cx][cy]
            continue
        for dx, dy in d:
            nx, ny = cx + dx, cy + dy
            if ((nx, ny)) in seen:
                continue
            seen.add((nx, ny))

            c = grid[ny][nx]
            if c != '#' and (not c.isupper() or c.lower() in keys):
                q.append((nx, ny, l + 1))



def part1(lines):
    print("\n part 1")


    entrance = None
    key_coords = []
    door_coords = []
    poi_value_to_coords = dict()

    grid = [['_' for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            ch = lines[y][x]

            if ch in POI_CHARACTERS:
                poi_value_to_coords[ch] = (x,y)
                if ch == '@':
                    entrance = (x,y)
                elif ch in ascii_lowercase:
                    key_coords.append((x,y))
                elif ch in ascii_uppercase:
                    door_coords.append((x,y))
                else:
                    print("unknown POI character: {}".format(ch))
                    return None
            grid[y][x] = ch
    print(entrance)
    (w,h) = (GRID_SIZE,GRID_SIZE)
    (x,y) = entrance

    pos = (
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y + 1),
    )



    allkeys = frozenset(ascii_lowercase)
#    r = reachable_keys(grid, entrance[0], entrance[1], set())
    q = [(0, pos, frozenset())]
    seen = set()
    while q:
        # distance, current pos, keys collected
        d, cpos, keys = heapq.heappop(q)
        if keys == allkeys:
            print(d)
            break
        if (cpos, keys) in seen:
            continue
        seen.add((cpos, keys))

        for (i, (cx,cy)) in enumerate(cpos):
            for l, nx, ny, key in reachable_keys(grid,cx,cy,keys):
                npos = cpos[0:i] + ((nx, ny),) + cpos[i+1:]
                heapq.heappush(q, (d+l, npos, keys | frozenset([key])))




    return None

def part2():
    return None

def main():
    print(f' AoC 2019, Day 18')



 #   print_map(map,x_max,y_max)

    print(f'\tpart 1:   ', end="")


    with open(CURRENT_FILE, 'r') as input_file:
        all_file = input_file.read()

    lines = all_file.split('\n')

    part1_answer = part1(lines)


    if part1_answer !=  part1_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part1_correct} ')
        print(f'\t\t Received : {part1_answer}')
    else:
        print(f'{part1_answer} \t\t\t ')


    print(f'\tpart 2:   ', end="")

    part2_answer = part2()

    if part2_answer != part2_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part2_correct} ')
        print(f'\t\t Received : {part2_answer}')
    else:
        print(f'{part2_answer} \t\t\t ')

