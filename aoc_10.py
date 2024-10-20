from fractions import Fraction
from collections import defaultdict
from operator import itemgetter

ASTEROID_MAPS = """\
.#..#
.....
#####
....#
...##

......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####

#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.

.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..

.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

MAP_SIZES = [(5, 5), (10, 10), (10, 10), (10, 10), (20, 20)]

pos_n = {(3, 4): 8, (5, 8): 33, (1, 2): 35, (6, 3): 41, (11, 13): 210}
tests = dict(zip(ASTEROID_MAPS.split("\n\n"), pos_n.items()))
# best location ((x,y), count of visible asteroids)


A_MAPS = []


def parse_maps(log=False):
	afs = ASTEROID_MAPS.split('\n\n')
	if log: print(f'{len(afs)} maps')
	for i in range(len(afs)):
		afs[i] = afs[i].strip()
		a = afs[i]
		if log:    print()
		if log: print(a)
		rows = a.split('\n')
		dims = (len(rows[0]), len(rows))
		if (dims != MAP_SIZES[i]):
			print('ERROR: Map dimensions ({dims} does not match provided dimenions: {MAP_SIZES[i]} ')
			detailed_print(a)



def detailed_print(m):
	m = m.strip().rstrip()
	print('detailed map')
	rows = m.split('\n')
	for i in range(len(rows)):
		print('%3d: %s' % (i, rows[i]))


def parsed(data):
	asteroids = []
	rows = data.splitlines()
	for y, row in enumerate(rows):
		for x, val in enumerate(row):
			if val == "#":
				asteroids.append((x, y))
	assert len(asteroids) == data.count("#")
	return asteroids


def quadrant(a0, a):
	x0, y0 = a0
	x, y = a
	if y < y0 and x >= x0:
		return 1
	if y >= y0 and x > x0:
		return 2
	if y > y0 and x <= x0:
		return 3
	if y <= y0 and x < x0:
		return 4


def grad(a0, a):
	q = quadrant(a0, a)
	x0, y0 = a0
	x, y = a
	(t, b) = (y - y0, x - x0)

	if (b == 0):
		m = float('inf')
	else:
		f = Fraction(t, b)
		m = abs(f)
	if q % 2:
		m *= -1
	return q, m


def part_a(data):
	gradients = defaultdict(set)
	A = parsed(data)
	for i, a0 in enumerate(A):
		for a in A[i + 1:]:
			q, g = grad(a, a0)
			gradients[a0].add((q, g))
			gradients[a].add(((q + 2) % 4, -g))
	n_collinear = {k: len(v) for k, v in gradients.items()}
	a, n = max(n_collinear.items(), key=itemgetter(1))
	return a, n


def norm2(a1, a2):
	dx = a2[0] - a1[0]
	dy = a2[1] - a1[1]
	d2 = dx * dx + dy * dy
	return d2


def part_ab(data, target=200, extra_assertions=()):
	A = parsed(data)
	a0, part_a_answer = part_a(data)
	d = defaultdict(list)
	for a in A:
		if a == a0:
			continue
		g = grad(a0, a)
		d[g].append(a)
	ds = {}
	for g in sorted(d):
		ds[g] = sorted(d[g], key=lambda a: norm2(a0, a), reverse=True)
	i = 0
	while True:
		for g in ds:
			if ds[g]:
				a = ds[g].pop()
				i += 1
				if i in extra_assertions:
					assert extra_assertions[i] == a
					log.info("The %dth asteroid to be vaporized is at %d,%d", i, *a)
				if i == target:
					part_b_answer = 100 * a[0] + a[1]
					return part_a_answer, part_b_answer


data = """\
#.#....#.#......#.....#......####.
#....#....##...#..#..##....#.##..#
#.#..#....#..#....##...###......##
...........##..##..##.####.#......
...##..##....##.#.....#.##....#..#
..##.....#..#.......#.#.........##
...###..##.###.#..................
.##...###.#.#.......#.#...##..#.#.
...#...##....#....##.#.....#...#.#
..##........#.#...#..#...##...##..
..#.##.......#..#......#.....##..#
....###..#..#...###...#.###...#.##
..#........#....#.....##.....#.#.#
...#....#.....#..#...###........#.
.##...#........#.#...#...##.......
.#....#.#.#.#.....#...........#...
.......###.##...#..#.#....#..##..#
#..#..###.#.......##....##.#..#...
..##...#.#.#........##..#..#.#..#.
.#.##..#.......#.#.#.........##.##
...#.#.....#.#....###.#.........#.
.#..#.##...#......#......#..##....
.##....#.#......##...#....#.##..#.
#..#..#..#...........#......##...#
#....##...#......#.###.#..#.#...#.
#......#.#.#.#....###..##.##...##.
......#.......#.#.#.#...#...##....
....##..#.....#.......#....#...#..
.#........#....#...#.#..#....#....
.#.##.##..##.#.#####..........##..
..####...##.#.....##.............#
....##......#.#..#....###....##...
......#..#.#####.#................
.#....#.#..#.###....##.......##.#.
"""


def main():
	a, b = part_ab(data)
	print(a)
	print(b)


if __name__ == "__main__":
	main()
