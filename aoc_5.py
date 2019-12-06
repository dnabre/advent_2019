import sys

# test cases for part 1
# [initial_state, final_state, input_values, output_values]
TESTS_1 = [('1,9,10,3,2,3,11,0,99,30,40,50', '3500,9,10,70,2,3,11,0,99,30,40,50',[],[]),
		('1,0,0,0,99', '2,0,0,0,99',[], []),
		('2,3,0,3,99', '2,3,0,6,99',[], []),
		('2,4,4,5,99,0', '2,4,4,5,99,9801',[],[]),
		('1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99',[],[]),
		(
			'1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,10,19,23,1,6,23,27,1,5,27,31,1,10,'
			'31,35,2,10,35,39,1,39,5,43,2,43,6,47,2,9,47,51,1,51,5,55,1,5,55,59,2,10,59,63,'
			'1,5,63,67,1,67,10,71,2,6,71,75,2,6,75,79,1,5,79,83,2,6,83,87,2,13,87,91,1,91,'
			'6,95,2,13,95,99,1,99,5,103,2,103,10,107,1,9,107,111,1,111,6,115,1,115,2,119,'
			'1,119,10,0,99,2,14,0,0',
			'5482655,12,2,2,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,60,1,10,19,64,1,6,23,66,'
			'1,5,27,67,1,10,31,71,2,10,35,284,1,39,5,285,2,43,6,570,2,9,47,1710,1,51,'
			'5,1711,1,5,55,1712,2,10,59,6848,1,5,63,6849,1,67,10,6853,2,6,71,13706,2,'
			'6,75,27412,1,5,79,27413,2,6,83,54826,2,13,87,274130,1,91,6,274132,2,13,95,'
			'1370660,1,99,5,1370661,2,103,10,5482644,1,9,107,5482647,1,111,6,5482649,1,'
			'115,2,5482651,1,119,10,0,99,2,14,0,0', [], []),
		('3,0,4,0,99', '50,0,4,0,99', [50], [50] ),
	]


def add(program, pc, _):
	num_1 = program[program[pc + 1]]
	num_2 = program[program[pc + 2]]
	loc = program[pc + 3]
	result = num_1 + num_2
	program[loc] = result
	return []



def multiple(program,pc,_):
	num_1 = program[program[pc + 1]]
	num_2 = program[program[pc + 2]]
	loc = program[pc + 3]
	result = num_1 * num_2
	program[loc] = result
	return []

def input(program, pc, inputs):
	loc = program[pc+1]
	in_value = inputs.pop(0)
	program[loc] = in_value
	return []

def output(program, pc, _):
	loc = program[pc+1]
	out_value = program[loc]
	return [out_value]


def halt(program,pc, _):
	# This code should never be run
	print("halt instruction executed instead of program being halted")
	assert(False)
	# no return



def run_program(program, inputs):
	""" Runs program returns final state
	:param program: list of integers representing the program/initial state
	:param input: list of integers which will provided to the program when it requests input
	:return: state of memory when program halts
	"""
	pc = 0
	outputs = []
	while True :
		# bit over engineered...
		op_code = {
			1: add,
			2: multiple,
			3: input,
			4: output,
			99: halt,
		}

		pc_shift = {
			add: 4,
			multiple: 4,
			input: 2,
			output: 2,
			halt: 0
		}

		instruction = program[pc]


		operator = op_code.get(instruction)
		if (operator == halt): return (program,outputs)

#		print(f'operator={operator} \t program={program} \t pc={pc} \t inputs={inputs}')

#		print(f'inputs={inputs} \t outputs={outputs}')

		op_output = operator(program,pc,inputs)
		outputs += op_output

#		print(f'inputs={inputs} \t outputs={outputs}')

		pc_increment = pc_shift.get(operator)
		pc += pc_increment
	#no return



def string_to_program(s):
	array_strings = s.split(',')
	# should be a way to map int() over the array
	prog = [int(ch) for ch in array_strings]
	return prog


def main():
	print('running examples')

	for t in TESTS_1:
		print(f'\n{t}')
		(test_prog, test_prog_expected, test_inputs, test_outputs) = t
		test_prog = string_to_program(test_prog)
		print('', end='\t')
		print(test_prog, end=' ')

		test_prog_expected = string_to_program(test_prog_expected)
		(test_result,program_outputs) = run_program(test_prog, test_inputs)
		print(f' -> {test_result}', end=' ')

		if (test_result != test_prog_expected):
			print(f'\n\t: error expected: {t[1]}')
			sys.exit("test failed")
		else:
			print('\n\t: correct')

	print('\n\n')




if __name__ == "__main__":
	main()
