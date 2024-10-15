import time
from threading import Thread

import IntCodeMachine
from IntCodeMachine import *

# AoC 2019 Day 25
# Part 1:   34095120
# Part 2:

part1_correct = 34095120
part2_correct = None

CURRENT_FILE = 'aoc_25_input.txt'

# Example showes we can jump 1-3 but not 4.
# Jump if these is space anywhere but 4 spaces ahead.
PARTO_COMMAND_QUEUE = ["NOT A J\n", "NOT B T\n"
                                    "OR T J\n", "NOT C T\n", "OR T J\n", "AND D J\n", "WALK\n"]
PART1_COMMAND_QUEUE = ["west\n", "take semiconductor\n", "west\n", "take planetoid\n", "west\n", "take food ration\n",
    "west\n", "take fixed point\n", "east\n", "east\n", "south\n", "east\n", "east\n", "north\n", "east\n", "north\n"]


def put_ascii(message, in_q):
    for i in message:
        a_num = ord(i)
        in_q.put_nowait(a_num)


def get_ascii(out_q):
    out_chs = []
    while not out_q.empty():
        num_ch = out_q.get()
        out_q.task_done()

        if num_ch > 128:
            return ("", num_ch)
        chr_ch = chr(num_ch)
        out_chs.append(chr_ch)
        if num_ch == 10:
            break
    result = ''.join(out_chs)
    return (result, -1)


def part1(intcode_program):
    #  print(f'\npart 1: sending {len(PART1_COMMAND_QUEUE)} commands to part_both to execute')
    return part_both(intcode_program, PART1_COMMAND_QUEUE)


def part2(intcode_program):
    # print(f'\npart 2: sending {len(PART2_COMMAND_QUEUE)} commands to part_both to execute')
    return part_both(intcode_program, PART2_COMMAND_QUEUE)


def part_both(intcode_program, command_queue):
    input_queue = Queue(maxsize=-1)
    output_queue = Queue(maxsize=-1)

    cpu = IntCodeMachine(intcode_program, input_queue, output_queue)
    worker = Thread(target=cpu.run_program, name="intcode", daemon=True)
    cpu.thread = worker
    worker.start()

    for cmd in command_queue:
        put_ascii(cmd, input_queue)
        # print(cmd, end="")

    num = None
    line = []
    while not cpu.halted:

        num = output_queue.get()
        output_queue.task_done()
        if num == 10 :
            # print("".join(line))
            ss = "".join(line)
            if "typing" in ss:
                # print(ss)
                parts = ss.split(" ")
                for p in parts:
                    if p.isdigit():
                        num = int(p)
                        cpu.stop()
                        worker.join()
                        return num
            line = []
        else:
            line.append(chr(num))

def main():
    print(f' AoC 2019, Day 25')

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

    # print(f'\tpart 2:   ', end="")  #  # part2_answer = part2(part2_code)  #  # if part2_answer != part2_correct:  #     print(f'\n\t\t INCORRECT ANSWER')  #     print(f'\t\t Should be: {part2_correct} ')  #     print(f'\t\t Received : {part2_answer}')  # else:  #     print(f'{part2_answer} \t\t\t ')


if __name__ == "__main__":
    main()
