import time

import IntCodeMachine
from IntCodeMachine import *
from threading import Thread


# AoC 2019 Day 23
# Part 1:   19359996
# Part 2:   1143330711

part1_correct = 19359996
part2_correct = 1143330711

CURRENT_FILE = 'aoc_21_input.txt'

ASCII_ART_CHARS=['@','#','.']

# Example showes we can jump 1-3 but not 4.
# Jump if these is space anywhere but 4 spaces ahead.
PART1_COMMAND_QUEUE = [
"NOT A J\n",
"NOT B T\n"
"OR T J\n",
"NOT C T\n",
"OR T J\n",
"AND D J\n",
"WALK\n"
]


# Bit sad that's trivial to figure out a working strategy and
# write the code for it by hand.
PART2_COMMAND_QUEUE = [
"NOT A J\n",
"NOT B T\n",
"OR T J\n",
"NOT C T\n",
"OR T J\n",
"AND D J\n",
"NOT H T\n",
"NOT T T\n",
"OR E T\n",
"AND T J\n",
"RUN\n"
]

def put_ascii(message, in_q):
    for i in message:
        a_num = ord(i)
        in_q.put_nowait(a_num)


def get_ascii(out_q):
    out_chs=[]
    while not out_q.empty():
        num_ch = out_q.get()
        out_q.task_done()
        if chr(num_ch) in ASCII_ART_CHARS:
            print(f'Fell in hole')
            while not out_q.empty():
                print(chr(num_ch), end="")
                num_ch = out_q.get()
                out_q.task_done()
            exit(-1)
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
    return part_both(intcode_program,PART1_COMMAND_QUEUE)

def part2(intcode_program):
   # print(f'\npart 2: sending {len(PART2_COMMAND_QUEUE)} commands to part_both to execute')
    return part_both(intcode_program,PART2_COMMAND_QUEUE)

def part_both(intcode_program, command_queue):
    input_queue = Queue(maxsize=-1)
    output_queue = Queue(maxsize=-1)

    cpu = IntCodeMachine(intcode_program, input_queue, output_queue)
    worker = Thread(target=cpu.run_program,name="intcode", daemon=True)
    cpu.thread = worker
    worker.start()

    for cmd in command_queue:
        put_ascii(cmd,input_queue)

    while True:
        if output_queue.empty():
            time.sleep(0)
        num = output_queue.get()
        output_queue.task_done()
        if num < 255:
            #print(chr(num), end="")
            continue
        else:
            cpu.stop()
            worker.join()
            return num




def main():
    print(f' AoC 2019, Day 21')

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

    part2_answer = part2(part2_code)

    if part2_answer != part2_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part2_correct} ')
        print(f'\t\t Received : {part2_answer}')
    else:
        print(f'{part2_answer} \t\t\t ')


if __name__ == "__main__":
    main()
