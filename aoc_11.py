import sys
from collections import defaultdict

from IntCodeMachine import *
from aoc_22 import part2

aoc_11_program = '3,8,1005,8,358,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,29,1,1104,7,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,54,1,103,17,10,1,7,3,10,2,8,9,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,89,1,1009,16,10,1006,0,86,1006,0,89,1006,0,35,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,124,1,105,8,10,1,2,0,10,1,1106,5,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,158,1,102,2,10,1,109,17,10,1,109,6,10,1,1003,1,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1001,8,0,195,1006,0,49,1,101,5,10,1006,0,5,1,108,6,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,232,2,1102,9,10,1,1108,9,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1002,8,1,262,1006,0,47,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,286,1006,0,79,2,1003,2,10,2,107,0,10,1006,0,89,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,323,1006,0,51,2,5,1,10,1,6,15,10,2,1102,3,10,101,1,9,9,1007,9,905,10,1005,10,15,99,109,680,104,0,104,1,21101,838211572492,0,1,21101,0,375,0,1106,0,479,21102,1,48063328668,1,21102,386,1,0,1106,0,479,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,21679533248,1,21101,0,433,0,1105,1,479,21102,235190455527,1,1,21102,444,1,0,1106,0,479,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,837901247244,1,21102,1,467,0,1106,0,479,21101,0,709488169828,1,21102,1,478,0,1105,1,479,99,109,2,22102,1,-1,1,21102,1,40,2,21101,0,510,3,21102,1,500,0,1105,1,543,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,505,506,521,4,0,1001,505,1,505,108,4,505,10,1006,10,537,1102,1,0,505,109,-2,2106,0,0,0,109,4,2101,0,-1,542,1207,-3,0,10,1006,10,560,21101,0,0,-3,21201,-3,0,1,21202,-2,1,2,21102,1,1,3,21102,1,579,0,1105,1,584,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,607,2207,-4,-2,10,1006,10,607,21202,-4,1,-4,1106,0,675,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21101,0,626,0,1106,0,584,22101,0,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,645,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,667,22101,0,-1,1,21102,1,667,0,105,1,542,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0'


# AoC 2019 Day 11
# Part 1:   1771
# Part 2:   HGEHJHUZ
#

def aoc11_part1():
    panels = defaultdict(int)  # maps (x,y) -> 0 or 1

    part1_input = aoc_11_program
    input_queue = Queue(maxsize=-1)
    output_queue = Queue(maxsize=-1)

    part1_code = IntCodeMachine.parse_from_string(part1_input)
    part1_cpu = IntCodeMachine(part1_code, input_queue, output_queue)
    result = part1_cpu.run_paint_robot_day11_part1(panels)
    print(f'len(panels) = {len(panels)}')
    white =0 # ones
    black =0 # zeros
    total = 0
    for (x,y) in panels.keys():
        #print(f'({x},{y})')
        r = panels[(x,y)]
        total = total + 1
        if r == 1 :
            white = white + 1
        else:
            black = black + 1

    print(f'white = {white}')
    print(f'black = {black}')
    print(f'total = {total}')
    return result

def aoc11_part2():

    panels2 = defaultdict(int)  # maps (x,y) -> 0 or 1
    panels2[0,0] = 1
    part2_input = aoc_11_program
    input_queue = Queue(maxsize=-1)
    output_queue = Queue(maxsize=-1)

    part2_code = IntCodeMachine.parse_from_string(part2_input)
    part2_cpu = IntCodeMachine(part2_code, input_queue, output_queue)
    panels2 = part2_cpu.run_paint_robot_day11_part2(panels2)

    (min_x,min_y,max_x,max_y) = (0,0,0,0)
    for (x,y) in panels2.keys():
        min_x = min(min_x,x)
        min_y = min(min_y,y)
        max_x = max(max_x,x)
        max_y = max(max_y, y)

    print("----------------------------------------------")
    for y in range(0,max_y+1):
        for x in range(0,max_x+1):
            ch = "█" if  panels2[(x,y)] == 1 else " "
            print(ch, end='')
        print()
    print("----------------------------------------------")



    return "HGEHJHUZ"






def main():
    print(f' AoC 2019, Day 11')

    print(f'\tpart 1:   ', end="")
    part1_answer = aoc11_part1()
    print(part1_answer)

    print(f'\tpart 2:   ')
    part2_answer = aoc11_part2()
    print(part2_answer)




