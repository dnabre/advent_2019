
import os
import collections

import string


example_1 = """\
#########
#b.A.@.a#
#########
"""

example_2 = """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""


example_3 = """\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""


example_4 = """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""


example_5 = """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""

example_steps = [8,86, 132,136,81]


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


class Location:
	def __init__(self,x,y,keys=''):
		self.x = x
		self.y = y
		self.keys = keys

	def __str__(self):
		return '[{},{},{}]'.format(self.x,self.y,key_format(self.keys))

	__repr__ = __str__


start_loc = None
keys=''
doors=''


places = set()
walls = set()
key_locations = set()
door_locations = set()

CURRENT_FILE = 'aoc_18_test_1.txt'

def process_map_by_character(inp):
	global keys
	global doors
	global key_locations
	global door_locations
	global places
	global start_loc

	x=0
	y=0

	for c in inp:
		if(c=='@'):
			start_loc= Location(x,y)
		elif(c=='\n'):
			x=0
			y = y + 1
		elif(c in string.ascii_lowercase):
			keys = keys + c
			key_locations.add(Location(x,y))
			places.add(Location(x, y))
		elif(c in string.ascii_uppercase):
			doors = doors + c
			door_locations.add(Location(x,y))
			places.add(Location(x,y))
		elif( c == '.'):
			places.add(Location(x,y))
		else:
			if(c!='#'):
				print('Error got {} in input stream. Expected #.'.format(c))
			walls.add(Location(x,y))
		x=x+1

		keys = ''.join(sorted(keys))
		doors = ''.join(sorted(keys))










def main():
	print('AOC_2019\t 18\n\n')



	with open(CURRENT_FILE, 'r') as input_file:
		all_file = input_file.read()
	print(all_file)

	process_map_by_character(all_file)

	print('start_loc:\t {}'.format(start_loc))
	print('keys:\t {}'.format(keys))
	print('doors:\t {}'.format(doors))

	print('key_locations:\t {}'.format(key_locations))
	print('door_locations:\t {}'.format(door_locations))
	print('places: \n {}'.format(places))
	print('walls: \n {}'.format(walls))





if __name__ == "__main__":
    main()
