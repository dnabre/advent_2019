import sys

# test cases for part 1
TESTS_1 = [['1,9,10,3,2,3,11,0,99,30,40,50', '3500,9,10,70,2,3,11,0,99,30,40,50'],
           ['1,0,0,0,99', '2,0,0,0,99'],
           ['2,3,0,3,99', '2,3,0,6,99'],
           ['2,4,4,5,99,0', '2,4,4,5,99,9801'],
           ['1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99']]

PROBLEM_PROGRAM = ('1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,10,19,23,1,6,23,27,1,5,27,31,1,10,'
                   '31,35,2,10,35,39,1,39,5,43,2,43,6,47,2,9,47,51,1,51,5,55,1,5,55,59,2,10,59,63,'
                   '1,5,63,67,1,67,10,71,2,6,71,75,2,6,75,79,1,5,79,83,2,6,83,87,2,13,87,91,1,91,'
                   '6,95,2,13,95,99,1,99,5,103,2,103,10,107,1,9,107,111,1,111,6,115,1,115,2,119,'
                   '1,119,10,0,99,2,14,0,0')


#specified in part 2
TARGET_VALUE = 19690720


def add(op1, op2):
	return op1 + op2

def multiple(op1, op2):
	return op1*op2


def run_program(program):
	""" Runs program returns final state
	:param program: list of integers representing the program/initial state
	:return: state of memory when program halts
	"""
	pc = 0
	while (program[pc] != 99):
		#bit over engineered...
		branch = {1: add,
		          2: multiple,
		          }
		num_1 = program[program[pc+1]]
		num_2 = program[program[pc+2]]
		loc = program[pc+3]

		op = branch.get(program[pc], 'halt')

		program[loc] = op(num_1, num_2)
		pc += 4
	return program


def string_to_program(s):
	array_strings = s.split(',')
	# should be a way to map int() over the array
	prog = [int(ch) for ch in array_strings]
	return prog

def setup_program(orig_program, noun, verb):
	new_prog = orig_program.copy()
	new_prog[1] = noun
	new_prog[2] = verb
	return new_prog

def find_inputs(program, target_value):

	for noun in range(100):
		for verb in range(100):
			prog = setup_program(program, noun, verb)
			r_prog = run_program(prog)
			result = r_prog[0]
			if(result == target_value):
				return (noun, verb)
	return (-1, -1)

def main():
	print('running examples')

	for t in TESTS_1:
		test_prog = string_to_program(t[0])
		print('', end='\t')
		print(test_prog, end=' ')

		test_prog_expected = string_to_program(t[1])
		test_result = run_program(test_prog)
		print(f' -> {test_result}', end=' ')

		if(test_result != test_prog_expected):
			print(f'\t: error expected: {t[1]}')
			sys.exit("test failed")
		else:
			print('\t: correct')

	print('\n\n')

	program = string_to_program(PROBLEM_PROGRAM)
	print(program)
	#changes specified in problem
	program[1] = 12
	program[2] = 2

	result = run_program(program)
	print(result)
	print()
	print(f'result of program[0]: {result[0]}')

	print('\n\n')

	# part 2
	print('"Part 2:\n')
	program = string_to_program(PROBLEM_PROGRAM) #get a copy of the original program
	(noun, verb) = find_inputs(program, TARGET_VALUE)
	if (noun == -1):
		print("Target Value not found")
		sys.exit(-1)
	answer = 100 * noun + verb
	print(f'Found:\t noun = {noun} \t verb = {verb} \t 100 * noun + verb = {answer}')

if __name__ == "__main__":
	main()
