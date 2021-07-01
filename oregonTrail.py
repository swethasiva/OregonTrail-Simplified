###########################################################################################################################################################################################
#	Title: The Oregon Trail (CSCI 561 - Foundations of Artificial Intelligence)
#	Author: Swetha Sivakumar (USC ID: 5978959727)
#	Last Modified Date: 19th Feb 2021
#	Description: Program to find the shortest path, if exists, from source to each target node using BFS, UCS or A* algorithm while considering Muddiness and Rocks througout the path 
#	Language Used: Python 3 
#	Input: input.txt
#	Output: output.txt (each line is a path from source to each of the target node)
#
##########################################################################################################################################################################################
from math import sqrt
import heapq
import re
from collections import deque 

# This is a utility function to print the optimal path by iterating through the parent array in reverse fashion from Target node to Source node until "None" is found.
# The function writes the optimal paths to output.txt, one line for each target specified in the input.txt
def print_optimal_path(node, parent):
	optimal_path = ""
	while(node != None):
		temp_node = node
		temp_node = re.sub(r"[\[\]]", "", temp_node)		
		temp_node = temp_node.split(",")
		optimal_path += str(temp_node[1].strip(" ")[::-1]) + "," + str(temp_node[0].strip(" ")[::-1])+" "
		node = parent[node]
	with open("output.txt", "a+") as f:	 # New I/O code to write solution to output.txt 
		f.write(optimal_path[::-1].lstrip()+"\n")
	return



# This Function runs A* on the input graph to find shortest valid path from source to each and every target provided in input.txt
# The following implementation of A* algorithm uses Euclidean Distance as its heuristic function. 
# Euclidean function works as an admissible heuristic function for the given problem statement since diagonal paths are also allowed and thus it never over-estimates the path cost.
def A_star_path_finder(W, H, start_x, start_y, max_rock_height, number_of_settling_sites, settling_sites, land_map):
	for target in settling_sites:
		if (start_x < 0 or start_y < 0 or target[0] < 0 or target[1] < 0 or start_x >= W or start_y >= H or target[0] >= W or target[1] >=H):
			with open("output.txt", "a+") as f:	##### Modification: I/O code to write solution to output.txt 
				f.write("FAIL"+"\n")
			print("FAIL")
			continue
		is_present = False 
		parent = dict()
		cost_till_now = dict()
		visited = set()
		# frontier: The priority queue that stores the (actual path_cost_till_now to a node from the Source + Heuristic path cost from the node to the target node, the co-ordinates of the node in consideration)
		# frontier, priority queue is implemented as a min-heap.
		frontier = []
		parent[str([start_x, start_y])] = None
		cost_till_now[str([start_x, start_y])] = 0
		if [start_x, start_y] == target:
			print_optimal_path(str([start_x, start_y]),parent)
			is_present = True
			break
		heapq.heappush(frontier, (sqrt((start_x- target[0])**2 + (start_y- target[1])**2), [start_x, start_y]))
		while len(frontier)>0:
			path_cost_till_now, current_node = heapq.heappop(frontier)
			visited.add(str(current_node))
			path_cost_till_now = cost_till_now[str(current_node)]
			# Print optimal path on reaching target
			if current_node == target:
				is_present = True 
				print(path_cost_till_now)
				print_optimal_path(str(current_node), parent)
				break
			if land_map[int(current_node[0])][int(current_node[1])] < 0:
				current_node_height = abs(land_map[int(current_node[0])][int(current_node[1])])
			else:
				current_node_height = 0
			for neighbhor in [[current_node[0], current_node[1]-1], [current_node[0], current_node[1]+1], [current_node[0]+1, current_node[1]], [current_node[0]-1, current_node[1]], [current_node[0]-1, current_node[1]-1], [current_node[0]+1, current_node[1]-1], [current_node[0]+1, current_node[1]+1], [current_node[0]-1, current_node[1]+1]]:
				#	Checking if neighbhor is a valid node within the mesh-grid of the landscape  
				if (neighbhor[0]<0 or neighbhor[1] < 0 or neighbhor[0] >= W or neighbhor[1] >= H) or (str(neighbhor) in visited):
					continue
				if land_map[neighbhor[0]][neighbhor[1]] < 0:
					neighbhor_node_height = abs(land_map[neighbhor[0]][neighbhor[1]])
					neighbhor_node_muddiness = 0
				else:
					neighbhor_node_height = 0
					neighbhor_node_muddiness = land_map[neighbhor[0]][neighbhor[1]]
				if (abs(current_node_height- neighbhor_node_height)>max_rock_height):
					continue
				extra_cost = abs(current_node_height- neighbhor_node_height) + neighbhor_node_muddiness
				if (neighbhor[0] != current_node[0] and neighbhor[1] != current_node[1]):
					extra_cost += 14
				else: 
					extra_cost += 10

				neighbhor_cost = extra_cost + path_cost_till_now 
			
				if str(neighbhor) not in cost_till_now or neighbhor_cost < cost_till_now[str(neighbhor)]:
					cost_till_now[str(neighbhor)] = neighbhor_cost 	
					heapq.heappush(frontier, (neighbhor_cost + sqrt((neighbhor[0]- target[0])**2 + (neighbhor[1]- target[1])**2), neighbhor))
					parent[str(neighbhor)] = str(current_node)

		# Print "Failed" if no path exists
		if not is_present:
			with open("output.txt", "a+") as f:
				f.write("FAIL"+"\n")
			print("FAIL")

# This function implements Uniform Cost Search to find the shortest path from source node to each of the given target sites. 
# In UCS, each of the diagonal neighbours of a node have a path cost of 14, while other neighbours have path cost of 10.
def ucs_path_finder(W, H, start_x, start_y, max_rock_height, number_of_settling_sites, settling_sites, land_map):
	for target in settling_sites:
		if (start_x < 0 or start_y < 0 or target[0] < 0 or target[1] < 0 or start_x >= W or start_y >= H or target[0] >= W or target[1] >=H):
			with open("output.txt", "a+") as f:
				f.write("FAIL"+"\n")
			print("FAIL")
			continue
		is_present = False 
		parent = dict()
		cost_till_now = dict()
		visited = set()
		# frontier: The priority queue that stores the (actual path_cost_till_now to a node from the Source, the co-ordinates of the node in consideration)
		# frontier, priority queue is implemented as a min-heap.
		frontier = []
		parent[str([start_x, start_y])] = None
		cost_till_now[str([start_x, start_y])] = 0
		if [start_x, start_y] == target:
			print_optimal_path(str([start_x, start_y]), parent)
			is_present = True
			break
		heapq.heappush(frontier, (cost_till_now[str([start_x, start_y])], [start_x, start_y]))
		while len(frontier)>0:
			path_cost_till_now, current_node = heapq.heappop(frontier)
			visited.add(str(current_node))
			path_cost_till_now = cost_till_now[str(current_node)]
			if current_node == target:
				is_present = True 
				print(path_cost_till_now)
				print_optimal_path(str(current_node), parent)
				break
			if land_map[int(current_node[0])][int(current_node[1])] < 0:
					current_node_height = abs(land_map[int(current_node[0])][int(current_node[1])])
			else:
				current_node_height = 0
			for neighbhor in [[current_node[0], current_node[1]-1], [current_node[0], current_node[1]+1], [current_node[0]+1, current_node[1]], [current_node[0]-1, current_node[1]], [current_node[0]-1, current_node[1]-1], [current_node[0]+1, current_node[1]-1], [current_node[0]+1, current_node[1]+1], [current_node[0]-1, current_node[1]+1]]:
				if (neighbhor[0]<0 or neighbhor[1] < 0 or neighbhor[0] >= W or neighbhor[1] >= H) or (str(neighbhor) in visited):
					continue
				if land_map[neighbhor[0]][neighbhor[1]] < 0:
					neighbhor_node_height = abs(land_map[neighbhor[0]][neighbhor[1]])
				else:
					neighbhor_node_height = 0
				if (abs(current_node_height- neighbhor_node_height)>max_rock_height):
					continue
				if (neighbhor[0] != current_node[0] and neighbhor[1] != current_node[1]):
					extra_cost = 14
				else: 
					extra_cost = 10

				neighbhor_cost = extra_cost + path_cost_till_now 
				
				is_found = False
				if str(neighbhor) not in cost_till_now or neighbhor_cost < cost_till_now[str(neighbhor)]:
					cost_till_now[str(neighbhor)] = neighbhor_cost 	
					heapq.heappush(frontier, (neighbhor_cost, neighbhor))
					parent[str(neighbhor)] = str(current_node)
				
		if not is_present:
			with open("output.txt", "a+") as f:
				f.write("FAIL"+"\n")
			print("FAIL")
	return

# This function implements Breadth First Search to find the shortest path from source node to each of the given target sites. 
# In BFS, each of the 8 neighbours of a node have a path cost of 1.
def bfs_path_finder(W, H, start_x, start_y, max_rock_height, number_of_settling_sites, settling_sites, land_map):
	for target in settling_sites:
		if (start_x < 0 or start_y < 0 or target[0] < 0 or target[1] < 0 or start_x >= W or start_y >= H or target[0] >= W or target[1] >=H):
			with open("output.txt", "a+") as f:
				f.write("FAIL"+"\n")
			print("FAIL")
			continue
		is_present = False 
		parent = dict()
		cost_till_now = dict()
		visited = set()
		frontier = deque()
		parent[str([start_x, start_y])] = None
		cost_till_now[str([start_x, start_y])] = 0
		if [start_x, start_y] == target:
			print_optimal_path(str([start_x, start_y]), parent)
			is_present = True
			break
		frontier.append([start_x, start_y])
		while len(frontier)>0:
			current_node = frontier.popleft()
			visited.add(str(current_node))
			path_cost_till_now = cost_till_now[str(current_node)]
			if current_node == target:
				is_present = True 
				print(path_cost_till_now)
				print_optimal_path(str(current_node), parent)
				break
			for neighbhor in [[current_node[0], current_node[1]-1], [current_node[0], current_node[1]+1], [current_node[0]+1, current_node[1]], [current_node[0]-1, current_node[1]], [current_node[0]-1, current_node[1]-1], [current_node[0]+1, current_node[1]-1], [current_node[0]+1, current_node[1]+1], [current_node[0]-1, current_node[1]+1]]:
				if (neighbhor[0]<0 or neighbhor[1] < 0 or neighbhor[0] >= W or neighbhor[1] >= H) or (str(neighbhor) in visited):
					continue
				if land_map[int(current_node[0])][int(current_node[1])] < 0:
					current_node_height = abs(land_map[int(current_node[0])][int(current_node[1])])
				else:
					current_node_height = 0
				if land_map[neighbhor[0]][neighbhor[1]] < 0:
					neighbhor_node_height = abs(land_map[neighbhor[0]][neighbhor[1]])
				else:
					neighbhor_node_height = 0
				if (abs(current_node_height- neighbhor_node_height)>max_rock_height):
					continue
				neighbhor_cost = 1 + path_cost_till_now 
				if str(neighbhor) not in cost_till_now or neighbhor_cost < cost_till_now[str(neighbhor)]:
					cost_till_now[str(neighbhor)] = neighbhor_cost 	
					frontier.append(neighbhor)
					parent[str(neighbhor)] = str(current_node)
				
		if not is_present:
			with open("output.txt", "a+") as f:
				f.write("FAIL"+"\n")
			print("FAIL")
	return

# This is a utility function to read input.txt and parse inputs like Algortithm name, source and target nodes, the meshgrid of the trail etc. and store them into appropriate variables.
def parse_input(): 
	with open("input.txt") as f:
		input_lines = f.readlines()
	algo_name = input_lines[0].strip().lower()
	W = int(input_lines[1].split()[0].strip())
	H = int(input_lines[1].split()[1].strip())
	start_x = int(input_lines[2].split()[0].strip())
	start_y = int(input_lines[2].split()[1].strip())
	max_rock_height = int(input_lines[3])
	number_of_settling_sites = int(input_lines[4])
	settling_sites = []
	for i in range(number_of_settling_sites):
		settling_sites.append([input_lines[5+i].split()[0], input_lines[5+i].split()[1]])
	for i in settling_sites:
		i[0] = int(i[0])
		i[1] = int(i[1])
	land_map = []
	for i in range(H):
		buff = []
		for row in input_lines[5+number_of_settling_sites+i].split():
			buff.append(int(row.strip()))
		land_map.append(buff)
	return algo_name, W, H, start_x, start_y, max_rock_height, number_of_settling_sites, settling_sites, land_map

algo_name, W, H, start_x, start_y, max_rock_height, number_of_settling_sites, settling_sites, land_map = parse_input()
land_map = [[land_map[j][i] for j in range(len(land_map))] for i in range(len(land_map[0]))]
if (algo_name == "bfs"):
	bfs_path_finder(W, H, start_x, start_y, max_rock_height, number_of_settling_sites, settling_sites, land_map)
elif (algo_name == "ucs"):
	ucs_path_finder(W, H, start_x, start_y, max_rock_height, number_of_settling_sites, settling_sites, land_map)
elif (algo_name == "a*"):
	A_star_path_finder(W, H, start_x, start_y, max_rock_height, number_of_settling_sites, settling_sites, land_map)

