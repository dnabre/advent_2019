import copy

# level[(z,r,c)] -> {#,.}
level = dict()

example = """\
....#
#..#.
#..##
..#..
#....
""".strip()

test = """\
12345
abcde
ABCDE
vwxyz
VWXYZ
""".strip()

problem = """\
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
			# ads = getAdjuncts(w,x,y)
			ad_bug_count = countAdjacentBugs(w, x, y)
			ch = w[x][y]
			if (ch == BUG):
				if (ad_bug_count == 1):
					n_w[x][y] = BUG
				else:
					n_w[x][y] = EMPTY
			elif (ch == EMPTY):
				if (ad_bug_count == 1) or (ad_bug_count == 2):
					n_w[x][y] = BUG
				else:
					n_w[x][y] = EMPTY
			else:
				# shouldn't happen
				raise Exception(f'encounter {ch} at {(x, y)} in world')
	return n_w


def calcBiodiversityRating(w):
	tile_i = 0
	total_bio_rating = 0
	for r in range(len(w)):
		for c in range(len(w[0])):
			if (w[r][c] == BUG):
				total_bio_rating += pow(2, tile_i)
			tile_i += 1
	return total_bio_rating


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
		result.append(['z'] * m_y)
	return result


def countAdjacentBugs(w, x, y):
	count = 0
	ads = getAdjacent(w, x, y)
	for sq in ads:
		if (sq == BUG):
			count += 1
	return count


def getAdjacent(w, x, y):
	result = []
	if (x == 0):
		if (y == 0):
			result.append(w[0][1])
			result.append(w[1][0])
		elif (y == 4):
			result.append(w[0][3])
			result.append(w[1][4])
		else:
			result.append(w[0][y - 1])
			result.append(w[0][y + 1])
			result.append(w[1][y])
	elif (x == 4):
		if (y == 0):
			result.append(w[4][1])
			result.append(w[3][0])
		elif (y == 4):
			result.append(w[4][3])
			result.append(w[3][4])
		else:
			result.append(w[4][y + 1])
			result.append(w[4][y - 1])
			result.append(w[3][y])
	elif (y == 0):
		result.append(w[x][1])
		result.append(w[x - 1][0])
		result.append(w[x + 1][0])
	elif (y == 4):
		result.append(w[x - 1][y])
		result.append(w[x][y - 1])
		result.append(w[x + 1][y])
	else:
		result.append(w[x - 1][y])
		result.append(w[x][y - 1])
		result.append(w[x][y + 1])
		result.append(w[x + 1][y])

	return result


def printNumberedWorld(w, c):
	if (c == 0):
		print('Inital state:')
	elif (c == 1):
		print('After 1 minute:')
	else:
		print(f'After {c} minutes:')
	printWorld(w)


initial_state = []
state_history = []
TARGET = problem


def part1():
	print('aoc 24 problem')

	global initial_state
	world = stringTo2DList(TARGET)
	initial_state = full_copy_world(world)
	global state_history
	state_history.append(initial_state)
	min_count = 0
	printNumberedWorld(world, min_count)
	while (min_count < 500):
		min_count += 1
		world = stepWorld(world)
		# printNumberedWorld(world,min_count)
		state_history.append(world)
		if (state_history.count(world) > 1):
			first_occurs = state_history.index(world)
			f_i = state_history.index(world)
			print(f'First repeated state at {f_i} and {min_count} minutes:')
			printWorld(world)
			print(f'With biodiversity rating of {calcBiodiversityRating(world)}')
			break


def getRightCol(l):
	results = []
	for r in range(5):
		results.append((l, r, 4))
	return results


def getLeftCol(l):
	results = []
	for r in range(5):
		results.append((l, r, 0))
	return results


def getTopRow(l):
	results = []
	for c in range(5):
		results.append((l, 0, c))
	return results


def getBottomRow(l):
	results = []
	for c in range(5):
		results.append((l, 4, c))
	return results


#	A B C D E
#	F G H I J
#	K L ? N O
#	P Q R S T
#	U V W X Y


def getAdjLocations(z, r, c):
	results = list()


	if (r == 1 or (r == 3)):  # ({G,I} or {Q,S}
		if (c == 1) or (c == 3):
			results.append((z, r - 1, c))
			results.append((z, r + 1, c))
			results.append((z, r, c - 1))
			results.append((z, r, c + 1))

	if (r == 2) and (c == 3):  # N
		results.append((z, 1, 3))
		results.append((z, 2, 4))
		results.append((z, 3, 3))
		results += getRightCol(z - 1)

	if (r == 2) and (c == 1):  # L
		results.append((z, 2, 0))
		results.append((z, 1, 1))
		results.append((z, 3, 1))
		results += getLeftCol(z - 1)

	if (r == 1) and (c == 2):  # H
		results.append((z, 0, 2))  # C
		results.append((z, 1, 1))  # G
		results.append((z, 1, 3))  # I
		results += getTopRow(z - 1)

	if (r == 3) and (c == 2):  # R
		results.append((z, 3, 3))  # S
		results.append((z, 3, 1))  # Q
		results.append((z, 4, 2))  # W
		results += getBottomRow(z - 1)

	if (r == 0):
		if (c == 1) or (c == 2) or (c == 3):  # B,C,D
			results.append((z, r, c - 1))  # left
			results.append((z, r, c + 1))  # right
			results.append((z, r + 1, c))  # down
			results.append((z + 1, 1, 2))  # H in level out
		elif (c == 0):  # A
			results.append((z, r, c + 1))  # B
			results.append((z, r + 1, c))  # F
			results.append((z+1, 2, 2))
			results.append((z + 1, 3, 3))  # S in level out
		elif (c == 4):  # E
			results.append((z, 0, 3))  # D
			results.append((z, 1, 4))  # J
			results.append((z + 1, 1, 2))  # H in level out
			results.append((z + 1, 2, 3))  # N in level out

	if (r == 4):  # bottom row
		if (c == 1) or (c == 2) or (c == 3):  # V, W, X
			results.append((z, 4, c - 1))  # left
			results.append((z, 4, c + 1))  # right
			results.append((z, 3, c))  # up
			results.append((z + 1, 3, 2))  # R in level out
		elif (c == 0):  # U
			results.append((z, 0, 3))  # P
			results.append((z, 4, 1))  # V
			results.append((z + 1, 2, 1))  # L in level out
			results.append((z + 1, 3, 2))  # R in level out
		elif (c == 4):  # Y
			results.append((z, 3, 4))  # T
			results.append((z, 4, 3))  # X
			results.append((z + 1, 2, 3))  # N in level out
			results.append((z + 1, 3, 2))  # R in level out
	if (c==0): # left col
		if (r==1) or (r==2) or (r==3): # F, K, P
			results.append((z,r-1,0)) # up
			results.append((z,r+1,0)) # down
			results.append((z,r,1))# right
			results.append((z+1, 2, 1)) #L in level out
		elif (r==0): # A
			results.append((z,0,1)) # B right
			results.append((z,1,0)), # F down
			results.append((z+1, 1,2)) # H in level out, up
			results.append((z+1, 2,1)) # L in level out, left
		elif (r==4): # U
			results.append((z,4,1)) #V, right
			results.append((z,3,0)) #P, up
			results.append((z+1, 3,2)) # R in level out, down)
			results.append((z+1, 2,1)) # L in level out, left

	if (c==4): # right col
		if (r==1) or (r==2) or (r==3): # J, O, T
			results.append((z,4,r-1)) # up
			results.append((z,4,r+1)) # down
			results.append((z,3, r)) # left
			results.append((z+1, 3,2)) # N in level out, right
		elif (r==0): # E
			results.append((z+1, 1,2))  # H in level out, up
			results.append((z, 4, r + 1))  # down
			results.append((z, 3, 0))  # left
			results.append((z + 1, 3, 2))  # N in level out, right
		elif (r==4): # Y
			results.append((z,3,4)) # T, up
			results.append((z,4,3)) # X, left
			results.append((z+1,3,2)) #N in level out, right
			results.append((z+1,3,2 )) #R in level out, down
	return results



bugs = []

def part2():
	global bugs


	global initial_state
	world = stringTo2DList(TARGET)
	initial_state = full_copy_world(world)
	for r in range(5):
		for c in range(5):
			if(r==2) and (c==2): continue
			else:
				if(world[r][c] == '#'):
					bugs.append((0,r,c))
	min_count = 0

	print(f'bug count: {len(bugs)}, {min_count} minutes elapsed')

	for t in range(200)	:
		new_bugs = []
		possible_new_bugs = []
		for b in bugs:
			(l,r,c) = b
			a_list = getAdjLocations(l,r,c)
			ad_bug_count = 0
			possible_new_bugs = add_new_locs(possible_new_bugs, a_list)
			for loc in a_list:
				if loc in bugs:
					ad_bug_count += 1
			if(ad_bug_count == 1):
				new_bugs.append(b)
		for emp_space in possible_new_bugs:
			(l,r,c) = emp_space
			a_list = getAdjLocations(l,r,c)
			ad_bug_count = 0
			for loc in a_list:
				if loc in bugs:
					ad_bug_count += 1
			if(ad_bug_count == 1) or (ad_bug_count == 2):
				new_bugs.append(emp_space)
		min_count += 1
		bugs = new_bugs

		print(f'bug count: {len(bugs)}, {min_count} minutes elapsed')

def add_new_locs(possible_locs, a_list):
	for a in a_list:
		if a in possible_locs:
			continue
		else:
			possible_locs.append(a)
	return possible_locs



def main():
	part1() # solution : 19516944
	part2() # solution : 2006


if __name__ == '__main__':
	main()




	# for z in [0]:
	# 	for r in range(5):
	# 		for c in range(5):
	# 			if (r==2) and (c==2): continue
	# 			re = getAdjLocations(z, r, c)
	# 			print(f'{(z, r, c)} [{len(re)}]:  {re}')
