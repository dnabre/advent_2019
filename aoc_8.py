import numpy as np




AOC_8_DATA_FILENAME = 'aoc_8_input.txt'
AOC_8_TEST_FILENAME = 'aoc_8_test.txt'
AOC_8_TEST_P2_FILENAME = 'aoc_8_test2.txt'


DATA_IMAGE_SIZE=(25,6)
TEST_IMAGE_SIZE=(3,2)
TEST_PART2_SIZE=(2,2)

INPUT_DATA = (DATA_IMAGE_SIZE, AOC_8_DATA_FILENAME)
TEST_DATA = (TEST_IMAGE_SIZE, AOC_8_TEST_FILENAME)
TEST_PART2_DATA = (TEST_PART2_SIZE, AOC_8_TEST_P2_FILENAME)

(CURRENT_SIZE, CURRENT_FILE) = INPUT_DATA

def combine_flat_layer(layer, result):
	assert(len(layer) == len(result))
	ret = result.copy()
	for i in (range(len(layer))):
		if(layer[i] != 2):
			ret[i] = layer[i]
		else:
			ret[i] = result[i]
	return ret


def list_to_ints(data):
	result = []
	for x in data:
		result.append(int(x))
	return result

def get_rows(data):
	list_nums = []
	for i in data:
		list_nums.append(int(i))
	return  group_list_by(list_nums, CURRENT_SIZE[0])



def get_cols(rows):
	return group_list_by(rows, CURRENT_SIZE[1])

def print_row(row):
	for i in row:
		if(i==0):
			print('⬛️', end='')
		else:
			print('⬜️', end='')
	print()

def print_col(cols):
	for r in cols:
		print_row(r)

def print_all_layers(layers):
	num_layers = len(layers)
	for i in range(num_layers):
		print_single_layer(layers[i], i+1)


def count_number_occurs_in_layer(layers, num):
	count = 0
	for r in layers:
		for i in r:
			if(i==num):
				count += 1
	return count


def print_single_layer(layer, layer_num):
	print(f'Layer {layer_num}:')
	for i in layer:
		print_row(i)


def group_list_by(data, num):
	return [data[i:i+num] for i in range(0, len(data), num)]


def string_to_num(row):
	return row

def data_to_layers(data):
	rows = get_rows(data)
	layers = get_cols(rows)
	return layers

def main():
	print("AOC 8")
	with open(CURRENT_FILE, 'r') as input_file:
		all_file = input_file.read()
	all_file = all_file.rstrip()


	print(all_file[0:1024])
	(SIZE_WIDE,SIZE_TALL) = CURRENT_SIZE
#	rows = get_rows(all_file)
#	layers = get_cols(rows)
	layers = data_to_layers(all_file)

	print(f'Data size: {len(all_file)} for {len(layers)} of {SIZE_WIDE}x{SIZE_TALL}')

	z_counts = [count_number_occurs_in_layer(c,0) for c in layers]
	#print(z_counts)

	fewest_zeros = SIZE_TALL * SIZE_WIDE + 1
	fewest_layer = []
	fewest_layer_num = -1
	for i in range(len(z_counts)):
		if(z_counts[i] < fewest_zeros):
			fewest_zeros = z_counts[i]
			fewest_layer = layers[i]
			fewest_layer_num = i +1

	#print(f'fewest_layer is Layer {fewest_layer_num} = {fewest_layer} with {fewest_zeros} zeroes')

	#print_single_layer(fewest_layer, 1)
	num_of_ones_in_layer = count_number_occurs_in_layer(fewest_layer, 1)
	num_of_twos_in_layer = count_number_occurs_in_layer(fewest_layer, 2)
	print(f'result: {num_of_ones_in_layer * num_of_twos_in_layer}')

#	print_all_layers(layers)
	flat_layers = (group_list_by(list_to_ints(all_file),SIZE_WIDE*SIZE_TALL))[::-1]
#	print(flat_layers)

	result = [3] * SIZE_TALL * SIZE_WIDE
	for l in flat_layers:
		#print(l)
		result = combine_flat_layer(l, result)
#		print(f'{l} \t {result}')

	layers2 = data_to_layers(result)
	#print(layers2)
	print_single_layer(layers2[0], 1)
	print('RLAKF')





