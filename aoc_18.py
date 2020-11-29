
import os
import collections

import string


example_1 = """\
#########
#b.A.@.a#
#########"""

example_2 = """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""


example_3 = """\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""


example_4 = """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""


example_5 = """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

example_steps = [8,86, 132,136,81]

currect_map = example_1

def key_format(k):
	if(k==''):
		return '-'*len(keys)
	r = ''
	for i in keys:
		if(i in k):
			r = r + i
		else:
			r = r + '-'
	return r

def print_map(m):
	for y in range(0,len(m[0])):
		for x in range(0,len(m)):
			print(m[x][y],end='')
		print()




class Location:
	def __init__(self,x,y,keys=''):
		self.x = x
		self.y = y
		self.keys = keys

	def __str__(self):
		return '[{},{},{}]'.format(self.x,self.y,key_format(self.keys))

	__repr__ = __str__




CURRENT_FILE = 'aoc_18_input.txt'



start_loc = None
keys=dict()
doors=dict()



def main():
	print('AOC_2019\t 18\n\n')
	global start_loc
	global keys
	global doors
	
	
	
	with open(CURRENT_FILE, 'r') as input_file:
		all_file = input_file.read()
	
	map2 = example_1
	#map2=all_file
	
	
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

	for y in range(0,height):
		for x in range(0,width):
			ch = map[x][y]
			if(ch == '@'):
				start_loc=(x,y)
				map[x][y]='.'			
			if(ch in string.ascii_lowercase):
				keys[(x,y)] = ch
				map[x][y]='.'
			if(ch in string.ascii_uppercase):
				doors[(x,y,)] = ch
				map[x][y]='.'


	print_map(map)
	print('start: {}'.format(start_loc))
	print('keys : {}'.format(keys))
	print('doors: {}'.format(doors))



if __name__ == "__main__":
    main()
