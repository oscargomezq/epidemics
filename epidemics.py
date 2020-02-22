import numpy as np
import matplotlib.pyplot as plt


# Number of levels
# level 0 = only the nearest 4 neighbors
# level 1 = smallest group of 4
# level m = all the population
m = 8

# Size of population
N = 4**m

# Size of side of square
len_side = 4**(int(m/2))

# Probability for geometric distribution
alpha = 1/10

# Probability for nearest neighbors (h=0)
p = 0.20

# Decrease modulator for higher levels
rho = 0.50

# List of sets of infected people (only includes the NEWLY infected people at each stage)
# Stores tuples of ints, not strings
infected_history = [set({})]

# Set of everyone infected so far (union of the history sets)
total_infected = set({})

# Returns x+1 in base b
def next_in_base (x, b):
	nxt = x.copy()
	i=1
	while x[-i] == b-1:
		nxt[-i] = 0
		i-=1
	nxt[-i] = nxt[-i]+1
	return nxt

# Returns b+1 in binary (string)
def next_in_bin (b):
	if b == "1"*(len(b)):
		return "1" + "0"*len(b)
	nxt = ''
	i=1
	while b[-i] == '1':
		nxt = '0' + nxt
		i+=1
	nxt = '1' + nxt
	nxt = b[:len(b)-len(nxt)]+ nxt
	return nxt

# Returns b-1 in binary (string)
def prev_in_bin (b):
	prev = bin_to_dec(b)-1
	return dec_to_bin(prev, len(b))

# Get same height everytime we sample
def get_height (x, y):
	x1 = bin_to_dec(x)
	y1 = bin_to_dec(y)
	idx = x1*(4**(m/2)) + y1
	np.random.seed(int(idx))
	return np.random.geometric(p=alpha)%(m+1)

# Return starting point for range of points to check
# x and y are binary strings
def find_range (x, y, h):
	x1 = x[:-h] + "0"*h
	y1 = y[:-h] + "0"*h
	return (x1, y1, 2**h)

# Return binary string for x with a given number of digits
def dec_to_bin (x, digits):
	b = bin(x)[2:]
	b = "0"*(digits-len(b)) + b
	return b

# Binary string to decimal int
def bin_to_dec (b):
	try:
		return int(b,2)
	except: print("ERROROOOOOOOOOOOROROROROROROROROROROROROROROROOROROROROR AAAAAAAAAHHHHH PANIC ", b)

# Update the infected sets for x,y getting infected in the given iteration
def update_infected (x, y, itr):
	infected_history[itr].add((bin_to_dec(x),bin_to_dec(y)))
	total_infected.add((bin_to_dec(x),bin_to_dec(y)))

# Randomly sample from the given probability that x,y infects the other at this level
def try_to_infect (x, y, h, compare_x, compare_y):
	# Check if already infected, skip altogether
	if (bin_to_dec(compare_x),bin_to_dec(compare_y)) in total_infected: return False
	# print ("Not yet infected")
	# Check if height of comp_x, comp_y is less than h, skip
	if get_height(compare_x, compare_y) < h: return False
	# print("Height test passes")
	inf_prob = p * (rho**h)
	# print("Probability:", inf_prob)
	np.random.seed()
	return 1 == np.random.binomial(1,inf_prob)

# Iterate through neighbors an individual can infect at given level h
def infect_iteration_h (x, y, h):
	start_x, start_y, length = find_range(x,y,h)
	# print('FIND RANGE', start_x, start_y, length)
	compare_x, compare_y = start_x, start_y
	for i in range(length):
		if i>0: compare_y = next_in_bin(compare_y)
		for j in range(length):
			if j>0: compare_x = next_in_bin(compare_x)
			# print ("Comparing with:", compare_x, compare_y)
			compare_h = get_height(compare_x, compare_y)
			# print("Height:", compare_h)
			got_infected = try_to_infect(x, y, h, compare_x, compare_y)
			if got_infected: update_infected (compare_x, compare_y, curr_iter)
		compare_x = start_x

# Interate through all neighbors an individual can infect
def infect_iteration (x, y, h):
	for i in range (1, h+1):
		# print ("Iterating at level:", i)
		infect_iteration_h (x, y, i)
	# Check nearest neighbors (height 0) separately
	nearest = []
	if (bin_to_dec(x) < len_side-1): nearest.append((next_in_bin(x),y))
	if (bin_to_dec(x) > 0): nearest.append((prev_in_bin(x),y))
	if (bin_to_dec(y) < len_side-1): nearest.append((x,next_in_bin(y)))
	if (bin_to_dec(y) > 0): nearest.append((x,prev_in_bin(y)))
	for neigh in nearest:
		got_infected = try_to_infect(x, y, 0, neigh[0], neigh[1])
		if got_infected: update_infected (neigh[0], neigh[1], curr_iter)

# Visualization
def print_matrix (infected_set, side):
	aa = np.zeros((side,side))
	for tup in infected_set:
		aa[tup[0], tup[1]] = 1
	plt.matshow(aa)
	plt.show()

# Main loop
total_time_steps = 10

curr_iter = 0
init_idx = dec_to_bin( int( len_side/2 ), m)
initial_infected = (init_idx, init_idx)
update_infected (initial_infected[0], initial_infected[1], curr_iter)

for i in range(total_time_steps):
	curr_iter += 1
	infected_history.append(set({}))
	for person in infected_history[curr_iter-1]:
		px, py = dec_to_bin(person[0],m), dec_to_bin(person[1],m)
		infect_iteration (px, py, get_height(px, py))
	print("--------------------------------------------------------------------------")
	# print("Infected at time step:", curr_iter-1)
	print(infected_history[curr_iter-1])
	print("Total infected so far:", len(total_infected))
	print()
	print_matrix (total_infected, len_side)
