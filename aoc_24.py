import copy

example="""\
....#
#..#.
#..##
..#..
#....
""".strip()

test="""\
12345
abcde
ABCDE
vwxyz
VWXYZ
""".strip()

 

problem="""\
.#.##
.###.
##.#.
####.
##.##
""".strip()

BUG = '#'
EMPTY = '.'

'''
	Eris isn't a very large place; a scan of the entire area fits into a 5x5 grid (your puzzle input). 
	The scan shows bugs (#) and empty spaces (.).

	*A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.

	*An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.

'''

def stepWorld(w):
	n_w = emptyWorld(w)
	for x in range(len(w)):
		for y in range(len(w[0])):
			#ads = getAdjuncts(w,x,y)
			ad_bug_count = countAdjacentBugs(w,x,y)
			ch = w[x][y]
			if(ch == BUG ):
				if(ad_bug_count == 1):
					n_w[x][y] = BUG
				else:
					n_w[x][y] = EMPTY
			elif(ch == EMPTY):
				if(ad_bug_count == 1) or (ad_bug_count==2):
					n_w[x][y] = BUG
				else:
					n_w[x][y] = EMPTY
			else:
				#shouldn't happen
				raise Exception(f'encounter {ch} at {(x,y)} in world')
	return n_w




def stringTo2DList(s):
	s = s.strip()
	parts = s.split('\n')
	result = []
	for p in parts:
		result += [list(p)]
	return result

def printWorld(world):
	for line in world:
		sline = ''.join(line)
		print(sline)
	
def full_copy_world(w):
	return copy.deepcopy(w)

def emptyWorld(w):
	m_x = len(w)
	m_y = len(w[0])
	result = []
	for _ in range(m_x):
		result.append(['z'] * m_y )
	return result


def countAdjacentBugs(w, x, y):
	count = 0
	ads = getAdjacent(w,x,y)
	for sq in ads:
		if(sq == BUG):
			count += 1
	return count


def getAdjacent(w, x, y):
	result = []
	if(x==0):
		if(y==0):
			result.append(w[0][1])
			result.append(w[1][0])	
		elif(y==4):
			result.append(w[0][3])
			result.append(w[1][4])
		else: 
			result.append(w[0][y-1])
			result.append(w[0][y+1])
			result.append(w[1][y])
	elif(x==4):
		if(y==0):
			result.append(w[4][1])
			result.append(w[3][0])
		elif(y==4):
			result.append(w[4][3])
			result.append(w[3][4])	
		else:
			result.append(w[4][y+1])
			result.append(w[4][y-1])
			result.append(w[3][y])
	elif(y==0):
		result.append(w[x][1])
		result.append(w[x-1][0])
		result.append(w[x+1][0])
	elif(y==4):
		result.append(w[x-1][y])
		result.append(w[x][y-1])
		result.append(w[x+1][y])
	else:
		result.append(w[x-1][y])
		result.append(w[x][y-1])
		result.append(w[x][y+1])
		result.append(w[x+1][y])

	return result


def printNumberedWorld(w, c):
	if(c==0):
		print('Inital state:')
	elif (c==1):
		print('After 1 minute:')
	else:
		print(f'After {c} minutes:')
	printWorld(w)

initial_state = []
state_history = []
TARGET = example

def main():
	print('aoc 24 problem')

	global initial_state
	world = stringTo2DList(TARGET)
	initial_state = full_copy_world(world)
	global state_history
	state_history.append(initial_state)
	min_count = 0
	printNumberedWorld(world,min_count)
	while (min_count < 4):
		min_count += 1
		world = stepWorld(world)
		printNumberedWorld(world,min_count)
		state_history.append(world)
		if(state_history.count(world) > 1):
			first_occurs = state_history.index(world)
			print()
			print(f''	)
		




'''
Initial state:
....#
#..#.
#..##
..#..
#....

After 1 minute:
#..#.
####.
###.#
##.##
.##..
'''
if __name__ == '__main__':
	main()