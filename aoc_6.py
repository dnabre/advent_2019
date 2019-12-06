
from enum import Enum
import sys

AOC_6_DATA_FILENAME='aoc_6.txt'



TESTS_1 = []

def direct_orbits(body, orbits, count_orbit):
	keys = orbits.keys()
	
	for k in keys:
		 v_o = orbits[k]
		 count_orbit[k] = [k,v_o]
	return

	





orbits=dict()
body = list()

count_orbit = dict()

def main():
	with open(AOC_6_DATA_FILENAME,'r') as input_file:
		lines = input_file.readlines()
		for p in lines:
			if(len(p) < 3):
				continue
			else:
				line_parts = p.split(')')
				orbits[line_parts[1][:3]] =line_parts[0][:3]
				body.append(line_parts[1][:3])
				body.append(line_parts[0][:3])
	print(f'{len(orbits)} items read')
	print(f'total bodies found: {len(body)}')
	keys = orbits.keys()
	values = orbits.values()

	key_set = set()
	value_set = set()



	print(len(orbits.items()),end='')
	print(' total pairs')
#	print(orbits.items())

	
	for (k,v) in orbits.items():
	#	print(f'orbits[{k}]={v}')
		key_set.add(k)
		value_set.add(v)
	
	body_numbers=dict()

	entities = key_set.union(value_set)
	num=0
	for e in entities:
		body_numbers[num]=e
		num+=1

	max_num = num

	for i in range(max_num):
		print(f'{i}\t: {body_numbers[i]}')

	print(f'total {max_num} objects')









if __name__ == '__main__':
	main()

