"""

input = 1    2    4    7   13   13   19   26

pattern = [1;0;-1;0]

p_m = [[1,0,-1,0,1,0,-1,0];[0,1,1,0,0,-1,-1,0];[0,0,1,1,1,0,0,0];[0,0,0,1,1,1,1,0];[0,0,0,0,1,1,1,1];[0,0,0,0,0,1,1,1];[0,0,0,0,0,0,1,1];[0,0,0,0,0,0,0,1]]

   1   0  -1   0   1   0  -1   0
   0   1   1   0   0  -1  -1   0
   0   0   1   1   1   0   0   0
   0   0   0   1   1   1   1   0
   0   0   0   0   1   1   1   1
   0   0   0   0   0   1   1   1
   0   0   0   0   0   0   1   1
   0   0   0   0   0   0   0   1
input' is the transpose of input

p_m * input' = q =
   -4
   -8
   12
   22
   26
   21
   15
    8

taking mod(abs(q),10)

   4
   8
   2
   2
   6
   1
   5
   8

repeated q = (p_m * mod(abs(q),10)) gives values


input 650 long8,
"""
aoc16_p1_input = '59754835304279095723667830764559994207668723615273907123832849523285892960990393495763064170399328763959561728553125232713663009161639789035331160605704223863754174835946381029543455581717775283582638013183215312822018348826709095340993876483418084566769957325454646682224309983510781204738662326823284208246064957584474684120465225052336374823382738788573365821572559301715471129142028462682986045997614184200503304763967364026464055684787169501819241361777789595715281841253470186857857671012867285957360755646446993278909888646724963166642032217322712337954157163771552371824741783496515778370667935574438315692768492954716331430001072240959235708'
aoc16_offset = 5975483
import numpy as np
import time
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
import scipy

base_pattern = [0, 1, 0, -1]


def get_pattern(num_count, i):
	pattern = []
	pi = 0
	while (len(pattern) < (num_count + 1)):
		n = base_pattern[pi]
		pattern += [n] * (i + 1)
		pi = (pi + 1) % (len(base_pattern))
	return pattern[1:num_count + 1]


def build_phase_matrix(n):
	mat_list = [get_pattern(n, r_num) for r_num in range(n)]
	return np.array(mat_list)


def apply_step(phase_matrix, input_list):
	in_vec = np.transpose(np.array(input_list))
	n_q = np.matmul(phase_matrix, in_vec)
	n_q = [abs(q) % 10 for q in n_q]
	return n_q


def string_for_first8(big_list):
	result = ''.join(map(str, big_list[:8]))
	return result





part2_tests = {
	"03036732577212944063491565474664": "84462026",
	"02935109699940807407585447034323": "78725270",
	"03081770884921959731165446850517": "53553731",
}


def string_for_first8(big_list):
	result = ''
	for i in range(8):
		result += str(big_list[i])
	return result

def str_to_list(t_string):
	return [int(t_string[i]) for i in range(len(t_string))]

def offsetfft(signal: np.array, repeat: int = 100) -> np.array:
	# digits to number
	offset = (10 ** np.arange(6, -1, -1) * signal[:7]).sum()
	offsetsignal = np.tile(signal, 10000)[offset:]
	for _ in range(repeat):
		offsetsignal = np.cumsum(offsetsignal[::-1])[::-1] % 10
	return offsetsignal

part2_answer = '41402171'

def main():
	#	c_len = 8
	#	mat = [get_pattern(c_len, r_num) for r_num in range(8)]

	test1 = '80871224585914546619083218645595'
	test2 = '19617804207202209144916044189917'
	test3 = '69317163492948606335995924319873'

	test4 = '03036732577212944063491565474664'
	test5 = '02935109699940807407585447034323'
	test6 = '03081770884921959731165446850517'
	start_time = time.time()

	target_string = test3
	n_list = str_to_list(target_string)
	result =  string_for_first8(offsetfft(np.array(str_to_list(aoc16_p1_input))))
	print(aoc16_p1_input, end='')
	print('\n->\t', end='')
	assert(result == part2_answer)
	print(result)



	"""
	print('building matrix: ', end='')
	mat = build_phase_matrix(len(n_list))
	print(f'done ({time.time() - start_time} ms)')
   """


"""
start_time = time.time()

n_steps = 100


print("calculating: ", end='')
for x in range(n_steps):
	n_list = apply_step(mat,n_list)
	print(" {:3d} ".format(x), end='')

print()
print(f'done {time.time() - start_time} ms')
result = string_for_first8(n_list)
print(result)

"""

if __name__ == "__main__":
	main()
