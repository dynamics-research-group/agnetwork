import pandas as pd
import json
import time
import re
import ast
import pprint

timestamp_conversion_factor = 10**9
import_na_values = ['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', 
				   	' ', 'NULL', '#NA', 'null', 'NaN', '-NaN', 'nan', '-nan', '']
json_export_directory = "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json"

def import_IE_from_excel(structure, file_path, population=None, debug=False):
	if structure == None or file_path == None: return 

	name = structure
	timestamp = time.time() * timestamp_conversion_factor
	structure_dict = {"name": name,
					  "timestamp": int(timestamp),
					  "irreducible_element_model": {
						  "metadata": {},
						  "elements": [],
						  "joints": []
					  	}
					 }
	if population != None:
		structure_dict["population"] = population

	elements_raw = pd.read_excel(file_path,
								 sheet_name='Elements',
								 keep_default_na=False,
								 na_values=import_na_values,
								 dtype=str)
	elements = elements_raw.loc[:, ~elements_raw.columns.str.contains('^Unnamed')].dropna(how='all')
	# print(elements)
	elements_json_str = elements.to_json(indent=2, orient="records").lower()
	# print(elements_json_str)
	elements_list = json.loads(elements_json_str)

	# iterate through dataframe rows
	for element in elements_list:
		element_dict = {}

		for key, value in element.items():
			if debug == True:
					print(f"Key:{key}, value: {value}")
			if value != None:
				if "description" in key: 
					element_dict["description"] = value
				if "name" in key or "element id" in key: 
					element_dict["name"] = str(value)
				if "material" in key:
					if "material" not in element_dict:
						element_dict["material"] = {}
					if "class" not in key and "properties" not in key: 
						element_dict["material"]["name"] = value
					elif "class" in key:
						element_dict["material"]["class"] = value
					elif "properties" in key:
						properties = create_properties_object(value)
						if properties != []:
							element_dict["material"]["properties"] = properties	
				if "shape" in key: 
					if "shape" not in element_dict:
						element_dict["shape"] = {}
					element_dict["shape"]["name"] = value
				if "geometry class" in key: 
					if "shape" not in element_dict:
						element_dict["shape"] = {}
					element_dict["shape"]["class"] = value
				if "dimensions" in key: 
					if "shape" not in element_dict:
						element_dict["shape"] = {}
					dimensions = create_properties_object(value)
					if dimensions != []:
						element_dict["shape"]["dimensions"] = dimensions
		
		element_dict["metadata"] = {}
		element_dict["type"] = "regular"

		# print("element")
		# pprint.pprint(element_dict,indent=2)

		structure_dict["irreducible_element_model"]["elements"].append(element_dict)

	boundary_raw = pd.read_excel(file_path, 
								 sheet_name='Boundary conditions', 
								 keep_default_na=False,
								 na_values=import_na_values,
								 dtype=str)
	boundary = boundary_raw.loc[:, ~boundary_raw.columns.str.contains('^Unnamed')].dropna()
	boundary_json_str = boundary.to_json(indent=2, orient="records").lower()
	boundary_list = json.loads(boundary_json_str)

	for boundary in boundary_list:
		if debug == True:
			print(f"Boundary element:{boundary}")
		boundary_dict = {key: str(value) for key, value in boundary.items()}
		boundary_dict["metadata"] = {}
		boundary_dict["type"] = "boundary-condition"
		structure_dict["irreducible_element_model"]["elements"].append(boundary_dict)

	joints_raw = pd.read_excel(file_path, 
							   sheet_name='Joints',
							   keep_default_na=False,
							   na_values=import_na_values, 
							   dtype=str)
	joints = joints_raw.loc[:, ~joints_raw.columns.str.contains('^Unnamed')].dropna(how='all')
	joints_json_str = joints.to_json(indent=2, orient="records").lower()
	joints_list = json.loads(joints_json_str)

	for joint in joints_list:
		joint_dict = {}

		for key, value in joint.items():
			if debug == True:
					print(f"Key:{key}, value: {value}")
			if value != None:
				if "name" in key: joint_dict["name"] = value
				if "element set" in key or "joint set" in key: joint_dict["element_set"] = [e.strip() for e in re.split(",", value)]
				if "location" in key:
					if "coordinates" not in joint_dict:
						joint_dict["coordinates"] = {}
					if "x-location" in key: 
						joint_dict["coordinates"]["x"] = value
					if "y-location" in key: 
						joint_dict["coordinates"]["y"] = value
					if "z-location" in key: 
						joint_dict["coordinates"]["z"] = value
				if "type" in key: joint_dict["type"] = value
				if "dof" in key:
					if "restricted_degrees_of_freedom" not in joint_dict: 
						joint_dict["restricted_degrees_of_freedom"] = {}
					if "disp dof" in key:
						if "displacement" not in joint_dict["restricted_degrees_of_freedom"]:
							joint_dict["restricted_degrees_of_freedom"]["displacement"] = {}
						displacement_degrees_of_freedom = create_degrees_of_freedom_object(value)
						if displacement_degrees_of_freedom != []:
							joint_dict["restricted_degrees_of_freedom"]["displacement"] = displacement_degrees_of_freedom
					if "rot dof" in key: 
						if "rotational" not in joint_dict["restricted_degrees_of_freedom"]:
							joint_dict["restricted_degrees_of_freedom"]["rotational"] = {}
						rotational_degrees_of_freedom = create_degrees_of_freedom_object(value)
						if rotational_degrees_of_freedom != []:
							joint_dict["restricted_degrees_of_freedom"]["rotational"] = rotational_degrees_of_freedom

		joint_dict["metadata"] = {}
		structure_dict["irreducible_element_model"]["joints"].append(joint_dict)

	with open (f"{json_export_directory}/{structure}.json", "w") as outfile:
		json.dump(structure_dict, outfile, indent=4)

def create_properties_object(properties):
	properties_object = []
	split_properties = re.split(",", properties)
	for p in split_properties:
		p = p.strip()
		split = re.split(":", p)
		if len(split) == 2:
			name = split[0]
			to_split = split[1].strip()
			for i, c in reversed(list(enumerate(to_split))):
				if c.isdigit():
					break	
			value = float(to_split[:i+1])
			units = to_split[i+1:]
			# print(f"Name {name}, value: {value}, units:{units}")
			if units == '':
				properties_object.append({"name": name,
											"value": value})
			else: 
				properties_object.append({"name": name,
											"value": value,
											"units": units})
	return properties_object

def create_degrees_of_freedom_object(degrees_of_freedom):
	degrees_of_freedom_object = {}
	split_degrees_of_freedom = re.split(",", degrees_of_freedom)
	for dof in split_degrees_of_freedom:
		dof = dof.replace('[','')
		dof = dof.replace(']','')
		dof = dof.strip()
		degrees_of_freedom_object[dof] = {}
	return degrees_of_freedom_object

def acquire_inputs():
	# Get all inputs from command prompt
	# Create all inputs as a python dictionary
	# Save the python dictionary as a json config file

	# look at dan's pbshm flask core initialisation module, first method
	# (ignoring line 16) def initialise_sub_system_config from
	# https://github.com/dynamics-research-group/pbshm-flask-core/blob/master/pbshm/initialisation/initialisation.py

	pass

def generate_graph_from_json(file_path):

	with open(file_path, "r") as infile:
		structure = json.load(infile)

	graph = {}
	attributes = {}
	list_of_nodes = []
	list_of_edges = []

	number_of_elements = len(structure["irreducible_element_model"]["elements"])
	number_of_joints = len(structure["irreducible_element_model"]["joints"])

	for element in structure["irreducible_element_model"]["elements"]:
		graph[element["name"]] = []
		if "shape" in element.keys():
			attributes[element["name"]] = element["shape"]["class"]
		else:
			attributes[element["name"]] = "N/A"
		list_of_nodes.append(element["name"])

	for joint in structure["irreducible_element_model"]["joints"]:
		for element1 in joint["element_set"]:
			for element2 in joint["element_set"]:
				if element1 != element2:
					graph[element1].append(element2)
		list_of_edges.append(joint["element_set"])

	# pprint.pprint(graph,indent=2)

	structure["attributed_graph"] = {}
	structure["attributed_graph"]["counts"] = {"elements": number_of_elements,
											   "joints": number_of_joints}
	structure["attributed_graph"]["graph"] = graph
	structure["attributed_graph"]["attributes"] = attributes
	structure["attributed_graph"]["nodes"] = list_of_nodes
	structure["attributed_graph"]["edges"] = list_of_edges

	with open(file_path, "w") as outfile:
		json.dump(structure, outfile, indent=4)

if __name__ == "__main__":
	# See if json config file exists
	# Check if it has all of the required variables inside of it
	# (config file will be python dict so pass into import_IE_from_excel the correct values)
	# If any variables are missing or config file does not exist, call acquire_inputs

	# inputs json export name, json export path, excel import path, excel import name

	# import_IE_from_excel('IE example', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/IE example.xlsx",
	# 					 debug=False)

	# import_IE_from_excel('Aeroplane 1', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Aeroplane 1.xlsx")
	# import_IE_from_excel('Bridge 1', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 1.xlsx",
	# 					 debug=True)

	# generate_graph_from_json("/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json/Aeroplane 1.json")
	# generate_graph_from_json("/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json/Bridge 1.json")

	import_IE_from_excel('Castledawson', 
						 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Castledawson_Bridge_IEM_revB.xlsx")
	generate_graph_from_json("/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json/Castledawson.json")

	import_IE_from_excel('Randlestown', 
						 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Randlestown_West_Deck_Bridge.xlsx")
	generate_graph_from_json("/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json/Randlestown.json")

	# import_IE_from_excel('Drumderg', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Drumderg_Footbridge.xlsx")
	# generate_graph_from_json("/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json/Drumderg.json")

	# import_IE_from_excel('Brough_Road', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Brough_Road_Footbridge.xlsx")
	# generate_graph_from_json("/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json/Brough_Road.json")