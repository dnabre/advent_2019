from enum import Enum
import sys

import itertools





def lookup_value(program, pc, p_mode, p_number):
	p_m = p_mode[p_number - 1]
	if (p_m == ParamMode.POSITION_MODE):
		loc = program[pc + p_number]
		value = program[loc]
	elif (p_m == ParamMode.IMMEDIATE_MODE):
		value = program[pc + p_number]
	else:
		raise Exception(f'invalid ParamMode:{p_mode}')
	return value


def add(program, pc, p_modes, inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	loc = program[pc + 3]  # location written to will never be in immediate mode
	result = num_1 + num_2
	program[loc] = result
	return ([], pc)


def multiple(program, pc, p_modes, inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	loc = program[pc + 3]  # location written to will never be in immediate mode
	result = num_1 * num_2
	program[loc] = result
	return ([], pc)

"""
def input(program, pc, p_modes, inputs):
	if (len(inputs) == 0):
		print(f'\ninput missing at pc={pc}')
		sys.exit(-1)
	loc = program[pc + 1]  # location written to will never be in immediate mode
	in_value = inputs.pop(0)
	program[loc] = in_value
	return ([], pc)
"""

def output(program, pc, p_modes, inputs):
	output_value = lookup_value(program, pc, p_modes, 1)
	out_value = output_value
	return ([out_value], pc)


def jump_if_true(program, pc, p_modes, inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	if (num_1 != 0): pc = num_2
	return ([], pc)


def jump_if_false(program, pc, p_modes, inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	if (num_1 == 0): pc = num_2
	return ([], pc)


def less_than(program, pc, p_modes, inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	loc = program[pc + 3]  # location written to will never be in immediate mode
	if (num_1 < num_2):
		program[loc] = 1
	else:
		program[loc] = 0
	return ([], pc)


def equals(program, pc, p_modes, inputs):
	num_1 = lookup_value(program, pc, p_modes, 1)
	num_2 = lookup_value(program, pc, p_modes, 2)
	loc = program[pc + 3]  # location written to will never be in immediate mode
	if (num_1 == num_2):
		program[loc] = 1
	else:
		program[loc] = 0
	return ([], pc)


def halt(program, pc, p_modes, inputs):
	# This code should never be run
	print('halt instruction executed instead of program being halted')
	assert (False)









def input(program, pc, p_modes, inputs):
	if (len(inputs) == 0):
		print(f'\ninput missing at pc={pc}')
		sys.exit(-1)
	loc = program[pc + 1]  # location written to will never be in immediate mode
	in_value = inputs.pop(0)
	program[loc] = in_value
	return ([], pc)


def input_a(program, pc, p_modes, inputs):
	#if (len(inputs) == 0):
	#	print(f'\ninput missing at pc={pc}')
	#	sys.exit(-1)
	loc = program[pc + 1]  # location written to will never be in immediate mode
	#in_value = inputs.pop(0)
	in_value = (yield)
	program[loc] = in_value
	return ([], pc)





# no return

class ParamMode(Enum):
	POSITION_MODE = 0
	IMMEDIATE_MODE = 1

	def __str__(self):
		if (self == ParamMode.POSITION_MODE): return 'p'
		if (self == ParamMode.IMMEDIATE_MODE): return 'i'
		return 'ERROR: INVALID ParamMode'


def run_program(program, inputs):
	""" Runs program returns final state
	:param program: list of integers representing the program/initial state
	:param input: list of integers which will provided to the program when it requests input
	:return: state of memory when program halts
	"""
	pc = 0
	outputs = []
	while True:
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
		# print(f'instruction={instruction}  type={type(instruction)}')
		opcode_number = instruction % 100

		p1_mode = ParamMode(instruction // 100 % 10)
		p2_mode = ParamMode(instruction // 1000 % 10)
		p3_mode = ParamMode(instruction // 10000 % 10)
		p_modes = (p1_mode, p2_mode, p3_mode)

		operator = op_code.get(opcode_number)
		if (operator == halt): return (program, outputs)

		(op_output, new_pc) = operator(program, pc, p_modes, inputs)
		if (pc == new_pc):
			pc_increment = pc_shift.get(operator)
			pc += pc_increment
		else:
			pc = new_pc

		outputs += op_output


# no return


def string_to_program(s):
	array_strings = s.split(',')
	result = []
	for string_int in array_strings:
		num = int(string_int)
		result.append(num)
	return result


def run_tests(test_set):
	for t in test_set:
		# print(f'\n{t}')
		(test_prog, test_prog_expected, test_inputs, test_outputs) = t
		test_prog = string_to_program(test_prog)
		# print('', end='\t')
		# print(test_prog, end=' ')

		test_prog_expected = string_to_program(test_prog_expected)
		(test_result, program_outputs) = run_program(test_prog, test_inputs)
		# print(f' -> {test_result}')
		# print(f'output={program_outputs}')

		failed = False
		if (test_result != test_prog_expected):
			failed = True
			print(f'error:  expected program state: {test_prog_expected}')
		if (test_outputs != program_outputs):
			failed = True
			print(f'error: expected program output: {test_outputs}')

		if failed:
			sys.exit('test failed')
		else:
			print(f'\t: correct \t {program_outputs}')







def aoc7_part1():
	test_1 = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
	test_2 = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
	test_3 = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
	input_1 = [4, 3, 2, 1, 0]
	input_2 = [0, 1, 2, 3, 4]
	input_3 = [1, 0, 4, 3, 2]

	part1_input = '3,8,1001,8,10,8,105,1,0,0,21,38,59,84,97,110,191,272,353,434,99999,3,9,1002,9,2,9,101,4,9,9,1002,9,2,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,5,9,9,101,5,9,9,1002,9,3,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99'

	input_series_tuples = list(itertools.permutations([0, 1, 2, 3, 4]))
	input_series = [list(x) for x in input_series_tuples]



	#print(f'len(input_series_tuples)={len(input_series_tuples)}')



	max_signal = -1

	for phase_s in input_series:
		target_program = part1_input

		amp_A = string_to_program(target_program)
		amp_B = string_to_program(target_program)
		amp_C = string_to_program(target_program)
		amp_D = string_to_program(target_program)
		amp_E = string_to_program(target_program)

		phase_settings = phase_s.copy()

		# print(phase_settings)

		(final_state_A, output_a) = run_program(amp_A, [phase_settings.pop(0)] + [0])
		# print(f'output_A = {output_a}')

		(final_state_B, output_b) = run_program(amp_B, [phase_settings.pop(0)] + output_a)
		# print(f'output_B = {output_b}')

		(final_state_C, output_c) = run_program(amp_C, [phase_settings.pop(0)] + output_b)
		# print(f'output_C = {output_c}')

		(final_state_D, output_d) = run_program(amp_D, [phase_settings.pop(0)] + output_c)
		# print(f'output_D = {output_d}')

		(final_state_E, output_e) = run_program(amp_E, [phase_settings.pop(0)] + output_d)
		# print(f'output_E = {output_e}')
		#print(f'Max thruster signal:{output_e} for settings {phase_s}')

		t = output_e.pop(0)
		if (t > max_signal):
			(max_signal, phase_input) = (t, phase_s.copy())

	print(f'\n\nBest Thruster Signal: {max_signal} for settings {phase_input}')
	print(f'Solution: {max_signal}')




def main():
	test_1 = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
	test_2 = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
	test_3 = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
	input_1 = [4, 3, 2, 1, 0]
	input_2 = [0, 1, 2, 3, 4]
	input_3 = [1, 0, 4, 3, 2]

	#part1_input = '3,8,1001,8,10,8,105,1,0,0,21,38,59,84,97,110,191,272,353,434,99999,3,9,1002,9,2,9,101,4,9,9,1002,9,2,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,5,9,9,101,5,9,9,1002,9,3,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99'

	aoc7_part1()


	test_4 ='3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
	test_5 = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'



	input_series_tuples = list(itertools.permutations([5,6,7,8,9]))
	input_series = [list(x) for x in input_series_tuples]



	#print(f'len(input_series_tuples)={len(input_series_tuples)}')



	max_signal = -1

	#for phase_s in input_series:
	#for phase_s in input_series:
	for x in [0]:
		phase_s = input_series.pop(0)
		target_program = test_4


		amp_A = string_to_program(target_program)
		amp_B = string_to_program(target_program)
		amp_C = string_to_program(target_program)
		amp_D = string_to_program(target_program)
		amp_E = string_to_program(target_program)

		phase_settings = phase_s.copy()

		# print(phase_settings)

		(final_state_A, output_a) = run_program(amp_A, [phase_settings.pop(0)] + [0])
		# print(f'output_A = {output_a}')

		(final_state_B, output_b) = run_program(amp_B, [phase_settings.pop(0)] + output_a)
		# print(f'output_B = {output_b}')

		(final_state_C, output_c) = run_program(amp_C, [phase_settings.pop(0)] + output_b)
		# print(f'output_C = {output_c}')

		(final_state_D, output_d) = run_program(amp_D, [phase_settings.pop(0)] + output_c)
		# print(f'output_D = {output_d}')

		(final_state_E, output_e) = run_program(amp_E, [phase_settings.pop(0)] + output_d)
		# print(f'output_E = {output_e}')
		print(f'Max thruster signal:{output_e} for settings {phase_s}')

		t = output_e.pop(0)
		if (t > max_signal):
			(max_signal, phase_input) = (t, phase_s.copy())

	#print(f'\n\nBest Thruster Signal: {max_signal} for settings {phase_input}')


if __name__ == '__main__':
	main()
