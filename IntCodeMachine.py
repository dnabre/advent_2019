from enum import Enum

class ParamMode(Enum):
	POSITION_MODE = 0
	IMMEDIATE_MODE = 1

	def __str__(self):
		if (self == ParamMode.POSITION_MODE): return 'p'
		if (self == ParamMode.IMMEDIATE_MODE): return 'i'
		return 'ERROR: INVALID ParamMode'


param_modes = {
		0: 'p',
		1: 'i'
	}

def get_param_modes(instruction):
	p1_mode = ParamMode(instruction // 100 %10)
	p2_mode = ParamMode(instruction // 1000 %10)
	p3_mode = ParamMode(instruction // 10000 %10)
	return (p1_mode,p2_mode,p3_mode)



class IntCode:
	def __init__(self, initial_state, input_callback, output_callback):
		self.program = initial_state
		self.pc = 0
		self.input_callback = input_callback
		self.output_callback = output_callback

		# op_code and pc_shift should probably be class variables of some sort?
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
	#	print(f'p_m={p_m, type(p_m)}')
		if (p_m == ParamMode.POSITION_MODE):
			loc = self.program[self.pc + p_number]
			value = self.program[loc]
		elif (p_m == ParamMode.IMMEDIATE_MODE):
			value = self.program[self.pc + p_number]
		else:
			raise Exception(f'invalid ParamMode:{p_mode}')
	#	print(f'value={value} \t type(value)={type(value)}')
		return value

	def add(self, p_modes):
		print(f'pc = {self.pc}', end='')
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		loc = self.program[self.pc + 3]  # location written to will never be in immediate mode
		#print(f'num_1={num_1,type(num_1)} \t num_1={num_2,type(num_2)}')
		result = num_1 + num_2
		self.program[loc] = result
		self.pc += self.pc_shift[self.add]
		print(f' new_pc={self.pc}')
		return []

	def multiple(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		loc = self.program[self.pc + 3]  # location written to will never be in immediate mode
		result = num_1 * num_2
		self.program[loc] = result
		self.pc += self.pc_shift[self.multiple]
		return []

	def input(self, p_modes):
		loc = self.program[self.pc + 1]  # location written to will never be in immediate mode
		self.program[loc] = self.input_callback()
		self.pc += self.pc_shift[self.input]
		return []

	def output(self, p_modes):
		output_value = self.lookup_value(p_modes, 1)
		out_value = output_value
		self.pc += self.pc_shift[self.output]
		return [out_value]

	def jump_if_true(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		if (num_1 != 0):
			self.pc = num_2
		else:
			self.pc += self.pc_shift[self.jump_if_true]
		return []

	def jump_if_false(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		if (num_1 == 0):
			self.pc = num_2
		else:
			self.pc += self.pc_shift[self.jump_if_false]
		return []

	def less_than(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		loc = self.program[self.pc + 3]  # location written to will never be in immediate mode
		if (num_1 < num_2):
			self.program[loc] = 1
		else:
			self.program[loc] = 0
		self.pc += self.pc_shift[self.less_than]
		return []


	def equals(self, p_modes):
		num_1 = self.lookup_value(p_modes, 1)
		num_2 = self.lookup_value(p_modes, 2)
		loc = self.program[self.pc + 3]  # location written to will never be in immediate mode
		if (num_1 == num_2):
			self.program[loc] = 1
		else:
			self.program[loc] = 0
		self.pc += self.pc_shift[self.equals]
		return []

	def halt(self):
		# This code should never be run
		self.pc += self.pc_shift[self.halt]
		print('halt instruction executed instead of program being halted')
		assert (False)
		# no return

	def run_program(self):
		while True:
			instruction = self.program[self.pc]
			p_nodes = get_param_modes(instruction)
			print(f'p_nodes={p_nodes,type(p_nodes)}')
			opcode_number = instruction % 100

			operator = self.op_code.get(opcode_number)
			if (operator == self.halt): return []
			op_output = operator(p_nodes)
			if(op_output != []):
				self.output_callback(op_output)
		# no return

	def compare_state(self, other_state):
		if(self.run_program() == other_state):
			return True
		else:
			return False

