#import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PI = math.pi

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

AOC_18_DATA_FILENAME='aoc_18_input.txt'

TEST_CHARS = ['#', '*', 'a','b','c','d','O','A','B','C','D', '@',]

MARGIN = 1
HEIGHT = 15
WIDTH = 15
FONT_SIZE=30

GRID_HEIGHT =81
GRID_WIDTH= 81

grid = []

def grid_init():
	for row in range(GRID_HEIGHT):
		grid.append([])
		for column in range(GRID_WIDTH):
			grid[row].append('_')






def get_dims(map):
	x = len(map)
	y = len(map[0])
	return (x,y)

def main():
	for ex in examples:
		ex = ex.split('\n')
		print(ex)
		print(get_dims(ex))
		print("\n\n")

	with open(AOC_18_DATA_FILENAME, 'r') as input_file:
		prob_map = input_file.readlines()

	for x in range(len(prob_map)):
		prob_map[x] = prob_map[x].strip()





	prob_map_dims = get_dims(prob_map)
	print(prob_map)
	print(prob_map_dims)

	prob_map = example_1.split('\n')

	grid_init()

	for x in range(len(prob_map)):
		for y in range(len(prob_map[x])):
			print(f'{(x,y)}')
			grid[x][y] = prob_map[x][y]
'''
	pygame.init()
	font = pygame.font.Font(None, FONT_SIZE)
	screen = pygame.display.set_mode((1350,1350))
	pygame.display.set_caption('AOC Day 18')
	clock = pygame.time.Clock()
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			screen.fill(BLACK)

			# Draw the grid
			num_example = len(TEST_CHARS)
			for row in range(GRID_HEIGHT):
				for column in range(GRID_WIDTH):
					color = WHITE

					if grid[row][column] == 1:
						color = GREEN
					pygame.draw.rect(screen,
									 color,
									 [(MARGIN + WIDTH) * column + MARGIN,
									  (MARGIN + HEIGHT) * row + MARGIN,
									  WIDTH,
									  HEIGHT])
					#ch = TEST_CHARS[((row*column) + column) % num_example]
					#print(f'{ch} @ {(MARGIN + WIDTH) * column + MARGIN}x{ (MARGIN + HEIGHT) * row + MARGIN}' )
					ch = grid[row][column]
					print(ch)
					if(ch != '.'):
						text = font.render(str(ch), True, BLACK)
						screen.blit(text,[(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN])

			# Limit to 60 frames per second
			clock.tick(60)

			# Go ahead and update the screen with what we've drawn.
			pygame.display.flip()
'''

if __name__ == "__main__":
	main()