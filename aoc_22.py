import sys


AOC_22_DATA_FILENAME = 'aoc_22_input.txt'
example_1 = """\
deal with increment 7
deal into new stack
deal into new stack
"""

example_2 = """\
cut 6
deal with increment 7
deal into new stack
"""

example_3 = """\
deal with increment 7
deal with increment 9
cut -2
"""

example_4 = """\
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""
examples = [example_1, example_2, example_3, example_4]
expected_results = [
	'0 3 6 9 2 5 8 1 4 7',
	'3 0 7 4 1 8 5 2 9 6',
	'6 3 0 7 4 1 8 5 2 9',
	'9 2 5 8 1 4 7 0 3 6'
]

PROBLEM_DECK_SIZE = 10007
deck_size = PROBLEM_DECK_SIZE


def deck2string(deck):
	result = ''
	for x in range(len(deck)):
		result += f'{deck[x]} '
	result = result[:-1]
	return result


def init_deck():
	#print(f'inital_deck of size {deck_size}')
	deck = []
	for i in range(0, deck_size):
		deck.append(i)
	return deck



def deal_new_stack(deck, ignored):
	new_deck = []
	#for i in range(len(deck)):
	#	new_deck.appendleft(deck[i])

	return list(reversed(deck))


def deal_cut(deck, n):
	return deck[n:] + deck[:n]


def instruction2string(f, param):
	result = ''
	if (f == deal_new_stack):
		result += 'deal into new stack'
	elif (f == deal_cut):
		result += f'cut {param}'
	elif (f == deck_deal_inc):
		result += f'deal with increment {param}'
	else:
		raise Exception(f'error {f}:{param}')
	return result

def deck_deal_inc(deck, n):
    out = [-1 for _ in range(len(deck))]
    for i in range(len(deck)):
        pos = (i * n) % len(deck)
        out[pos] = deck[i]
    assert not any(x == -1 for x in out)
    return out



linear_transform = dict()



def parse_instructions(target):
	count = 0
	result = []
	func = None
	param = None
	target = target.strip()
	target = target.split('\n')

	global ab_by_instruction_num
	ab_by_instruction_num = []

	for line in target:
		line = line.strip()

		count += 1
		parts = line.split(' ')
		if (parts[0] == 'cut'):
			func = deal_cut
			param = int(parts[1])
			a= 1
			b= -param

		elif (parts[1] == 'with'):
			func = deck_deal_inc
			param = int(parts[3])
			a=param
			b=0


		elif (parts[1] == 'into'):
			func = deal_new_stack
			param = None
			a = -1
			b = PROBLEM_DECK_SIZE -1

		else:
			print(f'Unrecoginized instruction: {count}:{line}')
			raise Exception()
		#linear_transform[func] = (a,b)
		ins = (func, param)
		(f_z, p_z) = ins
		ab_by_instruction_num.append((a,b))

		result += [ins]
		count += 1

	print(ab_by_instruction_num)
	print(len(ab_by_instruction_num))
	print(len(result))
	return result


num_space = {
	deal_cut: '\t\t\t\t    ',
	deal_new_stack:'    \t\t',
	deck_deal_inc:'\t'

}




def cut_transform(k, i):
	return (i - k) % PROBLEM_DECK_SIZE

def new_stack_transform(k, i):
	return (PROBLEM_DECK_SIZE - 1 - i) % PROBLEM_DECK_SIZE

def increment_transform(k, i):
	return (k*i) % PROBLEM_DECK_SIZE


index_transform = {
	deal_cut: cut_transform,
	deal_new_stack: new_stack_transform,
	deck_deal_inc: increment_transform
}


opcode= {
	deal_cut: 'C',
	deal_new_stack: 'S',
	deck_deal_inc: 'I'
}


whole_ab = (1,0)



def linear_get_index(b_i, count,func):
	global whole_ab

	(r_a,r_b) = whole_ab
	(a,b) = ab_by_instruction_num[count]


	if (opcode[func] == 'S'):
		new_a = -1 * r_a
		new_b = PROBLEM_DECK_SIZE -1 - r_b
	elif(opcode[func] =='C'):
		n = -b
		new_a = r_a
		new_b = r_b  + n + PROBLEM_DECK_SIZE
	elif(opcode[func] == 'I'):
		n = a
		n = pow(n, PROBLEM_DECK_SIZE - 2, PROBLEM_DECK_SIZE)
		new_a = r_a * n
		new_b = r_b * n
	else:
		raise Exception(str(func))
	whole_ab = (new_a % PROBLEM_DECK_SIZE, new_b % PROBLEM_DECK_SIZE)





	new_index = a*b_i  + b
	print(f'b_i = {b_i}, (a,b) = {(a, b)}, f={opcode[func]}, n_i = {new_index}, m(n_i) = {new_index % PROBLEM_DECK_SIZE} ')
	new_index = new_index % PROBLEM_DECK_SIZE
	return new_index


ab_by_instruction_num = []

def run_program(prog_string):
	deck = init_deck()
	#print(f'deck is {deck[0:5]} ... {deck[(len(deck)) - 5:]}')
	prog = parse_instructions(prog_string)
	#print(len(deck))
	count = 0
	for (func, param) in prog:
		before_index = deck.index(1822)
		deck = func(deck, param)
		after_index = deck.index(1822)
		p_index = linear_get_index(before_index, count,func)

		if(p_index == after_index):
			grade = '\t*'
		else:
			grade = '\t !!!'

		print(instruction2string(func,param), end='')
		print(num_space[func], end='')
		print(f'\t index {before_index} -> {after_index}  predicted: {p_index} \t {grade}')
		count += 1
	#	print(deck2string(deck))
		print(f'problem overall (a,b) = {whole_ab}')
	return deck


test_num = 2
target = examples[test_num]
good_result = expected_results[test_num]
desk_size = PROBLEM_DECK_SIZE


def part2():
	#part 2 soluion: 49174686993380 ??
	pos = 2020
	size = 119315717514047
	iterations = 101741582076661

	with open(AOC_22_DATA_FILENAME, 'r') as input_file:
		lines = input_file.read().strip()


	increment_mul = 1
	offset_diff = 0
	# 'run' program accumlating the linear tranforms for a given index
	for cmd in lines.split('\n'):
		print(cmd)
		op, *_, n = cmd.split(' ')
		if (op == 'cut'):
			offset_diff += int(n) * increment_mul
		elif (op == 'deal') and (n == 'stack'):
			increment_mul *= -1
			offset_diff += increment_mul
		elif (op == 'deal'):
			increment_mul *= pow(int(n), size - 2, size)

		increment_mul = increment_mul % size
		offset_diff = offset_diff % size

	# calculate what would happens to index after {iterations} runs of program
	increment = pow(increment_mul, iterations, size)
	offset = offset_diff * (1 - increment) * pow((1 - increment_mul) % size, size - 2, size)
	offset = offset % size
	card = 2020 - 1
	card = (offset + card * increment) % size
	print(f'Card at position {pos} after {iterations} rounds : {card}')



def main():
	print('problem 22')
	global deck_size
	global PROBLEM_DECK_SIZE

	# deck_size= 10
	# print('Checking test cases: ', end='')
	# for i in range((len(examples))):
	# 	print(f' {i}', end='')
	# 	result = run_program(examples[i])
	# 	result_string = deck2string(result)
	# #	print(result_string)
	#
	# 	assert(result_string == expected_results[i])
	# print()
	#
	# deck_size = PROBLEM_DECK_SIZE



	prob__prog = None
	with open(AOC_22_DATA_FILENAME, 'r') as input_file:
		prob_prog = input_file.readlines()
#	print(prob_prog)
# 	part1 = ''
# 	for p in prob_prog:
# 		part1 += p
#
# 	# print('\n\n')
#
#
# 	prog = parse_instructions(part1)
# 	d = run_program(part1)
#
#
# 	#assert (deck2string(deck) == expected_results[test_num])
# 	#print(deck2string(d))
#
# 	print(f'length {len(d)}')
#
#
# 	print (f'answer is {d.index(2019)}')
# 	for i in range(len(d)):
# 		if(d[i] == 2019):
# 			print(i)
# 			break

# part 2 soluion : 49174686993380
	part2()

if __name__ == '__main__':
	main()





