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

def deal_increment2(deck, n):
	assert (n > 0)
	new_deck = []
	for _ in range(0, len(deck)):
		new_deck.append(-1)
	for i in range(len(deck)):
		new_deck[(i *n) % len(deck)] = deck[i]
	return new_deck


def parse_instructions(target):
	count = 0
	result = []
	func = None
	param = None
	target = target.strip()
	target = target.split('\n')
	for line in target:
		line = line.strip()

		count += 1
		parts = line.split(' ')
		if (parts[0] == 'cut'):
			func = deal_cut
			param = int(parts[1])
		elif (parts[1] == 'with'):
			func = deck_deal_inc
			param = int(parts[3])
		elif (parts[1] == 'into'):
			func = deal_new_stack
			param = None
		else:
			print(f'Unrecoginized instruction: {count}:{line}')
			raise Exception()
		ins = (func, param)
		result += [ins]
	return result




def run_program(prog_string):
	deck = init_deck()
	#print(f'deck is {deck[0:5]} ... {deck[(len(deck)) - 5:]}')
	prog = parse_instructions(prog_string)
	#print(len(deck))
	for (func, param) in prog:
		#	print(instruction2string(func,param))
		deck = func(deck, param)

	#	print(deck2string(deck))

	return deck


test_num = 2
target = examples[test_num]
good_result = expected_results[test_num]


def main():
	print('problem 22')
	global deck_size


	deck_size= 10
	print('Checking test cases: ', end='')
	for i in range((len(examples))):
		print(f' {i}', end='')
		result = run_program(examples[i])
		result_string = deck2string(result)
	#	print(result_string)

		assert(result_string == expected_results[i])
	print()
	deck_size = PROBLEM_DECK_SIZE



	prob__prog = None
	with open(AOC_22_DATA_FILENAME, 'r') as input_file:
		prob_prog = input_file.readlines()
#	print(prob_prog)
	part1 = ''
	for p in prob_prog:
		part1 += p

	# print('\n\n')


	prog = parse_instructions(part1)
	d = run_program(part1)


	#assert (deck2string(deck) == expected_results[test_num])
	#print(deck2string(d))

	print(f'length {len(d)}')


	print (f'answer is {d.index(2019)}')
	for i in range(len(d)):
		if(d[i] == 2019):
			print(i)
			break

# part 2 soluion : 49174686993380 ??


if __name__ == '__main__':
	main()





