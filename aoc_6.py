
from enum import Enum
import sys

AOC_6_DATA_FILENAME='aoc_6.txt'



TESTS_1 = []




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

orbits=dict()

thisdict = {
	"brand": "Ford",
	"model": "Mustang",
	"year" : 1964
}

def main():
	with open(AOC_6_DATA_FILENAME,'r') as input_file:
		lines = input_file.readlines()
		for p in lines:
			if(len(p) < 3):
				continue
			else:
				line_parts = p.split(')')
				orbits[line_parts[1][:3]] =line_parts[0][:3]
	print(f'{len(orbits)} items read')

	keys = orbits.keys()
	values = orbits.values()

	key_set = set()
	value_set = set()



	print(len(orbits.items()),end='')
	print(' total pairs')
	print(orbits.items())

	for (k,v) in orbits.items():
		print(f'orbits[{k}]={v}')
		key_set.add(k)
		value_set.add(v)



	entities = key_set.union(value_set)


	print(f'{len(key_set)} keys, {len(value_set)} values, {len(entities)} entities')






if __name__ == '__main__':
	main()

