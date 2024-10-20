from enum import Enum
from queue import Queue
from threading import Thread
import sys
import itertools
import time
from IntCodeMachine import *

aoc_7_input = '3,8,1001,8,10,8,105,1,0,0,21,38,59,84,97,110,191,272,353,434,99999,3,9,1002,9,2,9,101,4,9,9,1002,9,2,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,5,9,9,101,5,9,9,1002,9,3,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99'


TESTS_1 = [

	('1,9,10,3,2,3,11,0,99,30,40,50', '3500,9,10,70,2,3,11,0,99,30,40,50', [], []),
	('1,0,0,0,99', '2,0,0,0,99', [], []),
	('2,3,0,3,99', '2,3,0,6,99', [], []),
	('2,4,4,5,99,0', '2,4,4,5,99,9801', [], []),
	('1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99', [], []),

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
	('3,0,4,0,99', '50,0,4,0,99', [50], [50]),
	('1002,4,3,4,33', '1002,4,3,4,99', [], []),
	('1101,100,-1,4,0', '1101,100,-1,4,99', [], []),
]

TESTS_2 = [
	('3,9,8,9,10,9,4,9,99,-1,8', '3,9,8,9,10,9,4,9,99,0,8', [4], [0]),
	('3,9,8,9,10,9,4,9,99,-1,8', '3,9,8,9,10,9,4,9,99,1,8', [8], [1]),
	('3,9,7,9,10,9,4,9,99,-1,8', '3,9,7,9,10,9,4,9,99,1,8', [3], [1]),
	('3,9,7,9,10,9,4,9,99,-1,8', '3,9,7,9,10,9,4,9,99,0,8', [8], [0]),
	('3,3,1108,-1,8,3,4,3,99', '3,3,1108,0,8,3,4,3,99', [3], [0]),
	('3,3,1108,-1,8,3,4,3,99', '3,3,1108,1,8,3,4,3,99', [8], [1]),
	('3,3,1107,-1,8,3,4,3,99', '3,3,1107,1,8,3,4,3,99', [4], [1]),
	('3,3,1107,-1,8,3,4,3,99', '3,3,1107,0,8,3,4,3,99', [10], [0]),
	('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '3,12,6,12,15,1,13,14,13,4,13,99,0,0,1,9', [0], [0]),
	('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '3,12,6,12,15,1,13,14,13,4,13,99,4,1,1,9', [4], [1]),
	('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '3,3,1105,0,9,1101,0,0,12,4,12,99,0', [0], [0]),
	('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '3,3,1105,7,9,1101,0,0,12,4,12,99,1', [7], [1]),
	(
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,3,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	[3], [999]),
	(
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1000,8,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	[8], [1000]),
	(
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1000,8,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1001,17,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	[17], [1001]),
]


def run_tests(test_set):
	for t in test_set:
		# print(f'\n{t}')
		(test_prog, test_prog_expected_string, test_inputs, test_outputs) = t
		test_prog = IntCodeMachine.parse_from_string(test_prog)
		input_queue = Queue(maxsize=0)
		for i in test_inputs:
			input_queue.put_nowait(i)
		output_queue = Queue(maxsize=0)
		cpu = IntCodeMachine(test_prog, input_queue, output_queue)
		test_results = cpu.run_program()
		program_outputs = []
		while (not output_queue.empty()):
			g = output_queue.get()
			program_outputs.append(g)
			output_queue.task_done()

		# print('', end='\t')
		# print(test_prog, end=' ')

		test_prog_expected = IntCodeMachine.parse_from_string(test_prog_expected_string)

		# print(f' -> {test_result}')
		# print(f'output={program_outputs}')

		failed = False
		if (test_results != test_prog_expected):
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

#	part1_input = '3,8,1001,8,10,8,105,1,0,0,21,38,59,84,97,110,191,272,353,434,99999,3,9,1002,9,2,9,101,4,9,9,1002,9,2,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,5,9,9,101,5,9,9,1002,9,3,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99'
	part1_input = aoc_7_input
	input_series_tuples = list(itertools.permutations([0, 1, 2, 3, 4]))
	input_series = [list(x) for x in input_series_tuples]

	max_signal = -1

	for phase_s in input_series:
		target_program = part1_input

		amp_A = IntCodeMachine.parse_from_string(target_program)
		amp_B = IntCodeMachine.parse_from_string(target_program)
		amp_C = IntCodeMachine.parse_from_string(target_program)
		amp_D = IntCodeMachine.parse_from_string(target_program)
		amp_E = IntCodeMachine.parse_from_string(target_program)

		phase_settings = phase_s.copy()

		# print(phase_settings)

#		(final_state_A, output_a) = run_program(amp_A, [phase_settings.pop(0)] + [0])
		# print(f'output_A = {output_a}')

#		(final_state_B, output_b) = run_program(amp_B, [phase_settings.pop(0)] + output_a)
		# print(f'output_B = {output_b}')

#		(final_state_C, output_c) = run_program(amp_C, [phase_settings.pop(0)] + output_b)
		# print(f'output_C = {output_c}')

#		(final_state_D, output_d) = run_program(amp_D, [phase_settings.pop(0)] + output_c)
		# print(f'output_D = {output_d}')

#		(final_state_E, output_e) = run_program(amp_E, [phase_settings.pop(0)] + output_d)
		# print(f'output_E = {output_e}')
		#print(f'Max thruster signal:{output_e} for settings {phase_s}')

#		t = output_e.pop(0)
#		if (t > max_signal):
#			(max_signal, phase_input) = (t, phase_s.copy())

#	print(f'\n\nBest Thruster Signal: {max_signal} for settings {phase_input}')
#	print(f'Solution: {max_signal}')

	print('Part 1 Tests')
	run_tests(TESTS_1)

	print('Part 2 Tests')
	run_tests(TESTS_2)



def send_phase( inputs, q_list):
	for i in range(5):
		q_list[i].put_nowait(inputs[i])


def part2(phase,code):
	# aoc7_part1()

	test_4 = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
	test_5 = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'
	phase_4 = [9, 8, 7, 6, 5]
	phase_5 = [9, 7, 8, 5, 6]

	#current_code = IntCodeMachine.parse_from_string(test_5)

	current_code = IntCodeMachine.parse_from_string(code)

	queue_a_to_b = Queue(maxsize=0)
	queue_b_to_c = Queue(maxsize=0)
	queue_c_to_d = Queue(maxsize=0)
	queue_d_to_e = Queue(maxsize=0)
	queue_e_to_a = Queue(maxsize=0)
	q_list = [queue_e_to_a, queue_a_to_b, queue_b_to_c, queue_c_to_d, queue_d_to_e, ]

	send_phase(phase, q_list)
	queue_e_to_a.put_nowait(0)

	cpu_A = IntCodeMachine(current_code, queue_e_to_a, queue_a_to_b)
	cpu_B = IntCodeMachine(current_code, queue_a_to_b, queue_b_to_c)
	cpu_C = IntCodeMachine(current_code, queue_b_to_c, queue_c_to_d)
	cpu_D = IntCodeMachine(current_code, queue_c_to_d, queue_d_to_e)
	cpu_E = IntCodeMachine(current_code, queue_d_to_e, queue_e_to_a)

	cpu_list = [cpu_A, cpu_B, cpu_C, cpu_D, cpu_E]
	cpu_name = ['cpu_A', 'cpu_B', 'cpu_C', 'cpu_D', 'cpu_E']
	num_threads = 5
	thread_list = []
	for i in range(num_threads):
		worker = Thread(target=cpu_list[i].run_program, name=cpu_name[i])
		cpu_list[i].thread_name = cpu_name[i]
		cpu_list[i].thread = worker
		worker.setDaemon(False)
		worker.start()
		thread_list.append(worker)
#	print("entering waits")
	for t in thread_list:
		t.join()
#	print("all threads joined")
	#time.sleep(2)
#	print("\n")
	#	for i in range(5):
	#		print(f'{cpu_name[i]} last output: {cpu_list[i].last_output}')
	for i in range(5):
		while (not q_list[i].empty()):
			result = q_list[i].get_nowait()
#			print(f'{cpu_name[i]} left in queue: {result}')
			q_list[i].task_done()
	return result


def main():

	phase_4 = [9,8,7,6,5]
	phase_5 = [9,7,8,5,6]
	code_4 ='3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
	code_5 = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'

	input_series_tuples = list(itertools.permutations([5,6,7,8,9]))
	input_series = [list(x) for x in input_series_tuples]
	max_signal = -1
	max_phase = []
	for phase_s in input_series:
		result = part2(phase_s,aoc_7_input)
#		print(f'r = {result} \t phase={phase_s}')
		if(result > max_signal):
			max_signal = result
			max_phase = phase_s


	print(f'Max Signal {max_signal} found at phase {max_phase})')
	print('Part 2 Solution: 63103596')

if __name__ == '__main__':
	main()
