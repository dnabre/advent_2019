
import os
import collections
import string

import numpy as np

# AoC 2019 Day 18
# Part 1:
# Part 2:
#

part1_correct= 4042
part2_correct= 2014





def print_map(m):
	for y in range(0,len(m[0])):
		for x in range(0,len(m)):
			print(m[x][y],end='')
		print()


CURRENT_FILE = 'aoc_18_input.txt'



start_loc = None
keys=dict()
doors=dict()
loweralpha_to_num = dict()
upperalpha_to_num = dict()
num_to_loweralpha = dict()
num_to_upperalpha = dict()
num_keys = 0
empty_key_string = ''



def part1():
	print('AOC_2019\t 18\n\n')
	global start_loc
	global keys
	global doors
	global loweralpha_to_num
	global upperalpha_to_num
	global num_to_loweralpha
	global num_to_upperalpha
	global num_keys
	global empty_key_string




	with open(CURRENT_FILE, 'r') as input_file:
		all_file = input_file.read()
	

	map2=all_file
	
	

	
	lines = map2.split('\n')
	height = len(lines)
	width = len(lines[0])

	print((width,height))
	map=[]	
	for l in lines:
		map.append(list(l))
	
	map = [*zip(*map)]
	r=[]
	for t in map:
		r.append(list(t))
	
	map=r

	#for y in range(0,height):
	#	for x in range(0,width):
	#		print(map[x][y],end='')
	#	print()

	print_map(map)

	return None

def part2():
	return None


def main():
	print(f' AoC 2019, Day 18')

	print(f'\tpart 1:   ', end="")

	part1_answer= part1()

	if part1_answer != part1_correct:
		print(f'\n\t\t INCORRECT ANSWER')
		print(f'\t\t Should be: {part1_correct} ')
		print(f'\t\t Received : {part1_answer}')
	else:
		print(f'{part1_answer} \t\t\t ')

	print(f'\tpart 2:   ', end="")

	part2_answer = part2()

	if part2_answer != part2_correct:
		print(f'\n\t\t INCORRECT ANSWER')
		print(f'\t\t Should be: {part2_correct} ')
		print(f'\t\t Received : {part2_answer}')
	else:
		print(f'{part2_answer} \t\t\t ')





if __name__ == "__main__":
    main()
