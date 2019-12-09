from enum import Enum
from queue import Queue
from threading import Thread

class ParamMode(Enum):
	POSITION_MODE = 0
	IMMEDIATE_MODE = 1

	def __str__(self):
		if (self == ParamMode.POSITION_MODE): return 'p'
		elif (self == ParamMode.IMMEDIATE_MODE): return 'i'
		else: raise TypeError(self)

param_modes = {
		0: 'p',
		1: 'i'
	}

def get_param_modes(instruction):
	p1_mode = ParamMode(instruction // 100 %10)
	p2_mode = ParamMode(instruction // 1000 %10)
	p3_mode = ParamMode(instruction // 10000 %10)
	return (p1_mode,p2_mode,p3_mode)

class IntCodeMachine:
	input_queue: Queue
	output_queue: Queue

	def __init__(self, initial_state, input_queue, output_queue):
		self.program = initial_state.copy()
		self.original_state = initial_state.copy()
		self.pc = 0
		self.input_queue = input_queue
		self.output_queue = output_queue
		self.thread = ()
		self.thread_name = ''
		self.last_output=()
		self.pc_shift = {
			self.add: 4,
			self.multiple: 4,
			self.input: 2,
			self.output: 2,
			self.jump_if_true: 3,
			self.jump_if_false: 3,
			self.less_than: 4,
			self.equals: 4,
			self.halt: 0
		}
		self.op_code = {
		1: self.add,
		2: self.multiple,
		3: self.input,
		4: self.output,
		5: self.jump_if_true,
		6: self.jump_if_false,
		7: self.less_than,
		8: self.equals,
		99: self.halt,
		}

	@staticmethod
	def parse_from_string(s):
		array_strings = s.split(',')
		result = []
		for string_int in array_strings:
			num = int(string_int.strip().rstrip())
			result.append(num)
		return result

	def lookup_value(self, p_mode, p_number):
		p_m = p_mode[p_number - 1]
		if (p_m == ParamMode.POSITION_MODE):
			loc = self.program[self.pc + p_number]
			value = self.program[loc]
		elif (p_m == ParamMode.IMMEDIATE_MODE):
			value = self.program[self.pc + p_number]
		else:
			raise Exception(f'invalid ParamMode:{p_mode}')
		return value

	def add(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		loc = self.program[self.pc + 3]  # location written to will never be in immediate mode
		result = num_1 + num_2
		self.program[loc] = result
		self.pc += self.pc_shift[self.add]
		return

	def multiple(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		loc = self.program[self.pc + 3]  # location written to will never be in immediate mode
		result = num_1 * num_2
		self.program[loc] = result
		self.pc += self.pc_shift[self.multiple]
		return

	def input(self, p_modes):
		loc = self.program[self.pc + 1]  # location written to will never be in immediate mode
		in_value = self.input_queue.get()
		self.program[loc] = in_value
		self.pc += self.pc_shift[self.input]
		self.input_queue.task_done()
		return

	def output(self, p_modes):
		output_value = self.lookup_value(p_modes, 1)
		self.last_output=output_value
		#print(f'{self.thread_name} outputting {output_value}\n', end='')
		self.output_queue.put_nowait(output_value)
		self.pc += self.pc_shift[self.output]
		return

	def jump_if_true(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		if (num_1 != 0):
			self.pc = num_2
		else:
			self.pc += self.pc_shift[self.jump_if_true]
		return

	def jump_if_false(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		if (num_1 == 0):
			self.pc = num_2
		else:
			self.pc += self.pc_shift[self.jump_if_false]
		return

	def less_than(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		loc = self.program[self.pc + 3]  # location written to will never be in immediate mode
		if (num_1 < num_2):
			self.program[loc] = 1
		else:
			self.program[loc] = 0
		self.pc += self.pc_shift[self.less_than]
		return

	def equals(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		loc = self.program[self.pc + 3]  # location written to will never be in immediate mode
		if (num_1 == num_2):
			self.program[loc] = 1
		else:
			self.program[loc] = 0
		self.pc += self.pc_shift[self.equals]
		return

	def halt(self, p_modes):
		#Handle closing queues and thread shutdown
		self.pc += self.pc_shift[self.halt]
		return

	def run_program(self):
		while True:
			instruction = self.program[self.pc]
			p_nodes = get_param_modes(instruction)
			opcode_number = instruction % 100
			operator = self.op_code[opcode_number]
			operator(p_nodes)
			if(operator == self.halt):
				return self.program

	def compare_state(self, other_state):
		if(self.run_program() == other_state):
			return True
		else:
			return False


