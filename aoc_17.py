
from collections import defaultdict
import time
from threading import Thread
from queue import Queue

from IntCodeMachine import *

# AoC 2019 Day 17
# Part 1: 5948
# Part 2:
#

aoc_17_program = '1,330,331,332,109,4374,1101,0,1182,15,1101,1467,0,24,1001,0,0,570,1006,570,36,1001,571,0,0,1001,570,-1,570,1001,24,1,24,1105,1,18,1008,571,0,571,1001,15,1,15,1008,15,1467,570,1006,570,14,21101,58,0,0,1105,1,786,1006,332,62,99,21102,333,1,1,21102,1,73,0,1105,1,579,1101,0,0,572,1102,0,1,573,3,574,101,1,573,573,1007,574,65,570,1005,570,151,107,67,574,570,1005,570,151,1001,574,-64,574,1002,574,-1,574,1001,572,1,572,1007,572,11,570,1006,570,165,101,1182,572,127,1002,574,1,0,3,574,101,1,573,573,1008,574,10,570,1005,570,189,1008,574,44,570,1006,570,158,1106,0,81,21102,340,1,1,1105,1,177,21102,477,1,1,1106,0,177,21101,514,0,1,21101,176,0,0,1105,1,579,99,21102,1,184,0,1105,1,579,4,574,104,10,99,1007,573,22,570,1006,570,165,1002,572,1,1182,21102,375,1,1,21102,211,1,0,1105,1,579,21101,1182,11,1,21102,222,1,0,1106,0,979,21102,1,388,1,21101,233,0,0,1106,0,579,21101,1182,22,1,21102,1,244,0,1106,0,979,21102,1,401,1,21102,255,1,0,1106,0,579,21101,1182,33,1,21101,266,0,0,1105,1,979,21102,1,414,1,21102,1,277,0,1106,0,579,3,575,1008,575,89,570,1008,575,121,575,1,575,570,575,3,574,1008,574,10,570,1006,570,291,104,10,21101,0,1182,1,21102,313,1,0,1106,0,622,1005,575,327,1101,1,0,575,21101,0,327,0,1106,0,786,4,438,99,0,1,1,6,77,97,105,110,58,10,33,10,69,120,112,101,99,116,101,100,32,102,117,110,99,116,105,111,110,32,110,97,109,101,32,98,117,116,32,103,111,116,58,32,0,12,70,117,110,99,116,105,111,110,32,65,58,10,12,70,117,110,99,116,105,111,110,32,66,58,10,12,70,117,110,99,116,105,111,110,32,67,58,10,23,67,111,110,116,105,110,117,111,117,115,32,118,105,100,101,111,32,102,101,101,100,63,10,0,37,10,69,120,112,101,99,116,101,100,32,82,44,32,76,44,32,111,114,32,100,105,115,116,97,110,99,101,32,98,117,116,32,103,111,116,58,32,36,10,69,120,112,101,99,116,101,100,32,99,111,109,109,97,32,111,114,32,110,101,119,108,105,110,101,32,98,117,116,32,103,111,116,58,32,43,10,68,101,102,105,110,105,116,105,111,110,115,32,109,97,121,32,98,101,32,97,116,32,109,111,115,116,32,50,48,32,99,104,97,114,97,99,116,101,114,115,33,10,94,62,118,60,0,1,0,-1,-1,0,1,0,0,0,0,0,0,1,26,26,0,109,4,2101,0,-3,587,20102,1,0,-1,22101,1,-3,-3,21101,0,0,-2,2208,-2,-1,570,1005,570,617,2201,-3,-2,609,4,0,21201,-2,1,-2,1106,0,597,109,-4,2106,0,0,109,5,1201,-4,0,629,21002,0,1,-2,22101,1,-4,-4,21102,1,0,-3,2208,-3,-2,570,1005,570,781,2201,-4,-3,652,21001,0,0,-1,1208,-1,-4,570,1005,570,709,1208,-1,-5,570,1005,570,734,1207,-1,0,570,1005,570,759,1206,-1,774,1001,578,562,684,1,0,576,576,1001,578,566,692,1,0,577,577,21102,1,702,0,1105,1,786,21201,-1,-1,-1,1105,1,676,1001,578,1,578,1008,578,4,570,1006,570,724,1001,578,-4,578,21101,731,0,0,1106,0,786,1106,0,774,1001,578,-1,578,1008,578,-1,570,1006,570,749,1001,578,4,578,21102,756,1,0,1105,1,786,1105,1,774,21202,-1,-11,1,22101,1182,1,1,21102,774,1,0,1106,0,622,21201,-3,1,-3,1105,1,640,109,-5,2106,0,0,109,7,1005,575,802,21002,576,1,-6,21001,577,0,-5,1105,1,814,21101,0,0,-1,21101,0,0,-5,21101,0,0,-6,20208,-6,576,-2,208,-5,577,570,22002,570,-2,-2,21202,-5,51,-3,22201,-6,-3,-3,22101,1467,-3,-3,2101,0,-3,843,1005,0,863,21202,-2,42,-4,22101,46,-4,-4,1206,-2,924,21101,0,1,-1,1105,1,924,1205,-2,873,21102,1,35,-4,1105,1,924,2102,1,-3,878,1008,0,1,570,1006,570,916,1001,374,1,374,1201,-3,0,895,1101,0,2,0,2101,0,-3,902,1001,438,0,438,2202,-6,-5,570,1,570,374,570,1,570,438,438,1001,578,558,922,20101,0,0,-4,1006,575,959,204,-4,22101,1,-6,-6,1208,-6,51,570,1006,570,814,104,10,22101,1,-5,-5,1208,-5,57,570,1006,570,810,104,10,1206,-1,974,99,1206,-1,974,1101,1,0,575,21101,973,0,0,1106,0,786,99,109,-7,2105,1,0,109,6,21101,0,0,-4,21101,0,0,-3,203,-2,22101,1,-3,-3,21208,-2,82,-1,1205,-1,1030,21208,-2,76,-1,1205,-1,1037,21207,-2,48,-1,1205,-1,1124,22107,57,-2,-1,1205,-1,1124,21201,-2,-48,-2,1106,0,1041,21101,-4,0,-2,1105,1,1041,21101,0,-5,-2,21201,-4,1,-4,21207,-4,11,-1,1206,-1,1138,2201,-5,-4,1059,2101,0,-2,0,203,-2,22101,1,-3,-3,21207,-2,48,-1,1205,-1,1107,22107,57,-2,-1,1205,-1,1107,21201,-2,-48,-2,2201,-5,-4,1090,20102,10,0,-1,22201,-2,-1,-2,2201,-5,-4,1103,1202,-2,1,0,1106,0,1060,21208,-2,10,-1,1205,-1,1162,21208,-2,44,-1,1206,-1,1131,1105,1,989,21101,439,0,1,1105,1,1150,21102,1,477,1,1106,0,1150,21102,1,514,1,21102,1149,1,0,1106,0,579,99,21101,0,1157,0,1105,1,579,204,-2,104,10,99,21207,-3,22,-1,1206,-1,1138,1202,-5,1,1176,2102,1,-4,0,109,-6,2105,1,0,4,9,42,1,7,1,42,1,7,1,42,1,7,1,42,1,7,1,42,1,7,1,42,11,48,1,1,1,48,1,1,1,48,1,1,1,48,7,46,1,3,1,46,1,3,1,5,11,9,7,14,1,3,1,5,1,9,1,9,1,5,1,14,1,3,1,5,1,9,1,9,1,5,1,14,1,3,1,5,1,9,1,9,1,5,1,10,11,3,1,9,1,9,1,5,1,10,1,3,1,3,1,1,1,3,1,9,1,9,1,5,1,10,1,3,11,9,1,9,1,5,1,10,1,7,1,1,1,13,1,9,1,5,1,6,13,1,1,13,1,3,13,6,1,3,1,9,1,13,1,3,1,5,1,6,11,9,1,11,13,6,1,5,1,13,1,11,1,1,1,3,1,12,1,5,1,13,1,11,1,1,7,10,1,5,1,13,1,11,1,5,1,1,1,10,1,5,1,13,1,5,13,1,1,10,1,5,1,13,1,11,1,7,1,10,1,5,1,13,13,7,1,10,1,5,1,33,1,10,7,33,1,50,1,50,1,50,1,50,1,50,1,38,13,38,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,7,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,16'

part1_correct= 5948
part2_correct= None


WALL = '#'
EMPTY = '.'
NEWLINE= '\n'
V_UP = '^'
V_DOWN = 'v'
V_LEFT = '<'
V_RIGHT = '>'

V_DIRS = [V_UP, V_DOWN, V_LEFT, V_RIGHT]

def aoc17_readmap():
    part1_input = aoc_17_program
    input_queue = Queue(maxsize=-1)
    output_queue = Queue(maxsize=-1)

    part1_code = IntCodeMachine.parse_from_string(part1_input)
    part1_cpu = IntCodeMachine(part1_code, input_queue, output_queue)
    #worker = Thread(target=part1_cpu.run_program,name="intcode", daemon=True)
    #part1_cpu.thread = worker
    #worker.start()
    part1_cpu.run_program()

    (x,y) = (0,0)
    (x_max, y_max) = (0,0)
    map  = defaultdict(lambda: EMPTY)

    while not part1_cpu.output_queue.empty():
        ch = chr(part1_cpu.output_queue.get())
        part1_cpu.output_queue.task_done()
        if ch == NEWLINE:
            y += 1
            x = 0
          #  print()
        else:
            map[(x,y)] = ch
            x_max = max(x_max, x)
            y_max = max(y_max, y)
            x += 1
           # print(ch, end="")


    print(f'map generated, max loc: {(x_max,y_max)}')
    return (map, (x_max, y_max))


def aoc17_part1(map, x_max,y_max ):
    score = 0
    for y in range(1,y_max-1):
        for x in range(1,x_max-1):
            ch = map[(x,y)]
            if ch == WALL:
                if map[(x-1,y)] == WALL and map[(x+1,y)] == WALL and map[(x,y-1)] == WALL and map[(x,(y+1))] == WALL :
                    score += x*y
    return score

def aoc17_part2():
    part2_input = aoc_17_program
    input_queue = Queue(maxsize=-1)
    output_queue = Queue(maxsize=-1)

    part2_code = IntCodeMachine.parse_from_string(part2_input)
    part2_cpu = IntCodeMachine(part2_code, input_queue, output_queue)

    return None


def main():
    print(f' AoC 2019, Day 17')

    (map, (x_max, y_max)) = aoc17_readmap()


    print(f'\tpart 1:   ', end="")

    part1_answer = aoc17_part1(map, x_max,y_max)


    if part1_answer !=  part1_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part1_correct} ')
        print(f'\t\t Received : {part1_answer}')
    else:
        print(f'{part1_answer} \t\t\t ')


    print(f'\tpart 2:   ', end="")

    part2_answer = aoc17_part2()

    if part2_answer != part2_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part2_correct} ')
        print(f'\t\t Received : {part2_answer}')
    else:
        print(f'{part2_answer} \t\t\t ')

