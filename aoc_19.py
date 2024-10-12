from threading import Thread

from IntCodeMachine import *

# AoC 2019 Day 19
# Part 1:   129
# Part 2:
#

part1_correct = 129
part2_correct = 14040699    # 1404, 699

CURRENT_FILE = 'aoc_19_input.txt'

input_queue = Queue(10)
output_queue = Queue(10)

def is_pulled(x,y, part1_code):
    part1_cpu = IntCodeMachine(part1_code, input_queue, output_queue)
    input_queue.put_nowait(x)
    input_queue.put_nowait(y)
    part1_cpu.run_program()
    r = output_queue.get()
    output_queue.task_done()
    return r==1

MAX_COORD_1= 50
def part1(part1_code):
    (max_x, max_y) = (MAX_COORD_1,MAX_COORD_1)
    pulled=0

    for y in range(0,max_y):
        for x in range(0,max_x):
            part1_cpu = IntCodeMachine(part1_code, input_queue, output_queue)
            input_queue.put_nowait(x)
            input_queue.put_nowait(y)
            part1_cpu.run_program()
            r = output_queue.get()
            output_queue.task_done()
            if r == 1:
                pulled += 1
    return pulled






def part2(part2_code):
    input_queue = Queue(maxsize=-1)
    output_queue = Queue(maxsize=-1)

    (max_x, max_y) = (MAX_COORD_1,MAX_COORD_1)
    pulled=0
    part2_cpu = IntCodeMachine(part2_code, input_queue, output_queue)
    for y in range(0,max_y):
        for x in range(0,max_x):
            input_queue.put_nowait(x)
            input_queue.put_nowait(y)
            part2_cpu.run_program()
            r = output_queue.get()
            output_queue.task_done()
            if r == 1:
                pulled += 1


    return pulled


    return None


def main():
    print(f' AoC 2019, Day 18')

    with open(CURRENT_FILE, 'r') as input_file:
        all_file = input_file.read()

    part1_code = IntCodeMachine.parse_from_string(all_file)
    part2_code = IntCodeMachine.parse_from_string(all_file)


    print(f'\tpart 1:   ', end="")

    part1_answer = part1(part1_code)

    if part1_answer != part1_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part1_correct} ')
        print(f'\t\t Received : {part1_answer}')
    else:
        print(f'{part1_answer} \t\t\t ')

    print(f'\tpart 2:   ', end="")

    #part2_answer = part2(part2_code)
    part2_answer =None

    if part2_answer != part2_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part2_correct} ')
        print(f'\t\t Received : {part2_answer}')
    else:
        print(f'{part2_answer} \t\t\t ')


if __name__ == "__main__":
    main()
