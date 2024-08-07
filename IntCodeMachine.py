from enum import Enum
from queue import Queue
from threading import Thread



class ParamMode(Enum):
	POSITION_MODE = 0
	IMMEDIATE_MODE = 1
	RELATIVE_MODE = 2

	def __str__(self):
		if (self == ParamMode.POSITION_MODE): return 'p'
		elif (self == ParamMode.IMMEDIATE_MODE): return 'i'
		elif (self == ParamMode.RELATIVE_MODE): return 'r'
		else: raise TypeError(self)

param_modes = {
		0: 'p',
		1: 'i',
		2: 'r'
	}

def get_param_modes(instruction):
#	print(f'get_param_modes({instruction})')
	i_mid = instruction
	i_mid = i_mid // 100
	p1r = i_mid % 10
	i_mid = i_mid // 10
	p2r = i_mid % 10
	i_mid = i_mid // 10
	p3r = i_mid % 10
#	print(f' raw mode numbers : {p1r} {p2r} {p3r}')
	p1_mode = ParamMode(p1r)
	p2_mode = ParamMode(p2r)
	p3_mode = ParamMode(p3r)
	return (p1_mode, p2_mode, p3_mode)


class IntCodeMemory:
	def __init__(self, program_code):
		self.memory = program_code.copy()

	def __setitem__(self,key,value):
		if (key >= len(self.memory)):
			print(f'setting self.program[{key}] > {len(self.memory) - 1}]={value}, expand to memory[{(key - len(self.memory))}]')
			self.memory += [0] * (1+ key - len(self.memory))
		self.memory[key]=value

	def __getitem__(self,key):
		if (key >= len(self.memory)):
				print(f'getting self.program[{key} > {len(self.memory) - 1}], expand to memory[{key}]')
				self.memory += [0] * (1 + key - len(self.memory))
		return self.memory[key]

	def __str__(self):
		return self.memory.__str__()

	def asList(self):
		return self.memory

class IntCodeMachine:
	input_queue: Queue
	output_queue: Queue

	def __init__(self, initial_state, input_queue, output_queue):

		self.program = IntCodeMemory(initial_state)
		#self.program = initial_state.copy()
		self.original_state = initial_state.copy()
		self.pc = 0
		self.relative_base = 0
		self.input_queue = input_queue
		self.output_queue = output_queue
		self.thread = ()
		self.thread_name = ''
		self.last_output=()
		self.watch = False
		self.watch_list = [21107,21108]
		self.pc_shift = {
			self.add: 4,
			self.multiple: 4,
			self.input: 2,
			self.output: 2,
			self.jump_if_true: 3,
			self.jump_if_false: 3,
			self.less_than: 4,
			self.equals: 4,
			self.adj_base:2,
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
		9: self.adj_base,
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

	@staticmethod
	def code_to_string(c):
		result = ""
		for instruct in c:
			result += f'{instruct},'
		return result[:-1]




	def lookup_value(self, p_mode, p_number):
		p_m = p_mode[p_number - 1]
		if (p_m == ParamMode.POSITION_MODE):
			loc = self.program[self.pc + p_number]
			value = self.program[loc]
			print(f'position mode p_m={p_number - 1}, loc: {loc}, value: {value}, yield {value}')
		elif (p_m == ParamMode.IMMEDIATE_MODE):
			value = self.program[self.pc + p_number]
			print(f'immedate mode p_m={p_number - 1}, loc: {self.pc+p_number}, value: {value}, value {value}')
		elif (p_m == ParamMode.RELATIVE_MODE):
			loc_adjust = self.program[self.pc + p_number] + self.relative_base
			value = self.program[loc_adjust]
			print(f'relative mode p_m={p_number - 1},, loc: {loc_adjust}, value: {value} adjust: {self.program[self.pc + p_number]} rb: {self.relative_base} ')
		else:
			print(f' invalud param')
			raise Exception(f'invalid ParamMode:{p_mode}')
		return value

	def lookup_position(self, p_mode, p_number):
		p_m = p_mode[p_number - 1]
		if (p_m == ParamMode.POSITION_MODE):
			loc = self.program[self.pc + p_number]

		elif (p_m == ParamMode.IMMEDIATE_MODE):
			loc = self.pc + p_number;

		elif (p_m == ParamMode.RELATIVE_MODE):
			loc= self.program[self.pc + p_number] + self.relative_base
		else:
			print(f' invalid param')
			raise Exception(f'invalid ParamMode:{p_mode}')
		return loc

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
		mode = ''
		if(p_modes[0] == ParamMode.POSITION_MODE):
			loc = self.program[self.pc + 1]
			mode += 'p'
		elif (p_modes[0] == ParamMode.RELATIVE_MODE):
			loc = self.relative_base + self.program[self.pc + 1]
			mode += 'r'
		else:
			loc = self.program[self.pc + 1]  # location written to will never be in immediate mode
			mode += 'UNKNOWN PARAMETER MODE'

		in_value = self.input_queue.get()
		#if(self.watch):
		print(f'{self.thread_name} inputting {in_value} to {loc} p={mode}\n', end='')
		self.program[loc] = in_value
		self.pc += self.pc_shift[self.input]
		self.input_queue.task_done()
		return

	def output(self, p_modes):
		#print(f'instruction {self.program[self.pc]}, {p_modes}')
		mode=''
		if (p_modes[0] == ParamMode.POSITION_MODE):
			loc = self.program[self.pc + 1]
			mode += 'p'
			output_value = self.program[loc]
		elif (p_modes[0] == ParamMode.RELATIVE_MODE):
			loc = self.relative_base + self.program[self.pc + 1]
			output_value = self.program[loc]
			mode += 'r'
		else:
			mode += 'UNKNOWN PARAMETER MODE'
			output_value = self.lookup_value(p_modes, 1)

		#if (self.watch):
		print(f'{self.thread_name} outputting {output_value}\n', end='')
		self.output_queue.put_nowait(output_value)
		self.pc += self.pc_shift[self.output]
		return

	def jump_if_true(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		print(f'\tjnz {self.program[self.pc+1]} {self.program[self.pc+2]}, num_1: {num_1} num_2: {num_2}')
		print(f' tape[20] => {self.program[20]}')

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
		#loc = self.program[self.pc + 3]
		#loc = self.lookup_value(p_modes,3)

		if (p_modes[0] == ParamMode.POSITION_MODE):
			loc = self.program[self.pc + 1]
		elif (p_modes[0] == ParamMode.RELATIVE_MODE):
			loc = self.relative_base + self.program[self.pc + 1]
		else:
			loc = self.program[self.pc+3]

		if (num_1 < num_2):
			self.program[loc] = 1
		else:
			self.program[loc] = 0
		self.pc += self.pc_shift[self.less_than]
		return

	def equals(self, p_modes):
		print(f' p_modes: {p_modes}')
		print("tape: ", end="")
		for i in range(20):
			print(f'{self.program[i]}, ', end="")
		print()
		print(f'\t\t GOAL: teq: av:17 bv: 8 eq: False to loc: 0 to 20')
		print(f' loc[21]={self.program[21]}, loc[4]={self.program[4]}, loc[20]={self.program[20]}')
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)

		num_3 = self.lookup_position(p_modes, 3)
		print(f'using lookup, num_1: {num_1} num_2: {num_2} num_3: {num_3}')
		self.program[num_3]= int(num_1 == num_2)
		print(f'\t teq=> av: {num_1} bv: {num_2} eq: {num_1==num_2} to loc: {int(num_1==num_2)} to {num_3} ')


		self.pc += self.pc_shift[self.equals]
		return

	def adj_base(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		self.relative_base += num_1
		self.pc += self.pc_shift[self.adj_base]
		return



	def halt(self, p_modes):
		#Handle closing queues and thread shutdown
		self.pc += self.pc_shift[self.halt]
		return



	def run_program(self):
		print(f'program: {self.program}')
		while True:
		#	print(f'{self.program} \t pc={self.pc} \t rb={self.relative_base}')
			instruction = self.program[self.pc]
			print(f'pc: {self.pc} raw: {instruction}')
			if self.pc == 6:
				print(f'program: {self.program}')
			if(instruction in self.watch_list):
				self.watch = True
				#print(f'pc={self.pc} \t rb={self.relative_base} code={self.program.asList()[self.pc:]} \t ')
			p_nodes = get_param_modes(instruction)
			print(f'p_nodes: {p_nodes}')
			opcode_number = instruction % 100
			operator = self.op_code[opcode_number]
			print(f' pc: {self.pc}  opcode: {opcode_number}')
		#	if(instruction in self.watch_list):
		#		self.watch = True
		#		print(f'intrs = {instruction}  pc={self.pc}  rb={self.relative_base}  opcode = {operator} \t {p_nodes}  \t code={self.program.asList()[self.pc:self.pc+8]} ')
			operator(p_nodes)
			self.watch = False
			if(operator == self.halt):
				return self.program

	def compare_state(self, other_state):
		if(self.run_program() == other_state):
			return True
		else:
			return False


