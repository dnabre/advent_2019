from IntCodeMachine import *

# AoC 2019 Day 23
# Part 1:   21089
# Part 2:

part1_correct = 21089
part2_correct = 16658

CURRENT_FILE = 'aoc_23_input.txt'

# input/output queues for IntCode Machine. We run IntCodeMachine a LOT but without any threads,
# So just create queues once and re-use them
input_queue = Queue(maxsize=-1)
output_queue = Queue(maxsize=-1)

NUMBER_COMPUTER=50

def part1(part1_code):
    i_qs = [None] * NUMBER_COMPUTER
    o_qs = [None] * NUMBER_COMPUTER
    cpus = [None] * NUMBER_COMPUTER
    run  = [None] * NUMBER_COMPUTER
    q_d  = [None] * NUMBER_COMPUTER

    for i in range(NUMBER_COMPUTER):
        i_qs[i] = Queue(maxsize=-1)
        i_qs[i].put_nowait(i)
        o_qs[i] = Queue(maxsize=-1)
        cpus[i] = IntCodeMachine(part1_code, i_qs[i], o_qs[i])
        cpus[i].thread_name = i
        cpus[i].networked = True
        run[i] = True


    while True:
        for i in range(NUMBER_COMPUTER):
            if  run[i]:
                run[i] = cpus[i].step_program()
            if cpus[i].net_step == 3:
                # process submitted packet
                target = o_qs[i].get_nowait()
                o_qs[i].task_done()
                x_value = o_qs[i].get_nowait()
                o_qs[i].task_done()
                y_value = o_qs[i].get_nowait()
                o_qs[i].task_done()
                if cpus[i].debug: print(f'packet from {i} to {target} X={x_value} Y={y_value}')
                if target >= NUMBER_COMPUTER:
                    if cpus[i].debug:
                        print(f'cpu {i} sent packet to non-existant address: {target}, X={x_value} Y={y_value}')
                    if target == 255:
                        return y_value
                else:
                    i_qs[target].put_nowait(x_value)
                    i_qs[target].put_nowait(y_value)
                cpus[i].net_step=0
    return None


def part2(part2_code):
   return None


def main():
    print(f' AoC 2019, Day 23')

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
