# AoC 2019 Day 18
# Part 1:
# Part 2:
from collections import defaultdict

part1_correct = 4042
part2_correct = 2014

CURRENT_FILE = 'aoc_18_input.txt'


# def print_map(m):
#     for y in range(0, len(m[0])):
#         for x in range(0, len(m)):
#             print(m[x][y], end='')
#         print()
#

'''
Node
  key = (x,y) coordinate
  contains (nothing, key, door)
  connects to [(x,y)..... 
'''

class Node:
    def __str__(self):
        return "<N: {} @ {} neigh: {}>".format(self.value, self.coord, self.edges)

    def __init__(self, coord, value, edges):
        if value == '#':
            print(f'error Node created with value {value} (WALL) at {coord} with edges {edges}')
        self.coord = coord
        self.value = value
        self.edges = edges
        self.edge_weight = [1]*len(edges)
    def get_weighted_edge_list(self):
        result = []
        for i in range(0, len(self.edges)):
            w = self.edge_weight[i]
            e = self.edges[i]
            result.append((e, w))
        return result

def neighbors(x,y):
    return [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

GRID_SIZE = 80

WALL='#'
EMPTY='.'
KEYS=set(map(chr,range(ord('a'),ord('z')+1)))
DOORS=set(map(chr,range(ord('A'),ord('Z')+1)))




def part1(all_file):
    print()


    grid = all_file.split('\n')

    door_list = []
    key_list = []

    coord_to_node = dict()
    poi_to_node = dict()
    node_list = []
    start_node = None

    path_count = 0
    path_list = []
    for y in range(0,GRID_SIZE+1):

        for x in range(0,GRID_SIZE+1):
            ch = grid[y][x]
            if ch == '#':
                print(' ', end='')
            else:
                edges = []
                for (x1,y1) in neighbors(x,y):
                    n_ch = grid[y1][x1]
                    if n_ch is not WALL:
                        edges.append((x1,y1))
                n = Node((x,y), ch, edges)
                coord_to_node[(x,y)] = n
                node_list.append(n)
                if ch == '@':
                    print('!', end='')
                    start_node = n
                    poi_to_node[(x,y)] = n
                elif ch in KEYS:
                    print('k', end='')
                    # print(f'key : {ch} at {(x,y)}')
                    key_list.append(n)
                    # print(f'key  node {n} adding {ch} @ {(x,y)} to poi')
                    poi_to_node[ch] = n
                elif ch in DOORS:
                    print('d', end='')
                    # print(f'door: {ch} at {(x, y)}')
                    door_list.append(n)
                    # print(f'door node {n} adding {ch} @ {(x, y)} to poi')
                    poi_to_node[ch] = n
                else:
                    assert(ch == '.')
                    path_list.append(n)
                    path_count += 1
                print('.', end='')
        print()

    print(f'poi_to_node: {poi_to_node} \n len(poi_to_node: {len(poi_to_node)})')
    for k in KEYS:
        p = poi_to_node[k]
        print(f'key {k}: {p}')
    print(f'key_list  ({len(key_list)} elms): {key_list}')
    print(list(map(lambda n: n.value, key_list )))
    print(f'door_list ({len(door_list)} elms): {door_list}')
    print(list(map(lambda n: n.value, key_list)))
    print(f'path_list ({len(path_list)} elms): {path_list}')
    print(f'path_count: {path_count}, should match len(path_list): {len(path_list)}')
    print()
    print(f'startnode: {start_node}')
    print(f'\t weights: {start_node.edge_weight}')
    print(f'\t edge w/ weights: {start_node.get_weighted_edge_list()}')

    return None
def part2(all_file):
    return None


def main():
    print(f' AoC 2019, Day 18')

    with open(CURRENT_FILE, 'r') as input_file:
        all_file = input_file.read()

    print(f'\tpart 1:   ', end="")

    part1_answer = part1(all_file)
    if part1_answer != part1_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part1_correct} ')
        print(f'\t\t Received : {part1_answer}')
    else:
        print(f'{part1_answer} \t\t\t ')

    print(f'\tpart 2:   ', end="")

    part2_answer = part2(all_file)

    if part2_answer != part2_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part2_correct} ')
        print(f'\t\t Received : {part2_answer}')
    else:
        print(f'{part2_answer} \t\t\t ')


if __name__ == "__main__":
    main()
