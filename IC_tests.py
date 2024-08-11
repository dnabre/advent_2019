
def run_tests(test_set, name=''):
	count = 0
	if(len(test_set) > 1):
		print(f'running {name} series of {len(test_set)} tests')
	for t in test_set:
	#	print(f'\n{t}')
		(test_prog, test_prog_expected_string, test_inputs, test_outputs) = t
		test_prog = IntCodeMachine.parse_from_string(test_prog)
		input_queue = Queue(maxsize=0)
		for i in test_inputs:
			input_queue.put_nowait(i)
		output_queue = Queue(maxsize=0)
		cpu = IntCodeMachine(test_prog, input_queue, output_queue)
		test_results = cpu.run_program().asList()
	#	print(test_prog)
#		print(test_results)
		program_outputs = []
		while (not output_queue.empty()):
			g = output_queue.get()
			program_outputs.append(g)
			output_queue.task_done()

	#	print('', end='\t')
	#	print(test_prog, end=' ')

		test_prog_expected = IntCodeMachine.parse_from_string(test_prog_expected_string)

#		print(f' -> {test_result}')
		print(f'output={program_outputs}', end="")

		failed = False
		if (test_results != test_prog_expected):
			failed = True
		#	print(t)
		#	print(f'error:  expected program state: {test_prog_expected} {type(test_prog_expected)}')
	#		print(f'error:  received program state: {test_results} {type(test_results)}')
			#print(f'raw string: {IntCodeMachine.code_to_string(test_results)}')
		if (test_outputs != program_outputs):
			failed = True
	#		print(t)
#			print(f'error: expected program output: {test_outputs}')
#			print(f'error: received program output: {program_outputs}')

		if failed:
			sys.exit('test failed')
		else:
			print(f'\t: correct \t {program_outputs}')
			count += 1
	if (len(test_set) > 1):
		print(f'series of tests {name} ran, {count} of {len(test_set)} correct: ', end='')
		if(len(test_set) == count): print('OK')
		else: print('errors found')
