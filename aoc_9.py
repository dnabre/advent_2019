from enum import Enum
from queue import Queue
from threading import Thread
import sys
import itertools
import time
from IntCodeMachine import *



#    Advent of Code 2019: Day 9
#        part1 answer: 3598076521
#        part2 answer: 90722

answer1 = 3598076521
answer2 = 90722


aoc_7_input = '3,8,1001,8,10,8,105,1,0,0,21,38,59,84,97,110,191,272,353,434,99999,3,9,1002,9,2,9,101,4,9,9,1002,9,2,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,5,9,9,101,5,9,9,1002,9,3,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99'

aoc_5_input = '3,225,1,225,6,6,1100,1,238,225,104,0,1102,57,23,224,101,-1311,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1102,57,67,225,102,67,150,224,1001,224,-2613,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,2,179,213,224,1001,224,-469,224,4,224,102,8,223,223,101,7,224,224,1,223,224,223,1001,188,27,224,101,-119,224,224,4,224,1002,223,8,223,1001,224,7,224,1,223,224,223,1,184,218,224,1001,224,-155,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,223,1101,21,80,224,1001,224,-101,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,1101,67,39,225,1101,89,68,225,101,69,35,224,1001,224,-126,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1102,7,52,225,1102,18,90,225,1101,65,92,225,1002,153,78,224,101,-6942,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1101,67,83,225,1102,31,65,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1007,226,226,224,102,2,223,223,1005,224,329,1001,223,1,223,108,677,226,224,1002,223,2,223,1005,224,344,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,359,1001,223,1,223,1107,677,226,224,102,2,223,223,1006,224,374,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,389,101,1,223,223,8,677,677,224,102,2,223,223,1006,224,404,1001,223,1,223,1008,226,226,224,102,2,223,223,1006,224,419,1001,223,1,223,107,677,226,224,102,2,223,223,1006,224,434,101,1,223,223,7,226,226,224,1002,223,2,223,1005,224,449,1001,223,1,223,1107,226,226,224,1002,223,2,223,1006,224,464,1001,223,1,223,1107,226,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,8,677,226,224,1002,223,2,223,1006,224,494,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,1008,677,226,224,102,2,223,223,1006,224,539,1001,223,1,223,1108,677,677,224,102,2,223,223,1005,224,554,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,569,101,1,223,223,1108,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,599,1001,223,1,223,1007,226,677,224,102,2,223,223,1005,224,614,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,629,1001,223,1,223,107,226,226,224,102,2,223,223,1005,224,644,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,659,101,1,223,223,107,677,677,224,1002,223,2,223,1005,224,674,1001,223,1,223,4,223,99,226'

aoc_9_input ='1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,3,0,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,33,1003,1101,0,23,1002,1102,1,557,1022,1102,1,24,1010,1102,1,22,1014,1101,470,0,1027,1102,38,1,1001,1102,1,21,1012,1102,1,1,1021,1101,0,26,1018,1101,0,827,1024,1101,690,0,1029,1101,0,473,1026,1102,1,27,1015,1101,695,0,1028,1101,822,0,1025,1102,1,35,1019,1102,1,30,1000,1101,0,39,1013,1101,25,0,1016,1101,28,0,1006,1102,1,36,1004,1101,34,0,1011,1101,31,0,1017,1101,0,0,1020,1101,29,0,1009,1102,1,554,1023,1102,32,1,1007,1101,37,0,1008,1101,20,0,1005,109,5,2101,0,0,63,1008,63,20,63,1005,63,203,4,187,1106,0,207,1001,64,1,64,1002,64,2,64,109,-4,2107,21,4,63,1005,63,227,1001,64,1,64,1105,1,229,4,213,1002,64,2,64,109,4,2108,37,3,63,1005,63,251,4,235,1001,64,1,64,1106,0,251,1002,64,2,64,109,12,21101,40,0,-5,1008,1012,38,63,1005,63,275,1001,64,1,64,1105,1,277,4,257,1002,64,2,64,109,-14,21108,41,41,10,1005,1013,299,4,283,1001,64,1,64,1105,1,299,1002,64,2,64,109,5,1202,-4,1,63,1008,63,36,63,1005,63,321,4,305,1106,0,325,1001,64,1,64,1002,64,2,64,109,-3,2108,38,-1,63,1005,63,345,1001,64,1,64,1106,0,347,4,331,1002,64,2,64,109,-8,1201,4,0,63,1008,63,40,63,1005,63,367,1105,1,373,4,353,1001,64,1,64,1002,64,2,64,109,20,1205,4,391,4,379,1001,64,1,64,1106,0,391,1002,64,2,64,109,5,1205,-2,407,1001,64,1,64,1106,0,409,4,397,1002,64,2,64,109,-15,2102,1,-3,63,1008,63,36,63,1005,63,431,4,415,1106,0,435,1001,64,1,64,1002,64,2,64,109,-6,1202,6,1,63,1008,63,31,63,1005,63,459,1001,64,1,64,1105,1,461,4,441,1002,64,2,64,109,28,2106,0,-2,1105,1,479,4,467,1001,64,1,64,1002,64,2,64,109,-14,21107,42,41,-4,1005,1011,499,1001,64,1,64,1106,0,501,4,485,1002,64,2,64,109,8,1206,-3,515,4,507,1105,1,519,1001,64,1,64,1002,64,2,64,109,-29,2101,0,6,63,1008,63,33,63,1005,63,539,1105,1,545,4,525,1001,64,1,64,1002,64,2,64,109,30,2105,1,-1,1106,0,563,4,551,1001,64,1,64,1002,64,2,64,109,5,1206,-8,579,1001,64,1,64,1106,0,581,4,569,1002,64,2,64,109,-31,1201,3,0,63,1008,63,38,63,1005,63,607,4,587,1001,64,1,64,1106,0,607,1002,64,2,64,109,11,21101,43,0,4,1008,1013,43,63,1005,63,633,4,613,1001,64,1,64,1106,0,633,1002,64,2,64,109,-10,2107,22,3,63,1005,63,651,4,639,1106,0,655,1001,64,1,64,1002,64,2,64,109,26,21102,44,1,-8,1008,1017,44,63,1005,63,681,4,661,1001,64,1,64,1105,1,681,1002,64,2,64,109,-3,2106,0,6,4,687,1105,1,699,1001,64,1,64,1002,64,2,64,109,-3,21108,45,43,0,1005,1019,715,1105,1,721,4,705,1001,64,1,64,1002,64,2,64,109,-25,1207,9,32,63,1005,63,737,1105,1,743,4,727,1001,64,1,64,1002,64,2,64,109,18,21107,46,47,3,1005,1015,761,4,749,1106,0,765,1001,64,1,64,1002,64,2,64,109,-3,2102,1,-3,63,1008,63,31,63,1005,63,789,1001,64,1,64,1105,1,791,4,771,1002,64,2,64,109,-5,1208,-4,30,63,1005,63,813,4,797,1001,64,1,64,1105,1,813,1002,64,2,64,109,28,2105,1,-8,4,819,1106,0,831,1001,64,1,64,1002,64,2,64,109,-30,1207,0,24,63,1005,63,853,4,837,1001,64,1,64,1106,0,853,1002,64,2,64,109,16,21102,47,1,-7,1008,1011,45,63,1005,63,873,1105,1,879,4,859,1001,64,1,64,1002,64,2,64,109,-21,1208,5,26,63,1005,63,899,1001,64,1,64,1105,1,901,4,885,4,64,99,21102,27,1,1,21102,915,1,0,1106,0,922,21201,1,69417,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1106,0,922,21201,1,0,-1,21201,-2,-3,1,21101,0,957,0,1105,1,922,22201,1,-1,-2,1105,1,968,22102,1,-2,-2,109,-3,2106,0,0'
TESTS_1 = [

	('1,9,10,3,2,3,11,0,99,30,40,50', '3500,9,10,70,2,3,11,0,99,30,40,50', [], []),
	('1,0,0,0,99', '2,0,0,0,99', [], []),
	('2,3,0,3,99', '2,3,0,6,99', [], []),
	('2,4,4,5,99,0', '2,4,4,5,99,9801', [], []),
	('1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99', [], []),

	(
		'1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,10,19,23,1,6,23,27,1,5,27,31,1,10,'
		'31,35,2,10,35,39,1,39,5,43,2,43,6,47,2,9,47,51,1,51,5,55,1,5,55,59,2,10,59,63,'
		'1,5,63,67,1,67,10,71,2,6,71,75,2,6,75,79,1,5,79,83,2,6,83,87,2,13,87,91,1,91,'
		'6,95,2,13,95,99,1,99,5,103,2,103,10,107,1,9,107,111,1,111,6,115,1,115,2,119,'
		'1,119,10,0,99,2,14,0,0',
		'5482655,12,2,2,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,60,1,10,19,64,1,6,23,66,'
		'1,5,27,67,1,10,31,71,2,10,35,284,1,39,5,285,2,43,6,570,2,9,47,1710,1,51,'
		'5,1711,1,5,55,1712,2,10,59,6848,1,5,63,6849,1,67,10,6853,2,6,71,13706,2,'
		'6,75,27412,1,5,79,27413,2,6,83,54826,2,13,87,274130,1,91,6,274132,2,13,95,'
		'1370660,1,99,5,1370661,2,103,10,5482644,1,9,107,5482647,1,111,6,5482649,1,'
		'115,2,5482651,1,119,10,0,99,2,14,0,0', [], []),
	('3,0,4,0,99', '50,0,4,0,99', [50], [50]),
	('1002,4,3,4,33', '1002,4,3,4,99', [], []),
	('1101,100,-1,4,0', '1101,100,-1,4,99', [], []),
]



TESTS_2 = [
	('3,9,8,9,10,9,4,9,99,-1,8', '3,9,8,9,10,9,4,9,99,0,8', [4], [0]),
	('3,9,8,9,10,9,4,9,99,-1,8', '3,9,8,9,10,9,4,9,99,1,8', [8], [1]),
	('3,9,7,9,10,9,4,9,99,-1,8', '3,9,7,9,10,9,4,9,99,1,8', [3], [1]),
	('3,9,7,9,10,9,4,9,99,-1,8', '3,9,7,9,10,9,4,9,99,0,8', [8], [0]),
	('3,3,1108,-1,8,3,4,3,99', '3,3,1108,0,8,3,4,3,99', [3], [0]),
	('3,3,1108,-1,8,3,4,3,99', '3,3,1108,1,8,3,4,3,99', [8], [1]),
	('3,3,1107,-1,8,3,4,3,99', '3,3,1107,1,8,3,4,3,99', [4], [1]),
	('3,3,1107,-1,8,3,4,3,99', '3,3,1107,0,8,3,4,3,99', [10], [0]),
	('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '3,12,6,12,15,1,13,14,13,4,13,99,0,0,1,9', [0], [0]),
	('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '3,12,6,12,15,1,13,14,13,4,13,99,4,1,1,9', [4], [1]),
	('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '3,3,1105,0,9,1101,0,0,12,4,12,99,0', [0], [0]),
	('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '3,3,1105,7,9,1101,0,0,12,4,12,99,1', [7], [1]),
	(
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,3,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	[3], [999]),
	(
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1000,8,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	[8], [1000]),
	(
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1000,8,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1001,17,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	[17], [1001]),
]

P_TEST=[
(
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1000,8,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	'3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,1001,17,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
	[17], [1001])
]


TESTS_9_1=[
	('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99','109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,1', [], [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]),
	('1102,34915192,34915192,7,4,7,99,0', '1102,34915192,34915192,7,4,7,99,1219070632396864', [], [1219070632396864]),
	('104,1125899906842624,99','104,1125899906842624,99',[],[1125899906842624]),
	('109,-1,4,1,99', '109,-1,4,1,99', [], [-1]),
	('109,-1,104,1,99', '109,-1,104,1,99', [], [1]),
	('109,-1,204,1,99', '109,-1,204,1,99', [], [109]),
	('109,1,9,2,204,-6,99', '109,1,9,2,204,-6,99', [], [204]),
	('109,1,109,9,204,-6,99', '109,1,109,9,204,-6,99', [], [204]),
	('109,1,209,-1,204,-106,99', '109,1,209,-1,204,-106,99', [], [204]),
	('109,1,3,3,204,2,99', '109,1,3,51385958,204,2,99', [51385958], [51385958]),
	('109,1,203,2,204,2,99', '109, 1, 203, 109109019, 204, 2, 99', [109109019], [109109019])
	]

TEST_9_204 = [('109,1,203,2,204,2,99', '109, 1, 203, 109109019, 204, 2, 99', [109109019], [109109019])]


def aoc9_part1():
	part1_input = aoc_9_input
	input_queue = Queue(maxsize=-1)
	output_queue = Queue(maxsize=-1)
	input_queue.put_nowait(1)
	part1_code= IntCodeMachine.parse_from_string(part1_input)
	part1_cpu = IntCodeMachine(part1_code, input_queue, output_queue)
	result  =part1_cpu.run_program()
	#print(result)


	program_outputs = []
	while (not output_queue.empty()):
		g = output_queue.get()
		program_outputs.append(g)
		output_queue.task_done()

	#print(f'output: {program_outputs}')
	return program_outputs
def aoc9_part2():
	part1_input = aoc_9_input
	input_queue = Queue(maxsize=-1)
	output_queue = Queue(maxsize=-1)
	input_queue.put_nowait(2)
	part1_code= IntCodeMachine.parse_from_string(part1_input)
	part1_cpu = IntCodeMachine(part1_code, input_queue, output_queue)
	result  =part1_cpu.run_program()
	#print(result)


	program_outputs = []
	while (not output_queue.empty()):
		g = output_queue.get()
		program_outputs.append(g)
		output_queue.task_done()

	#print(f'output: {program_outputs}')
	return program_outputs





def output_queue_to_list(q):
	result = []
	while (not q.empty()):
		result.append(q.get())
		q.task_done()
	return result

def main():

#	run_tests(TESTS_1, name="Test Set #1")
#	run_tests(TESTS_2, name="Test Set #2")
#	run_tests(P_TEST, name="Problem Test")
#	run_tests(TESTS_9_1, name="Problem 9 Series")

	part1_answer = aoc9_part1()[0]


	print(f' AoC 2019, Day 9')
	print(f'\tpart 1:', end="")
	if part1_answer != answer1:
		print(f'\treceived: {part1_answer}, expected {answer1}')
	else:
		print(f'\tpart1: {part1_answer}')

	part2_answer = aoc9_part2()[0]
	print(f'\tpart 2:', end="")
	if part2_answer != answer2:
		print(f'\treceived: {part2_answer}, expected {answer2}')
	else:
		print(f'\tpart1: {part2_answer}')



if __name__ == '__main__':
	main()
