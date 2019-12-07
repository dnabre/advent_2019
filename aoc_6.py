
from enum import Enum
import sys

AOC_6_DATA_FILENAME='aoc_6.txt'
AOC_6_TEST_FILENAME='aoc_6_test.txt'

# Part 1 Solution: 247089




TESTS_1 = []

orbits=dict()

def read_orbits(filename):
	orbit_data = dict()
	with open(filename,'r') as input_file:
		lines = input_file.readlines()
		for p in lines:
			line_parts = p.split(')')
			if((len (line_parts[0]) + len(line_parts[1]) > 1)):
				orbit_data[line_parts[1].rstrip()] = line_parts[0].rstrip()
			else:
				print(f'rejecting {p}')
	print(f'{len(orbit_data)} items read')
	return orbit_data

def count_orbits(top, orbits):
	count = 0
	if top in orbits.keys():
		count += 1
		child = orbits[top]
#		print(f'{top} orbits {child}')
		count += count_orbits(child, orbits)
		return count



	else:
		return count


def count_all_orbits(orbits):
	count = 0
	for k in orbits.keys():
		num_i = count_orbits(k, orbits)
#		print(f'root {k} has {num_i} orbits')
		count += num_i
	return count


def main():
	orbits = read_orbits(AOC_6_DATA_FILENAME)
	print(orbits)
	keys = orbits.keys()
	values = orbits.values()
	print(len(orbits.items()),end='')
	print(' total pairs')

	count = count_all_orbits(orbits)
	print(f'total orbits: {count}')







if __name__ == '__main__':
	main()

