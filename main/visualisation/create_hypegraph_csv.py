from tempfile import NamedTemporaryFile
import shutil
import csv
import json

def write_paoh_csv_from_json(file_path, name):
	# load structure from json specified in file_path
	with open(f"{file_path}{name}.json", 'r') as infile:
		structure = json.load(infile)
	with open(f"/Users/Julian/Documents/WorkDocuments/Irreducible Element/AGs/Hypergraphs/{name}.csv", 'w') as outfile:
		writer = csv.writer(outfile)
		# iterate through the joints in the ie model for the loaded structure
		for joint in structure["irreducible_element_model"]["joints"]:
			for node in joint["element_set"]:
				csv_entry = [joint["name"], node, 2020,'','']
				writer.writerow(csv_entry)

def highlight_mcs_in_csv(file_path, name, mcs, number):
	mcs_node_set = set()
	# create set of nodes is mcs
	for node_pair in mcs:
		if number == 1:
			mcs_node_set.add(node_pair[0])
		if number == 2:
			mcs_node_set.add(node_pair[1])
	print(mcs_node_set)
	# create tempfile to write to
	tempfile = NamedTemporaryFile('w+t', newline='', delete=False)
	# load csv where the mcs is to be highlighted, number determines whether graph was first or second in mcs
	with open(f"{file_path}{name}.csv", 'r') as csvfile, tempfile:
		reader = csv.reader(csvfile)
		writer = csv.writer(tempfile)
		for row in reader:
			if row[1] in mcs_node_set:
				row[4] = 'MCS'
			writer.writerow(row)
	shutil.move(tempfile.name, f"{file_path}{name}.csv")

def extract_mcs_from_csv(file_path, name, mcs, number):
	mcs_node_set = set()
	# create set of nodes is mcs
	for node_pair in mcs:
		if number == 1:
			mcs_node_set.add(node_pair[0])
		if number == 2:
			mcs_node_set.add(node_pair[1])
	print(mcs_node_set)
	# create tempfile to write to
	tempfile = NamedTemporaryFile('w+t', newline='', delete=False)
	# load csv where the mcs is to be highlighted, number determines whether graph was first or second in mcs
	with open(f"{file_path}{name}.csv", 'r') as csvfile, tempfile:
		reader = csv.reader(csvfile)
		writer = csv.writer(tempfile)
		for row in reader:
			if row[1] in mcs_node_set:
				writer.writerow(row)
	shutil.move(tempfile.name, f"{file_path}{name}_MCS_only.csv")

def extract_mcs_from_json(file_path, graph1, graph2, mcs):
	mcs_node_set1 = set()
	mcs_node_set2 = set()
	for node_pair in mcs:
		mcs_node_set1.add(node_pair[0])
		mcs_node_set2.add(node_pair[1])
	for graph, mcs_node_set in zip([graph1, graph2], [mcs_node_set1, mcs_node_set2]):
		with open(f"{file_path}{graph}.json", 'r') as infile:
			structure = json.load(infile)
		# find edges which have at least two elements from the mcs in them
		with open(f"/Users/Julian/Documents/WorkDocuments/Irreducible Element/MCS/{graph}_MCS.csv", 'w') as outfile:
			writer = csv.writer(outfile)
			# iterate through the joints in the ie model for the loaded structure
			for joint in structure["irreducible_element_model"]["joints"]:
				element_set = set(joint["element_set"])
				if len(element_set.intersection(mcs_node_set)) >= 2:
					for node in element_set:
						if node in mcs_node_set:
							csv_entry = [joint["name"], node, 2020,'','']
							writer.writerow(csv_entry)


if __name__ == "__main__":
	directory = "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json/"

	write_paoh_csv_from_json(directory, "Drumderg")

	directory2 = "/Users/Julian/Documents/WorkDocuments/Irreducible Element/MCS/"
	mcs = [('nd', 'df'), ('nc', 'if'), ('ne', 'db'), ('ns', 'dc'), ('df', 'dd'), ('dj', 'de'), ('dl', 'dg'), ('sv', 'dk'), ('sg', 'sf')]
	csv1 = "Drumderg_MCS_highlighted"
	csv2 = "Castledawson_MCS_highlighted"
	highlight_mcs_in_csv(directory2, csv2, mcs, 2)

	extract_mcs_from_csv(directory2, csv1, mcs, 1)

	graph1 = "Drumderg"
	graph2 = "Castledawson"
	extract_mcs_from_json(directory, graph1, graph2, mcs)