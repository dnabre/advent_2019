
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

'''
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
'''
def key_format(k):	
	return "".join(k)

def print_map(m):
	for y in range(0,len(m[0])):
		for x in range(0,len(m)):
			print(m[x][y],end='')
		print()




class Location:
	def __init__(self,x,y,steps=0,keys=False):
		self.x = x
		self.y = y
		if(keys==False):
			self.keys = list(empty_key_string)
		else:
			self.keys = keys
		self.steps = steps

	def addKey(self,new_key):
		n = loweralpha_to_num[new_key]
		self.keys[n] = new_key

	def isGoal(self):
		if('-' in self.keys):
			return False
		else:
			return True


	def __str__(self):
		return '[{},{},{},{}]'.format(self.x,self.y,key_format(self.keys),self.steps)

	__repr__ = __str__




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


def bfs(start,map):    
	visited = []
	queue = [start]
 
	while queue:
        
		node = queue.pop(0)
		if node not in visited:
            
			visited.append(node)
 #           neighbours = graph[node]
			neighbours = expand_node(node,map,keys,doors)
			for neighbour in neighbours:
				queue.append(neighbour)

	return visited


def expand_node(node,map,keys,doors):
	x = node.x
	y = node.y
	result = list()

	up = map[x][y+1]
	down = map[x][y-1]
	left = map[x-1][y]
	right = map[x+1][y]

	for l in [up,down,left,right]:
		if(l=='#'):
			continue
		if(l=='.'):
			result = []


	return result

def fill_alpha_to_num():
	low_list = list(string.ascii_lowercase)
	up_list = list(string.ascii_uppercase)
	for i in range(0,26):
		up_ch = up_list[i]
		low_ch = low_list[i]
		loweralpha_to_num[low_ch] = i
		upperalpha_to_num[up_ch] = i
		num_to_loweralpha[i] = low_ch
		num_to_upperalpha[i] = up_ch
	return 
	

def main():
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

	fill_alpha_to_num()


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

	

	#find highest key
	for y in range(0,height):
		for x in range(0,width):
			ch = map[x][y]
			if(ch in string.ascii_lowercase):
				print(ch)
				n = loweralpha_to_num[ch]
				num_keys = max(n,num_keys)
	num_keys = num_keys + 1 #convert of 0-index into alphabet to number of letters
	empty_key_string = num_keys * '-'
	print('searching for {} keys'.format(num_keys))
	
	for y in range(0,height):
		for x in range(0,width):
			ch = map[x][y]
			if(ch == '@'):
				start_loc=Location(x,y)
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

	
#	bfs(start_loc,map)


if __name__ == "__main__":
    main()
