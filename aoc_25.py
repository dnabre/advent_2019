from threading import Thread
from IntCodeMachine import *

# AoC 2019 Day 25
# Part 1:   34095120

part1_correct = 34095120
CURRENT_FILE = 'aoc_25_input.txt'

# Played game until found path. Just feed it to IntMachine
PART1_COMMAND_QUEUE = ["west\n", "take semiconductor\n", "west\n", "take planetoid\n", "west\n", "take food ration\n",
    "west\n", "take fixed point\n", "east\n", "east\n", "south\n", "east\n", "east\n", "north\n", "east\n", "north\n"]

def put_ascii(message, in_q):
    for i in message:
        a_num = ord(i)
        in_q.put_nowait(a_num)

def part1(intcode_program, command_queue):
    input_queue = Queue(maxsize=-1)
    output_queue = Queue(maxsize=-1)

    cpu = IntCodeMachine(intcode_program, input_queue, output_queue)
    worker = Thread(target=cpu.run_program, name="intcode", daemon=True)
    cpu.thread = worker
    worker.start()

    for cmd in command_queue:
        put_ascii(cmd, input_queue)

    line = []
    while not cpu.halted:
        num = output_queue.get()
        output_queue.task_done()
        if num == 10 :
            ss = "".join(line)
            if "typing" in ss:

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
    print(f'\tpart 1:   ', end="")

    part1_answer = part1(part1_code, PART1_COMMAND_QUEUE)
    if part1_answer != part1_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part1_correct} ')
        print(f'\t\t Received : {part1_answer}')
    else:
        print(f'{part1_answer} \t\t\t ')

if __name__ == "__main__":
    main()
