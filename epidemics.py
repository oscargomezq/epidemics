import numpy as np

# Number of levels
# level 0 = only the nearest 4 neighbors
# level 1 = smallest group of 4
# level m = all the population
m = 4

# Size of population
N = 4**m

# Probability for geometric distribution
alpha = 1/10

# Probability for nearest neighbors (h=0)
p = 0.10

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
	return int(b,2)

# Update the infected sets for x,y getting infected in the given iteration
def update_infected (x, y, itr):
	infected_history[itr].add((bin_to_dec(x),bin_to_dec(y)))
	total_infected.add((bin_to_dec(x),bin_to_dec(y)))

# Randomly sample from the given probability that x,y infects the other at this level
def try_to_infect (x, y, h, compare_x, compare_y):
	# Check if already infected, skip altogether
	if (bin_to_dec(x),bin_to_dec(y)) in total_infected: return False

	# Check if height of comp_x, comp_y is less than h, skip
	if get_height(compare_x, compare_y) < h: return False

	inf_prob = p * (rho**h)
	return 1 == np.random.binomial(1,inf_prob)

# Iterate through neighbors an individual can infect at given level h
def infect_iteration_h (x, y, h):
	start_x, start_y, length =  find_range(x,y,h)
	compare_x, compare_y = start_x, start_y
	for i in range(length):
		if i>0: compare_y = next_in_bin(compare_y)
		for j in range(length):
			if j>0: compare_x = next_in_bin(compare_x)
			compare_h = get_height(compare_x, compare_y)
			got_infected = try_to_infect(x, y, h, compare_x, compare_y)
			if got_infected: update_infected (compare_x, compare_y, curr_iter)
		compare_x = start_x

# Interate through all neighbors an individual can infect
def infect_iteration (x, y, h):
	for i in range (h+1):
		print ("Iterating at level:", i)
		infect_iteration_h (x, y, i)

	# Check nearest neighbors (height 0) separately
	nearest = [(next_in_bin(x),y), (prev_in_bin(x),y), (x,next_in_bin(y)), (x,prev_in_bin(y))]
	for neigh in nearest:
		got_infected = try_to_infect(x, y, 0, neigh[0], neigh[1])
		if got_infected: update_infected (compare_x, compare_y, curr_iter)


# Main loop
total_iterations = 10

curr_iter = 0
init_idx = dec_to_bin( int( (4**(int(m/2)))/2 ), m)
initial_infected = (init_idx, init_idx)
update_infected (initial_infected[0], initial_infected[1], curr_iter)

for i in range(total_iterations):
	curr_iter += 1
	print("Infected at iteration:", curr_iter-1)
	print(infected_history[curr_iter-1])
	print()
	infected_history.append(set({}))
	for person in infected_history[curr_iter-1]:
		px, py = dec_to_bin(person[0],m), dec_to_bin(person[1],m)
		infect_iteration (px, py, get_height(px, py))
	


# x=37
# y=255
# xbin = dec_to_bin(x, m)
# ybin = dec_to_bin(y, m)
# print(xbin,ybin)
# print(find_range(xbin, ybin, 3))


# print(next_in_bin(xbin), next_in_bin(ybin))

# x=0
# y=0
# xbin = dec_to_bin(x, m)
# ybin = dec_to_bin(y, m)
# infect_iteration(xbin,ybin,3)
