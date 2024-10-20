import copy

# AoC 2019 Day 24
# Part 1:   19516944
# Part 2:   2006

part1_correct = 19516944
part2_correct = 2006

CURRENT_FILE = "aoc_24_input.txt"

# level[(z,r,c)] -> {#,.}
level = dict()

BUG = '#'
EMPTY = '.'


def step_world(w):
    n_w = empty_world(w)
    for x in range(len(w)):
        for y in range(len(w[0])):
            # ads = getAdjuncts(w,x,y)
            ad_bug_count = count_adjacent_bugs(w, x, y)
            ch = w[x][y]
            if (ch == BUG):
                if (ad_bug_count == 1):
                    n_w[x][y] = BUG
                else:
                    n_w[x][y] = EMPTY
            elif (ch == EMPTY):
                if (ad_bug_count == 1) or (ad_bug_count == 2):
                    n_w[x][y] = BUG
                else:
                    n_w[x][y] = EMPTY
            else:
                print(f'encounter {ch} at {(x, y)} in world')
                exit(-1)
    return n_w


def calc_biodiversity_rating(w):
    tile_i = 0
    total_bio_rating = 0
    for r in range(len(w)):
        for c in range(len(w[0])):
            if (w[r][c] == BUG):
                total_bio_rating += pow(2, tile_i)
            tile_i += 1
    return total_bio_rating


def string_to_2d_list(s):
    s = s.strip()
    parts = s.split('\n')
    result = []
    for p in parts:
        result += [list(p)]
    return result

def full_copy_world(w):
    return copy.deepcopy(w)


def empty_world(w):
    m_x = len(w)
    m_y = len(w[0])
    result = []
    for _ in range(m_x):
        result.append(['z'] * m_y)
    return result


def count_adjacent_bugs(w, x, y):
    count = 0
    ads = get_adjacent(w, x, y)
    for sq in ads:
        if (sq == BUG):
            count += 1
    return count


def get_adjacent(w, x, y):
    result = []
    if (x == 0):
        if (y == 0):
            result.append(w[0][1])
            result.append(w[1][0])
        elif (y == 4):
            result.append(w[0][3])
            result.append(w[1][4])
        else:
            result.append(w[0][y - 1])
            result.append(w[0][y + 1])
            result.append(w[1][y])
    elif (x == 4):
        if (y == 0):
            result.append(w[4][1])
            result.append(w[3][0])
        elif (y == 4):
            result.append(w[4][3])
            result.append(w[3][4])
        else:
            result.append(w[4][y + 1])
            result.append(w[4][y - 1])
            result.append(w[3][y])
    elif (y == 0):
        result.append(w[x][1])
        result.append(w[x - 1][0])
        result.append(w[x + 1][0])
    elif (y == 4):
        result.append(w[x - 1][y])
        result.append(w[x][y - 1])
        result.append(w[x + 1][y])
    else:
        result.append(w[x - 1][y])
        result.append(w[x][y - 1])
        result.append(w[x][y + 1])
        result.append(w[x + 1][y])
    return result


def part1(problem):
    world = string_to_2d_list(problem)
    initial_state = full_copy_world(world)
    state_history= [initial_state]
    min_count = 0
    while True:
        min_count += 1
        world = step_world(world)
        state_history.append(world)
        if (state_history.count(world) > 1):
            return calc_biodiversity_rating(world)



def get_right_col(l):
    results = []
    for r in range(5):
        results.append((l, r, 4))
    return results


def get_left_col(l):
    results = []
    for r in range(5):
        results.append((l, r, 0))
    return results


def get_top_row(l):
    results = []
    for c in range(5):
        results.append((l, 0, c))
    return results


def get_bottom_row(l):
    results = []
    for c in range(5):
        results.append((l, 4, c))
    return results


#	A B C D E
#	F G H I J
#	K L ? N O
#	P Q R S T
#	U V W X Y

def get_adj_locations(z, r, c):
    results = list()

    if (r == 1 or (r == 3)):  # ({G,I} or {Q,S}
        if (c == 1) or (c == 3):
            results.append((z, r - 1, c))
            results.append((z, r + 1, c))
            results.append((z, r, c - 1))
            results.append((z, r, c + 1))

    if (r == 2) and (c == 3):  # N
        results.append((z, 1, 3))
        results.append((z, 2, 4))
        results.append((z, 3, 3))
        results += get_right_col(z - 1)

    if (r == 2) and (c == 1):  # L
        results.append((z, 2, 0))
        results.append((z, 1, 1))
        results.append((z, 3, 1))
        results += get_left_col(z - 1)

    if (r == 1) and (c == 2):  # H
        results.append((z, 0, 2))  # C
        results.append((z, 1, 1))  # G
        results.append((z, 1, 3))  # I
        results += get_top_row(z - 1)

    if (r == 3) and (c == 2):  # R
        results.append((z, 3, 3))  # S
        results.append((z, 3, 1))  # Q
        results.append((z, 4, 2))  # W
        results += get_bottom_row(z - 1)

    if (r == 0):
        if (c == 1) or (c == 2) or (c == 3):  # B,C,D
            results.append((z, r, c - 1))  # left
            results.append((z, r, c + 1))  # right
            results.append((z, r + 1, c))  # down
            results.append((z + 1, 1, 2))  # H in level out
        elif (c == 0):  # A
            results.append((z, r, c + 1))  # B
            results.append((z, r + 1, c))  # F
            results.append((z + 1, 2, 2))
            results.append((z + 1, 3, 3))  # S in level out
        elif (c == 4):  # E
            results.append((z, 0, 3))  # D
            results.append((z, 1, 4))  # J
            results.append((z + 1, 1, 2))  # H in level out
            results.append((z + 1, 2, 3))  # N in level out

    if (r == 4):  # bottom row
        if (c == 1) or (c == 2) or (c == 3):  # V, W, X
            results.append((z, 4, c - 1))  # left
            results.append((z, 4, c + 1))  # right
            results.append((z, 3, c))  # up
            results.append((z + 1, 3, 2))  # R in level out
        elif (c == 0):  # U
            results.append((z, 0, 3))  # P
            results.append((z, 4, 1))  # V
            results.append((z + 1, 2, 1))  # L in level out
            results.append((z + 1, 3, 2))  # R in level out
        elif (c == 4):  # Y
            results.append((z, 3, 4))  # T
            results.append((z, 4, 3))  # X
            results.append((z + 1, 2, 3))  # N in level out
            results.append((z + 1, 3, 2))  # R in level out
    if (c == 0):  # left col
        if (r == 1) or (r == 2) or (r == 3):  # F, K, P
            results.append((z, r - 1, 0))  # up
            results.append((z, r + 1, 0))  # down
            results.append((z, r, 1))  # right
            results.append((z + 1, 2, 1))  # L in level out
        elif (r == 0):  # A
            results.append((z, 0, 1))  # B right
            results.append((z, 1, 0)),  # F down
            results.append((z + 1, 1, 2))  # H in level out, up
            results.append((z + 1, 2, 1))  # L in level out, left
        elif (r == 4):  # U
            results.append((z, 4, 1))  # V, right
            results.append((z, 3, 0))  # P, up
            results.append((z + 1, 3, 2))  # R in level out, down
            results.append((z + 1, 2, 1))  # L in level out, left

    if (c == 4):  # right col
        if (r == 1) or (r == 2) or (r == 3):  # J, O, T
            results.append((z, 4, r - 1))  # up
            results.append((z, 4, r + 1))  # down
            results.append((z, 3, r))  # left
            results.append((z + 1, 3, 2))  # N in level out, right
        elif (r == 0):  # E
            results.append((z + 1, 1, 2))  # H in level out, up
            results.append((z, 4, r + 1))  # down
            results.append((z, 3, 0))  # left
            results.append((z + 1, 3, 2))  # N in level out, right
        elif (r == 4):  # Y
            results.append((z, 3, 4))  # T, up
            results.append((z, 4, 3))  # X, left
            results.append((z + 1, 3, 2))  # N in level out, right
            results.append((z + 1, 3, 2))  # R in level out, down
    return results



def look_around(x, y, layer, layers):
    neightbors = []
    if y > 0:
        neightbors.append(layers[layer][y - 1][x])
    else:
        if layer != 0:
            neightbors.append(layers[layer - 1][1][2])
    if y < 4:
        neightbors.append(layers[layer][y + 1][x])
    else:
        if layer != 0:
            neightbors.append(layers[layer - 1][3][2])
    if x > 0:
        neightbors.append(layers[layer][y][x - 1])
    else:
        if layer != 0:
            neightbors.append(layers[layer - 1][2][1])
    if x < 4:
        neightbors.append(layers[layer][y][x + 1])
    else:
        if layer != 0:
            neightbors.append(layers[layer - 1][2][3])
    if x == y == 2:
        return []
    if layer != len(layers) - 1:
        if (x, y) == (2, 1):
            neightbors.extend(layers[layer + 1][0])
        if (x, y) == (2, 3):
            neightbors.extend(layers[layer + 1][-1])
        if (x, y) == (1, 2):
            neightbors.extend(i[0] for i in layers[layer + 1])
        if (x, y) == (3, 2):
            neightbors.extend(i[-1] for i in layers[layer + 1])
    return neightbors


def part2(problem):
    layers = [[[0 for _ in range(5)] for _ in range(5)],
              [[int(i == "#") for i in j] for j in problem.splitlines()],
              [[0 for _ in range(5)] for _ in range(5)], ]

    for minute in range(200):
        layers_len = len(layers)
        next_layers = [[[0 for _ in range(5)] for _ in range(5)]]
        for i in range(layers_len):
            current_layer = layers[i]
            next_grid = []
            for y in range(5):
                next_grid.append(
                    # fiddled with until it got a sensible result. no idea what it's actually doing at this point
                    [(1 if sum(look_around(x, y, i, layers)) == 1 else 0) if current_layer[y][x] == 1 else (
                        1 if sum(look_around(x, y, i, layers)) in {1, 2} else 0) for x in range(5)])
            next_layers.append(next_grid)
        next_layers.append([[0 for _ in range(5)] for _ in range(5)])
        layers = next_layers
    answer=  sum(sum(sum(row) for row in layer) for layer in layers)
    return answer


def main():
    print(f' AoC 2019, Day 24')

    with open(CURRENT_FILE, 'r') as input_file:
        all_file = input_file.read()

    problem = all_file.strip()

    print(f'\tpart 1:   ', end="")
    part1_answer = part1(problem)
    if part1_answer != part1_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part1_correct} ')
        print(f'\t\t Received : {part1_answer}')
    else:
        print(f'{part1_answer} \t\t\t ')

    print(f'\tpart 2:   ', end="")

    part2_answer = part2(problem)

    if part2_answer != part2_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part2_correct} ')
        print(f'\t\t Received : {part2_answer}')
    else:
        print(f'{part2_answer} \t\t\t ')

if __name__ == "__main__":
    main()
