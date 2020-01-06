
import math

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
examples = [example_1,example_2,example_3,example_4,example_5]
target = example_4
AOC_18_DATA_FILENAME='aoc_18_input.txt'


def part_1_map():
	with open(AOC_18_DATA_FILENAME, 'r') as input_file:
		prob_map = input_file.readlines()
	return prob_map

def get_dims(map):
	x = len(map)
	y = len(map[0])
	return (y,x)

def map2array(map):
	result = []
	rows = map.split('\n')
	for r in rows: r = r.strip()
	rows = rows[:-1]
	for r in rows:
		new_row=[]
		for c in r:
			new_row.append(c)
#			print(c,end='')
#		print()
		result.append(new_row)
	return result

def make_paded_array(map):
	n_rows = len(map)
	n_cols = len(map[0])
	print((n_rows,n_cols))
	for r in map:
		r.append('#')
		r.insert(0,'#')	
	row_length = len(map[0])
	map.insert(0,(['#'] * row_length))
	map.append(['#'] * row_length)
	return map

def print_map(map):
	for r in map:
		for c in r:
			print(c,end='')
		print()
def coords_for(map, ch):
	x = 0
	y = 0
	for (y,r) in enumerate(map):
		
		for (x,c) in enumerate(r):
			if(c == ch):
				return (x,y)
			
		
	return (-1,-1)
def map2dict(map):
	map = make_paded_array(map)
	m = dict()
	for (y,r) in enumerate(map):
		for (x,c) in enumerate(r):
			m[(x-1,y-1)] = c
	return m

markers = '@,a,b,c,d,e,f,g,H,A,B,C,D,E,F,G,H'
def main():
	#print(target)
	map = map2array(target)
	print_map(map)	
	#print(get_dims(map))
	dims = get_dims(map)
	print(dims)
	pd_map = map2dict(map)
	
	for y in range(dims[1]):
		for x in range(dims[0]):
			c = pd_map[(x,y)]
			print(c,end='')
		print()

	

if __name__ == "__main__":
	main()