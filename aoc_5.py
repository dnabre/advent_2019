from enum import Enum
import sys

AOC_5_DATA_FILENAME="aoc_5.txt"


# test cases for part 1
# [initial_state, final_state, input_values, output_values]
TESTS_1 = [

		('1,9,10,3,2,3,11,0,99,30,40,50', '3500,9,10,70,2,3,11,0,99,30,40,50',[],[]),
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
		   ('1002,4,3,4,33', '1002,4,3,4,99', [], []),
		   ('1101,100,-1,4,0','1101,100,-1,4,99',[],[]),
	]




TESTS_2 = [
('3,9,8,9,10,9,4,9,99,-1,8', '3,9,8,9,10,9,4,9,99,0,8', [4], [0]),
('3,9,8,9,10,9,4,9,99,-1,8', '3,9,8,9,10,9,4,9,99,1,8', [8], [1]),
('3,9,7,9,10,9,4,9,99,-1,8', '3,9,7,9,10,9,4,9,99,1,8', [3],[1]),
('3,9,7,9,10,9,4,9,99,-1,8', '3,9,7,9,10,9,4,9,99,0,8', [8],[0]),
('3,3,1108,-1,8,3,4,3,99', '3,3,1108,0,8,3,4,3,99', [3],[0]),
('3,3,1108,-1,8,3,4,3,99', '3,3,1108,1,8,3,4,3,99', [8],[1]),
('3,3,1107,-1,8,3,4,3,99', '3,3,1107,1,8,3,4,3,99', [4],[1]),
('3,3,1107,-1,8,3,4,3,99', '3,3,1107,0,8,3,4,3,99', [10],[0]),
('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9','3,12,6,12,15,1,13,14,13,4,13,99,0,0,1,9',[0],[0]),
('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9','3,12,6,12,15,1,13,14,13,4,13,99,4,1,1,9',[4],[1]),
('3,3,1105,-1,9,1101,0,0,12,4,12,99,1','3,3,1105,0,9,1101,0,0,12,4,12,99,0',[0],[0]),
('3,3,1105,-1,9,1101,0,0,12,4,12,99,1','3,3,1105,7,9,1101,0,0,12,4,12,99,1',[7],[1]),
('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,3,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',[3],[999]),
('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1000,8,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',[8],[1000]),
('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1000,8,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1001,17,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',[17],[1001]),
	]

PART_1_partial = [('','',[1],[0, 0, 0, 0, 0, 0, 0, 0, 0, 14155342])]


PART_2_partial = [('','',[5],[8684145])]



def lookup_value(program,pc,p_mode, p_number):
	p_m = p_mode[p_number - 1]
	if(p_m ==ParamMode.POSITION_MODE):
		loc = program[pc+p_number]
		value = program[loc]
	elif (p_m == ParamMode.IMMEDIATE_MODE):
		value = program[pc+p_number]
	else:
		raise Exception(f"invalid ParamMode:{p_mode}")
	return value



def add(program,pc,p_modes,inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	loc = program[pc + 3] # location written to will never be in immediate mode
	result = num_1 + num_2
	program[loc] = result
	return ([],pc)



def multiple(program,pc,p_modes,inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	loc = program[pc + 3] # location written to will never be in immediate mode
	result = num_1 * num_2
	program[loc] = result
	return ([], pc)

def input(program,pc,p_modes,inputs):
	if (len(inputs) == 0 ):
		print(f'\ninput missing at pc={pc}')
		sys.exit(-1)
	loc = program[pc+1] # location written to will never be in immediate mode
	in_value = inputs.pop(0)
	program[loc] = in_value
	return ([], pc)

def output(program,pc,p_modes,inputs):
	output_value = lookup_value(program,pc,p_modes,1)
	out_value = output_value
	return ([out_value],pc)


def jump_if_true(program,pc,p_modes,inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	if (num_1 != 0): pc = num_2
	return([],pc)

def jump_if_false(program,pc,p_modes,inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	if (num_1 == 0): pc = num_2
	return([],pc)

def less_than(program,pc,p_modes,inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	loc = program[pc + 3]  # location written to will never be in immediate mode
	if(num_1 < num_2):
		program[loc] = 1
	else:
		program[loc] = 0
	return([],pc)

def equals(program,pc,p_modes,inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	loc = program[pc + 3]  # location written to will never be in immediate mode
	if (num_1 == num_2):
		program[loc] = 1
	else:
		program[loc] = 0
	return ([], pc)


def halt(program,pc,p_modes,inputs):
	# This code should never be run
	print('halt instruction executed instead of program being halted')
	assert(False)
	# no return

class ParamMode(Enum):
		POSITION_MODE  = 0
		IMMEDIATE_MODE = 1
		def __str__(self):
			if(self == ParamMode.POSITION_MODE): return 'p'
			if(self == ParamMode.IMMEDIATE_MODE): return 'i'
			return 'ERROR: INVALID ParamMode'


def run_program(program, inputs):
	""" Runs program returns final state
	:param program: list of integers representing the program/initial state
	:param input: list of integers which will provided to the program when it requests input
	:return: state of memory when program halts
	"""
	pc = 0
	outputs = []
	while True :
		op_code = {
			1: add,
			2: multiple,
			3: input,
			4: output,
			5: jump_if_true,
			6: jump_if_false,
			7: less_than,
			8: equals,

			99: halt,
		}

		pc_shift = {
			add: 4,
			multiple: 4,
			input: 2,
			output: 2,
			jump_if_true: 3,
			jump_if_false: 3,
			less_than: 4,
			equals: 4,
			halt: 0
		}

		param_modes = {
			0: 'p',
			1: 'i'
		}


		instruction = program[pc]
		opcode_number = instruction % 100

		p1_mode = ParamMode(instruction // 100 %10)
		p2_mode = ParamMode(instruction // 1000 %10)
		p3_mode = ParamMode(instruction // 10000 %10)
		p_modes = (p1_mode,p2_mode,p3_mode)

		operator = op_code.get(opcode_number)
		if (operator == halt): return (program,outputs)

		(op_output,new_pc) = operator(program,pc,p_modes,inputs)
		if(pc == new_pc):
			pc_increment = pc_shift.get(operator)
			pc += pc_increment
		else:
			pc = new_pc

		outputs += op_output
	#no return



def string_to_program(s):
	array_strings = s.split(',')
	result = []
	for string_int in array_strings:
		num = int(string_int)
		result.append(num)
	return result



def run_tests(test_set):
	for t in test_set:
		#print(f'\n{t}')
		(test_prog, test_prog_expected, test_inputs, test_outputs) = t
		test_prog = string_to_program(test_prog)
		#print('', end='\t')
		#print(test_prog, end=' ')

		test_prog_expected = string_to_program(test_prog_expected)
		(test_result, program_outputs) = run_program(test_prog, test_inputs)
		#print(f' -> {test_result}')
		#print(f'output={program_outputs}')


		failed = False
		if (test_result != test_prog_expected):
			failed = True
			print(f'error:  expected program state: {test_prog_expected}')
		if (test_outputs != program_outputs):
			failed = True
			print(f'error: expected program output: {test_outputs}')

		if failed:
			sys.exit("test failed")
		else:
			print(f'\t: correct \t {program_outputs}')



def main():
	with open(AOC_5_DATA_FILENAME,'r') as file:
		lines = file.readlines()
		PART_1=[(lines[0],lines[1],PART_1_partial[0][2],PART_1_partial[0][3])]
		PART_2 = [(lines[2], lines[3], PART_2_partial[0][2], PART_2_partial[0][3])]
		print("Part 1 Tests")
		run_tests(TESTS_1)
		print("Part 1 Problem")
		run_tests(PART_1)

		print("Part 2 Tests")
		run_tests(TESTS_2)
		print("Part 2 Problem")
		run_tests(PART_2)


if __name__ == "__main__":
	main()
