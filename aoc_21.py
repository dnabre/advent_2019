import IntCodeMachine
from IntCodeMachine import *


# AoC 2019 Day 23
# Part 1:   21089
# Part 2:

part1_correct = 19359996
part2_correct = 1143330711

CURRENT_FILE = 'aoc_21_input.txt'

def part1(part1_code):
    return None


def part2(part2_code):
    return None



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

"""
    let swift_script = vec![
        // !c && d
        "NOT C T",
        "AND D T",
        "OR T J",

        // !a
        "NOT A T",
        "OR T J",

        "WALK",
    ];
    
        let swift_script = vec![
        // !c && d && (!f || h)
        "NOT C T",
        "AND D T",
        "OR T J",
        "NOT F T",
        "OR H T",
        "AND T J",

        // !a
        "NOT A T",
        "OR T J",

        // a && !b
        "NOT B T",
        "AND A T",
        "AND D T",
        "OR T J",

        "RUN"
    ];
"""