import itertools
import json
import pprint

# Backtracking algorithm
def bound(graph1_modified, graph2_modified, graph1, graph2, current_solution, len_best_solution):
	len_current_solution = len(current_solution)
	if len(graph1_modified) + len_current_solution <= len_best_solution:
		return True
	elif len(graph2_modified) + len_current_solution <= len_best_solution:
		return True
	else:
		candidates = set()
		for vertex1 in graph1_modified:
			for vertex2 in  graph2_modified:
					if compatible_attributes(graph1[vertex1], graph2[vertex2]):
						candidates.add(vertex1)
		if len(candidates) + len_current_solution >= len_best_solution:
			return False
		else:
			return True

def backtrack(graph1, graph2, attributes1, graph2_attributed, filename='best.txt'):
	initial_solution = []
	#  graph2_modified = graph2.keys()
	graph2_modified = list(sort(graph2))
	graph1_modified = graph1.copy()
	len_best_solution = 0
	# return list(backtrack_algorithm(G1_dash, G2_dash, G1, G2, m_initial, best))
	with open('/Users/Julian/Documents/WorkDocuments/Irreducible Element/Random write/' + filename,'w') as f:
		f.write('MCS for graphs \n{0}\n{1}\n \n'.format(list(graph1.keys()), list(graph2.keys())))
	return [solution[0] for solution in list(backtrack_algorithm(graph1_modified, graph2_modified, 
							                       				 graph1, graph2, 
												   				 attributes1, graph2_attributed, 
												   				 initial_solution, len_best_solution, filename))]

def backtrack_algorithm(graph1_modified, graph2_modified,
						graph1, graph2, 
						attributes1, attributes2, 
						current_solution, len_best_solution, filename):
	# Create a list of nodes from G1 and G2 that have already been used to form the solution
	vertex1_list_int = [pair[0] for pair in current_solution]
	vertex2_list_int = [pair[1] for pair in current_solution]
	# ordered_nodes = (key for key in G1_dash.keys())
	ordered_nodes = sort(graph1_modified)
	while True:
			if bound(graph1_modified, graph2_modified, graph1, graph2, current_solution, len_best_solution):
				# This new solution cannot have exceed the current best estimate
				break
			try:
				vertex1 = next(ordered_nodes)
			except:
				# This new solution must exceed the current best estimate, update the best estimate
				len_best_solution = len(current_solution)
				print(len_best_solution)
				with open('/Users/Julian/Documents/WorkDocuments/Irreducible Element/Random write/' + filename,'a') as f:
					f.write('Length {0} \n{1}\n \n'.format(len_best_solution, current_solution))
				yield current_solution, len_best_solution
				break
			# Add the current v1 to the list of nodes that have been tried
			vertex1_list = vertex1_list_int + [vertex1] 
			for vertex2 in graph2_modified:
				# Check whether the new pair of nodes (v1, v2) can be added to the solution
				# print(AG1[v1])
				if compatible_attributes(attributes1[vertex1], attributes2[vertex2]):
					if compatible_connected(set(graph1[vertex1]), set(graph2[vertex2]), current_solution):
						if compatible_heuristic(set(graph1[vertex1]), set(graph2[vertex2]), current_solution):
							# Add the current v2 to the list of nodes that have been tried in this branch
							vertex2_list = vertex2_list_int + [vertex2]
							# Carry on down the tree
							for list_of_solutions in backtrack_algorithm({vertex1 : graph1_modified[vertex1] for vertex1 in graph1_modified if vertex1 not in vertex1_list}, 
																			[vertex2 for vertex2 in graph2_modified if vertex2 not in vertex2_list],
																			graph1, graph2,
																			attributes1, attributes2,
																			list(current_solution) + [(vertex1, vertex2)],
																			len_best_solution, filename): 
									# Find the length of the current best estimate
									if list_of_solutions[1] > len_best_solution: 
										len_best_solution = list_of_solutions[1]
									yield list_of_solutions
			# Remove the node v1 that has already been tried from the remaining graph G1_dash
			del graph1_modified[vertex1]

def sort(graph):
	sorted_graph = sorted(graph.items(), key = lambda item : len(item[1]), reverse=True)
	sorted_nodes = (node[0] for node in sorted_graph)
	return sorted_nodes

def compatible_connected(neighbourhood1, neighbourhood2, current_solution):
	# If no associations exist, any node is compatible
	if current_solution == []:
		return True
	else:
		for vertex1, vertex2 in current_solution:
			if vertex1 in neighbourhood1 and vertex2 in neighbourhood2:
				return True
		return False
	
def compatible_general(Nv1, Nv2, m):
	# If no associations exist, any node is compatible
	# Ensures graph is induced, but not necessarily connected
	if m == []:
		return True
	else:
		for pair in m:
				if pair[0] in Nv1 and pair[1] in Nv2:
					return True
				if pair[0] not in Nv1 and pair[1] not in Nv2:
					return True
		return False

def compatible_heuristic(neighbourhood1, neighbourhood2, current_solution):
	# My best guess as to the heuristic in the paper by Cao
	# Enforces induced subgraphs
	correspondence_set1 = set()
	correspondence_set2 = set()
	for pair_of_vertices in current_solution:
		vertex1, vertex2 = pair_of_vertices
		if vertex1 in neighbourhood1:
			correspondence_set1.add(pair_of_vertices)
		if vertex2 in neighbourhood2:
			correspondence_set2.add(pair_of_vertices)
	if len(correspondence_set1) == len(correspondence_set2):
		if correspondence_set1 == correspondence_set2:
			return True
	return False

def compatible_attributes(attributes1, attributes2):
	if attributes1 == attributes2: 
		# print(attributes1, attributes2)
		return True
	return False

def load_AG_from_json_file(file_path):
	with open(file_path, "r") as infile:
		structure = json.load(infile)
	return structure["attributed_graph"]

if __name__ == "__main__":
	directory = "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json/"

	# graph1_attributed = load_AG_from_json_file(f"{directory}Aeroplane 1.json")
	# # pprint.pprint(graph1_attributed,indent=2)

	# graph2_attributed = load_AG_from_json_file(f"{directory}Bridge 1.json")

	# print(backtrack(graph1_attributed["graph"], 
	# 				graph2_attributed["graph"], 
	# 				graph1_attributed["attributes"], 
	# 				graph2_attributed["attributes"]))
	
	graph1_attributed = load_AG_from_json_file(f"{directory}Randlestown.json")
	# pprint.pprint(graph1_attributed,indent=2)

	graph2_attributed = load_AG_from_json_file(f"{directory}Castledawson.json")

	print(backtrack(graph1_attributed["graph"], 
					graph2_attributed["graph"], 
					graph1_attributed["attributes"], 
					graph2_attributed["attributes"]))