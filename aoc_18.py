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

'''
    BFS from the entrance point. 
    To expand from a state, check the adjacent POIs (keys, doors, entrance) reachable using keys owned by that state
    Use a priority queue, with distances to next state so we expand to closer options from each state first 
    
    
    function that expands(current_coord, have_keys) -> [list of (dist,POI)]  should be memoized
    ? should function return doors that we have the key for in its search? I think no
    
    Use bitset (https://pypi.org/project/bitsets/) or similiar to represent the current keys a state has




'''




def part1(lines):
    print()
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

