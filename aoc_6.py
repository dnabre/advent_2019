
from collections import defaultdict
from collections import deque


AOC_6_DATA_FILENAME = 'aoc_6.txt'
AOC_6_TEST_FILENAME = 'aoc_6_test.txt'


# Part 1 Solution: 247089



d_links = defaultdict(list)



def read_orbits(filename):
	orbit_data = dict()
	with open(filename, 'r') as input_file:
		lines = input_file.readlines()
		for p in lines:
#			print(p)
			line_parts = p.split(')')
			(a, b) = (line_parts[0].rstrip(), line_parts[1].rstrip())
			d_links[a].append(b)
			d_links[b].append(a)

			if (b == 'YOU'):
				you_orbit = a
				print(f'*YOU orbits {a}')
			elif (b == 'SAN'):
				santa_orbit = a
				print(f'*SAN orbits {a}')
			else:
				orbit_data[b] = a
#				print(f'{b} orbits {a}')

	print(f'{len(orbit_data)} items read')
	return (you_orbit, santa_orbit, orbit_data)


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
		count += num_i
	return count

def have_seen(node, list_of_seen):
	for n in list_of_seen:
		if (n == node):
			return True
	return False



def search(start,end):
	lengths = {start:0}
	nodes = deque([start])
	visited = {start}
	while (end not in lengths):
		node = nodes.pop()
		length = lengths[node]
		for other_node in d_links[node]:
			if( have_seen(other_node,visited)):
				continue
			else:
				visited.add(other_node)
				nodes.appendleft(other_node)
				lengths[other_node] = length + 1

	return lengths[end]








def main():
	(you, santa, orbits) = read_orbits(AOC_6_DATA_FILENAME)
	#print(orbits)
	keys = orbits.keys()
	values = orbits.values()
	print(len(orbits.items()), end='')
	print(' total pairs')

	print(f'YOU orbits {you}')
	print(f'SAN orbits {santa}')

	count = count_all_orbits(orbits)
	print(f'total orbits: {count}')


	#o_path = search(you_p[0], santa_p[0])
	o_path = search(you,santa)
	print(f"edges between 'YOU''  and  'SAN' : {o_path}")




if __name__ == '__main__':
	main()
