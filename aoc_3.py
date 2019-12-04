import numpy as np

FILENAME = "aoc_3_input.txt"

DIRECTIONS = {
	'L':np.array([-1,0]),
	'R':np.array([1,0]),
	'U':np.array([0,1]),
	'D':np.array([0,-1])
	}

CENTRAL_PORT = np.array([0,0])

TESTS_1 = [
	('R8,U5,L5,D3\nU7,R6,D4,L4',6),
	('R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83',159),
	('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7',135)
]

def L1_from_centralPort(p1):
	return L1(p1,np_a_2_tuple(CENTRAL_PORT))

def L1( p1, p2):
	return abs(p1[0]- p2[0]) + abs(p1[1] - p2[1])	


def parse_wire(wire_pair_string):
	wp = wire_pair_string.split(',')
	wire_parts=[]
	for wps in wp:
		direction = wps[0]
		distance = int(wps[1:])
		wire_parts.append((direction,distance))
	return wire_parts

def np_a_2_tuple(np_2d_array):
	""" Convert a length 2 numpy vector into a tuple so I can stick them into an set. 
		TODO: figure out how to use numpy array in sets and the like
	"""
	x = np_2d_array[0]
	y = np_2d_array[1]
	return (x,y)

def get_steps(origin, wire_part):
	""" Convert a (distance,direction) pair in the set  of points that make up that wire
		This respresentation is horribly inefficient, but straight forward. 
		Return the complete wire offset for converting other pieces.
	"""
	steps = set()
	(direction,distance) = wire_part
	d_v = DIRECTIONS[direction]
	for s in range(distance):
		origin = np.add(origin, d_v)
		steps.add(np_a_2_tuple(origin))
	return (origin,steps)

def get_wire_steps(wire_instructions):
	current_place = CENTRAL_PORT
	steps=set()
	for wire_piece in wire_instructions:
		(offset,p_steps) = get_steps(current_place, wire_piece)
		current_place = offset
		steps.update(p_steps)
	return steps	

def parse_wire_pair(two_wire_string):
	wire_pair  = [parse_wire(w_s) for w_s in two_wire_string.split('\n')]	
	(red_pair,green_pair) = wire_pair
	(red_steps,green_steps) = (get_wire_steps(red_pair), get_wire_steps(green_pair))
	return (red_steps,green_steps) 

def get_wire_intersect_min_distance(wire_string):
	(red_steps,green_steps) = parse_wire_pair(wire_string)
	wire_intersects = red_steps.intersection(green_steps)
	dist_from_port = [L1_from_centralPort(intersect_point) for intersect_point in wire_intersects]
	return min(dist_from_port)

def main():
	print('running given examples: ', end='')
	for t in TESTS_1:
		(s, r) = t
		dist = get_wire_intersect_min_distance(s)
		assert(dist == r)
	print(' done')

	part1_problem  = open(FILENAME, "r").read()
	print(f'read part 1 problem, input length={len(part1_problem)}')
	dist = get_wire_intersect_min_distance(part1_problem)
	print(f'part 1 solution: {dist}')

if __name__ == "__main__":
	main()

