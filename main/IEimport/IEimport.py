import pandas as pd
import json
import time
import re
from pprint import pprint
import math

timestamp_conversion_factor = 10**9
import_na_values = ['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', 
				   	' ', 'NULL', '#NA', 'null', 'NaN', '-NaN', 'nan', '-nan', '']
new_json_export_directory = "/Users/Julian/Documents/WorkDocuments/Python/pbshm-schema/docs"

# Create list of unique entries for each column
material_list = []
geometry_class_list = []
shape_list = []
joint_type_list = []

material_mapping_dict = {'FRP' : {"name" : "composite", "type" : {"name" : "fibre-reinforced"}}, 
						'Assembly' : {"name" : "metal", "type": {"name": "aluminiumAlloy"}}, 
						'Aluminium' : {"name" : "metal", "type" : {"name" : "aluminiumAlloy"}}, 
						'Concrete' : {"name" : "ceramic", "type" : {"name" : "cement"}}, 
						'Steel' : {"name" : "metal", "type": {"name" : "ferrousAlloy", "type" : {"name" : "steel"}}}, 
						'Reinforced Concrete' : {"name" : "composite", "type" : {"name" : "fibre-reinforced"}}, 
						'Reinfoced Concrete': {"name" : "composite", "type" : {"name" : "fibre-reinforced"}},
						'Mixed' : {"name" : "composite", "type" : {"name" : "fibre-reinforced"}},
						'Steele, Concrete' : {"name" : "composite", "type" : {"name" : "fibre-reinforced"}},
						'Steel, Concrete' : {"name" : "composite", "type" : {"name" : "fibre-reinforced"}},
						'Encased Concrete' : {"name" : "composite", "type" : {"name" : "fibre-reinforced"}}
						}
geometry_class_mapping_dict = { 'Beam' : 'beam',
								'Plate' : 'plate', 
								'Slab' : 'slab', 
								'Column' : 'column', 
								'Beam ' : 'beam', 
								'Wall' : 'wall', 
								'Cable' : 'cable', 
								'Block' : 'block',
								'Fuselage' : 'fuselage',
								'Tower' : 'tower',
								'Other' : 'other'}
shape_mapping_dict = 	{'Truncated cone' : {"name" : "shell", "type" : {"name" : "translateAndScale", "type" : {"name" : "cylinder"}}},	
						'Cylindrical' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cylinder"}}}, 
						'Cone': {"name" : "shell", "type" : {"name" : "translateAndScale", "type" : {"name" : "cylinder"}}}, 
						'Aerofoil' : {"name" : "beam", "type": { "name": "other" }}, 
						'Pylon' : {"name" : "beam", "type": { "name": "other" }}, 
						'Assembly' : {"name" : "beam", "type": { "name": "other" }}, 
						'Rotor hub' : {"name" : "shell", "type" : {"name" : "translateAndScale", "type" : {"name" : "cylinder"}}}, 
						'Trapezoid' : {"name" : "shell", "type" : {"name" : "translateAndScale", "type" : {"name" : "cuboid"}}}, 
						'U' : {"name" : "beam", "type": { "name": "other" }}, 
						'Continuous Slab' : {"name" : "plate", "type" : {"name" : "rectangular"}}, 
						'SHS' : {"name" : "beam", "type": { "name": "other" }}, 
						'RHS' : {"name" : "beam", "type": { "name": "other" }}, 
						'Hollow cylinder' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cylinder"}}}, 
						'Ribbed Plate' : {"name" : "plate", "type" : {"name" : "rectangular"}},
						'Ribbed (Solid)' : {"name" : "plate", "type" : {"name" : "rectangular"}},
						'I' : {"name" : "beam", "type" : {"name" : "i-beam"}},
						'I Beam' : {"name" : "beam", "type" : {"name" : "i-beam"}},
						'Box (Hollow)': {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'Box (Solid)': {"name" : "solid", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'I beam' : {"name" : "beam", "type" : {"name" : "i-beam"}},
						'Cylinder (Solid)' : {"name" : "solid", "type" : {"name" : "translate", "type" :  {"name" : "cylinder"}}},
						'CHS' : {"name" : "beam", "type": { "name": "other" }},
						'Cylinder (hollow)' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cylinder"}}},
						'Cylinder Hollow' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cylinder"}}},
						'Cylinder Solid' : {"name" : "solid", "type" : {"name" : "translate", "type" :  {"name" : "cylinder"}}},
						'Trapezoid Hollow' : {"name" : "shell", "type" : {"name" : "translateAndScale", "type" : {"name" : "cuboid"}}},
						'Cuboid Hollow' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'Trapezoid (Hollow)' : {"name" : "shell", "type" : {"name" : "translateAndScale", "type" : {"name" : "cuboid"}}},
						'Cylinder (Hollow)' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cylinder"}}},
						'Cylinder\nHollow' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cylinder"}}},
						'Beam' : {"name" : "beam", "type": { "name": "other" }},
						'Rectangular Beam' : {"name" : "beam", "type" : {"name" : "rectangular"}},
						'Plate' : {"name" : "plate", "type": { "name": "other" }},
						'Rectangular' : {"name" : "plate", "type" : {"name" : "rectangular"}},
						'Rectangular Plate' : {"name" : "plate", "type" : {"name" : "rectangular"}},
						'Rectangular box' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'Cylinder' : {"name" : "solid", "type" : {"name" : "translate", "type" :  {"name" : "cylinder"}}},
						'Cylinder ' : {"name" : "solid", "type" : {"name" : "translate", "type" :  {"name" : "cylinder"}}},
						'Cuboid' : {"name" : "solid", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'Cuboid ' : {"name" : "solid", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'Cuboid (Solid)' : {"name" : "solid", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'Cuboid (shell)' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'Cuboid (Hollow)' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'Square' : {"name" : "solid", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}},
						'Square Hollow' : {"name" : "shell", "type" : {"name" : "translate", "type" : {"name" : "cuboid"}}}
						}
joint_type_mapping_dict = 	{'Lug' : {"name" : "static", "nature" : {"name" : "bolted"}}, 
							'Complex' : {"name" : "static", "nature" : {"name" : "bolted"}}, 
							'Friction' : {"name" : "dynamic", "nature" : {"name" : "other"}}, 
							'Clamped' : {"name" : "static", "nature" : {"name" : "other"}}, 
							'Bolted' : {"name" : "static", "nature" : {"name" : "bolted"}}, 
							'Bearing' : {"name" : "dynamic", "nature" : {"name" : "other"}}, 
							'Bearing ' : {"name" : "dynamic", "nature" : {"name" : "other"}}, 
							'Soil' : {"name" : "static", "nature" : {"name" : "other"}}, 
							'Fixed' : {"name" : "static", "nature" : {"name" : "other"}}, 
							'Expansion' : {"name" : "dynamic", "nature" : {"name" : "expansion"}}, 
							'Pin' : {"name" : "dynamic", "nature" : {"name" : "pinned"}}, 
							'Roller' : {"name" : "dynamic", "nature" : {"name" : "other"}}, 
							'roller' : {"name" : "dynamic", "nature" : {"name" : "other"}},
							'Simply supported' : {"name" : "dynamic", "nature" : {"name" : "other"}},
							'Joined' : {"name" : "static", "nature" : {"name" : "other"}},
							'Pinned' : {"name" : "dynamic", "nature" : {"name" : "other"}},
							'Splice' : {"name" : "static", "nature" : {"name" : "other"}}}

def discover_element_mappings(structure, file_path):
	if structure == None or file_path == None: return 
	elements_raw = pd.read_excel(file_path,
								 sheet_name='Elements',
								 keep_default_na=False,
								 na_values=import_na_values,
								 dtype=str)
	elements = elements_raw.loc[:, ~elements_raw.columns.str.contains('^Unnamed')].dropna(how='all')

	#Create Column Mappings
	column_mappings = {}
	index = 0
	for col in elements.columns:
		column_mappings[col.strip().lower()] = index
		index += 1

	#Enumerate through rows
	for index, row in elements.iterrows():
		if row[column_mappings["material"]] not in material_list:
			# print(row[columnMappings["material"]])
			material_list.append(row[column_mappings["material"]])
		if row[column_mappings["geometry class"]] not in geometry_class_list:
			geometry_class_list.append(row[column_mappings["geometry class"]])
		if row[column_mappings["shape"]] not in shape_list:
			shape_list.append(row[column_mappings["shape"]])

def discover_joint_mappings(structure, file_path):
	if structure == None or file_path == None: return
	joints_raw = pd.read_excel(file_path, 
							   sheet_name='Joints',
							   keep_default_na=False,
							   na_values=import_na_values, 
							   dtype=str)
	joints = joints_raw.loc[:, ~joints_raw.columns.str.contains('^Unnamed')].dropna(how='all')

	#Create Column Mappings
	columnMappings = {}
	index = 0
	for col in joints.columns:
		columnMappings[col.strip().lower()] = index
		index += 1

	for index, row in joints.iterrows():
		if row[columnMappings["type"]] not in joint_type_list:
			joint_type_list.append(row[columnMappings["type"]])

	# print(columnMappings)
	# print(joints)
	# print(math.isnan(joints['Disp DoF'][0]))
	# 'name' 'element set', 'x-location', 'y-location', 'z-location', 'type', 'disp dof', 'rot dof'

def import_IE_from_excel_new(name, file_path, population="testpopulation"):
	if name == None or file_path == None: return 

	timestamp = time.time() * timestamp_conversion_factor

	jsonNew = 	{"version": "1.1.0",
				"name": name,
				"population" : population,
				"timestamp": int(timestamp),
				"models": {
					"irreducibleElement": {
						"type" : "grounded",
						"elements": [],
						"relationships": []
						}
					}	
				}

	# Import IE model information
	elements_raw = pd.read_excel(file_path,
								 sheet_name='Elements',
								 keep_default_na=False,
								 na_values=import_na_values,
								 dtype=str)
	elements = elements_raw.loc[:, ~elements_raw.columns.str.contains('^Unnamed')].dropna(how='all')

	joints_raw = pd.read_excel(file_path, 
							   sheet_name='Joints',
							   keep_default_na=False,
							   na_values=import_na_values, 
							   dtype=str)
	joints = joints_raw.loc[:, ~joints_raw.columns.str.contains('^Unnamed')].dropna(how='all')

	boundary_raw = pd.read_excel(file_path, 
								 sheet_name='Boundary conditions', 
								 keep_default_na=False,
								 na_values=import_na_values,
								 dtype=str)
	boundary_conditions = boundary_raw.loc[:, ~boundary_raw.columns.str.contains('^Unnamed')].dropna()

	# Create Column Mappings
	columnMappings = {"elements" : {}, "joints" : {}, "boundary-conditions" : {}}
	index = 0
	for col in elements.columns:
		columnMappings["elements"][col.strip().lower()] = index
		index += 1

	index = 0
	for col in joints.columns:
		columnMappings["joints"][col.strip().lower()] = index
		index += 1

	index = 0
	for col in boundary_conditions.columns:
		columnMappings["boundary-conditions"][col.strip().lower()] = index
		index += 1
	
	# Enumerate through rows in elements
	for index, row in elements.iterrows():
		if row[columnMappings["elements"]["geometry class"]] not in geometry_class_mapping_dict:
			print(f'Error: geometry class \'{row[columnMappings["elements"]["geometry class"]]}\' not in mappings dictionary (Row:{index+2} in {file_path})')
			continue
		if row[columnMappings["elements"]["shape"]] not in shape_mapping_dict:
			print(f'Error: shape \'{row[columnMappings["elements"]["shape"]]}\' not in mappings dictionary (Row:{index+2} in {file_path})')
			continue
		if row[columnMappings["elements"]["material"]] not in material_mapping_dict:
			print(f'Error: material \'{row[columnMappings["elements"]["material"]]}\' not in mappings dictionary (Row:{index+2} in {file_path})')
			continue

		element = 	{"name" : row[columnMappings["elements"]["name"]],
					"type" : "regular",
					"contextual" : {
						"type" : geometry_class_mapping_dict[row[columnMappings["elements"]["geometry class"]]]
					},
					"geometry" : {
						"type" : shape_mapping_dict[row[columnMappings["elements"]["shape"]]]
					},
					"material" : {
						"type" : material_mapping_dict[row[columnMappings["elements"]["material"]]]
					}
					}
		# print(element)
		jsonNew["models"]["irreducibleElement"]["elements"].append(element)

	# Enumerate through rows in joints
	jsonJoints = []
	for index, row in joints.iterrows():
		joint  = {}
		joint["name"] = row[columnMappings["joints"]["joint id"]]

		coordinates_object = {"global": {
										"translational": {
											"x": {"unit": "m", "value": check_and_convert_to_numeric(row[columnMappings["joints"]["x-location"]], index, file_path)},
											"y": {"unit": "m", "value": check_and_convert_to_numeric(row[columnMappings["joints"]["y-location"]], index, file_path)},
											"z": {"unit": "m", "value": check_and_convert_to_numeric(row[columnMappings["joints"]["z-location"]], index, file_path)}
										}
									}}
		element_set = [e.strip() for e in re.split(",", row[columnMappings["joints"]["element set"]])]
		if row[columnMappings["joints"]["type"]] == "Perfect":
			joint["type"] = "perfect"
			joint["coordinates"] = coordinates_object
			element_set = [e.strip() for e in re.split(",", row[columnMappings["joints"]["element set"]])]
			joint["elements"] = []
			for element in element_set:
				joint["elements"].append({"name" : element})
			# pprint(joint, indent=2)
			jsonNew["models"]["irreducibleElement"]["relationships"].append(joint)
		elif row[columnMappings["joints"]["type"]] not in joint_type_mapping_dict:
			print(f'Error: joint type \'{row[columnMappings["joints"]["type"]]}\' not in mappings dictionary(Row:{index+2} in {file_path})')
		elif len(element_set) > 2:
			joint["type"] = "connection"
			joint["elements"] = []
			for element in element_set:
				joint["elements"].append({"name" : element, "coordinates" : coordinates_object, "nature" : {"name" : "static", "nature" : {"name" : "other"} } } )
		else:
			joint["type"] = "joint"
			joint["nature"] = joint_type_mapping_dict[row[columnMappings["joints"]["type"]]]
			if joint["nature"]["name"] == "dynamic":
				if type(row[columnMappings["joints"]["disp dof"]]) == str: 
					joint["degreesOfFreedom"] = { "global" : {}} 
					joint["degreesOfFreedom"]["global"]["translational"] = translational_degrees_of_freedom_object(row[columnMappings["joints"]["disp dof"]])
				if type(row[columnMappings["joints"]["rot dof"]]) == str:
					if "degreesOfFreedom" not in joint: 
						joint["degreesOfFreedom"] = { "global" : {}} 
						joint["degreesOfFreedom"]["global"]["rotational"] = rotational_degrees_of_freedom_object(row[columnMappings["joints"]["rot dof"]])
					else:
						joint["degreesOfFreedom"]["global"]["rotational"] = rotational_degrees_of_freedom_object(row[columnMappings["joints"]["rot dof"]])
				if "degreesOfFreedom" not in joint:
					print(f'Error: dynamic joint has no dof information in Row:{index+2} in {file_path}')
			joint["elements"] = []
			for element in element_set:
				joint["elements"].append({"name" : element,
											"coordinates" : coordinates_object})
		jsonNew["models"]["irreducibleElement"]["relationships"].append(joint)
		# pprint(joint, indent=2)

	for index, row in boundary_conditions.iterrows():
		boundaryCondition = {}
		boundaryCondition["name"] = row[columnMappings["boundary-conditions"]["name"]]
		boundaryCondition["type"] = "ground"
		jsonNew["models"]["irreducibleElement"]["elements"].append(boundaryCondition)
	
	with open (f"{new_json_export_directory}/{name}.json", "w") as outfile:
		json.dump(jsonNew, outfile, indent=4)

	# print(jsonBoundaryConditions)


	# print(f"For {file_path} we have the following elements:")
	# print(jsonElements)
	
	# For geometry, shape, material create list of entries and decide what we need to do with them

	#print(elements)
	#elements_json_str = elements.to_json(indent=2, orient="records").lower()
	#print(elements_json_str)
	#elements_list = json.loads(elements_json_str)


def import_IE_from_excel(structure, file_path, json_export_directory, population=None, debug=False):
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
	# print(elements_list)

	# iterate through dataframe rows
	for element in elements_list:
		element_dict = {}

		for key, value in element.items():
			if debug == True:
					print(f"Key:{key}, value: {value}")
			if value != None:
				if "description" in key: 
					element_dict["description"] = value.strip()
				if "name" in key or "element id" in key: 
					element_dict["name"] = str(value).strip()
				if "material" in key:
					if "material" not in element_dict:
						element_dict["material"] = {}
					if "class" not in key and "properties" not in key: 
						element_dict["material"]["name"] = value.strip()
					elif "class" in key:
						element_dict["material"]["class"] = value.strip()
					elif "properties" in key:
						properties = create_properties_object(value)
						if properties != []:
							element_dict["material"]["properties"] = properties	
				if "shape" in key: 
					if "shape" not in element_dict:
						element_dict["shape"] = {}
					element_dict["shape"]["name"] = value.strip()
				if "geometry class" in key: 
					if "shape" not in element_dict:
						element_dict["shape"] = {}
					element_dict["shape"]["class"] = value.strip()
				if "dimensions" in key: 
					if "shape" not in element_dict:
						element_dict["shape"] = {}
					dimensions = create_properties_object(value)
					if dimensions != []:
						element_dict["shape"]["dimensions"] = dimensions
		
		element_dict["metadata"] = {}
		element_dict["type"] = "regular"

		# print("element")
		# pprint(element_dict,indent=2)

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
		boundary_dict = {str(key).strip(): str(value).strip() for key, value in boundary.items()}
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
				if "name" in key or "joint id" in key: joint_dict["name"] = value.strip()
				if "element set" in key or "joint set" in key: 
					joint_dict["element_set"] = [e.strip() for e in re.split(",", value)]
				if "location" in key:
					if "coordinates" not in joint_dict:
						joint_dict["coordinates"] = {}
					if "x-location" in key: 
						joint_dict["coordinates"]["x"] = value
					if "y-location" in key: 
						joint_dict["coordinates"]["y"] = value
					if "z-location" in key: 
						joint_dict["coordinates"]["z"] = value
				if "type" in key: joint_dict["type"] = value.strip()
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

	print(f"{json_export_directory}{structure}.json")
	with open (f"{json_export_directory}{structure}.json", "w") as outfile:
		json.dump(structure_dict, outfile, indent=4)

def create_properties_object(properties):
	properties_object = []
	split_properties = re.split(",", properties)
	for p in split_properties:
		p = p.strip()
		split = re.split(":", p)
		if len(split) == 2:
			name = split[0].strip()
			to_split = split[1].strip()
			for i, c in reversed(list(enumerate(to_split))):
				if c.isdigit():
					break	
			if i != 0:
				value = float(to_split[:i+1])
				units = to_split[i+1:].strip()
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

def translational_degrees_of_freedom_object(degrees_of_freedom):
	degrees_of_freedom_object = {}
	split_degrees_of_freedom = re.split(",", degrees_of_freedom)
	for dof in split_degrees_of_freedom:
		dof = dof.replace('[','')
		dof = dof.replace(']','')
		dof = dof.strip()
		degrees_of_freedom_object[dof] = {"unit": "mm", "minimum": 0, "maximum": 1}
	return degrees_of_freedom_object

def rotational_degrees_of_freedom_object(degrees_of_freedom):
	degrees_of_freedom_object = {}
	split_degrees_of_freedom = re.split(",", degrees_of_freedom)
	for dof in split_degrees_of_freedom:
		dof = dof.replace('[','')
		dof = dof.replace(']','')
		dof = dof.strip()
		if dof == 'x':
			degrees_of_freedom_object["alpha"] = {"unit": "degrees", "minimum": 0, "maximum": 1}
		elif dof == 'y':
			degrees_of_freedom_object["beta"] = {"unit": "degrees", "minimum": 0, "maximum": 1}
		elif dof == 'z':
			degrees_of_freedom_object["gamma"] = {"unit": "degrees", "minimum": 0, "maximum": 1}
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
		try:
			graph[element["name"]] = []
			if "shape" in element.keys():
				attributes[element["name"]] = element["shape"]["class"]
				list_of_nodes.append(element["name"])
			else:
				attributes[element["name"]] = "N/A"
				list_of_nodes.append(element["name"])
		except:
			print(element)

	for joint in structure["irreducible_element_model"]["joints"]:
		for element1 in joint["element_set"]:
			for element2 in joint["element_set"]:
				if element1 != element2:
					graph[element1].append(element2)
		list_of_edges.append(joint["element_set"])

	# pprint(graph,indent=2)

	structure["attributed_graph"] = {}
	structure["attributed_graph"]["counts"] = {"elements": number_of_elements,
											   "joints": number_of_joints}
	structure["attributed_graph"]["graph"] = graph
	structure["attributed_graph"]["attributes"] = attributes
	structure["attributed_graph"]["nodes"] = list_of_nodes
	structure["attributed_graph"]["edges"] = list_of_edges

	with open(file_path, "w") as outfile:
		json.dump(structure, outfile, indent=4)

	return structure["attributed_graph"]

def check_and_convert_to_numeric(value, index, file_path):
	if type(value) == int:
		return value
	elif type(value) == float:
		if math.isnan(value):
			print(f'Nan value found on Row:{index+2} in {file_path}')
		else:
			return value
	elif type(value) == str:
		try:
			return int(value)
		except ValueError:
			return float(value)

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
	# import_IE_from_excel('Aeroplane 2', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Aeroplane 2.xlsx")
	# import_IE_from_excel('Bridge 2', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 2.xlsx")
	# import_IE_from_excel('Bridge 3', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 3.xlsx")
	# import_IE_from_excel('Turbine 1', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Turbine 1.xlsx")

	# discover_joint_mappings('Aeroplane 1', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Aeroplane 1.xlsx")
	# discover_joint_mappings('Bridge 1', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 1.xlsx")
	# discover_joint_mappings('Aeroplane 2', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Aeroplane 2.xlsx")
	# discover_joint_mappings('Bridge 2', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 2.xlsx")
	# discover_joint_mappings('Bridge 3', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 3.xlsx")
	# discover_joint_mappings('Turbine 1', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Turbine 1.xlsx")
	# discover_joint_mappings('Castledawson', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Castledawson_Deck_Bridge_IEM.xlsx")
	# discover_joint_mappings('Randallstown', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Randallstown_West_Deck_Bridge_IEM.xlsx")
	# discover_joint_mappings('Drumderg', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Drumderg_Footbridge_IEM.xlsx")
	# discover_joint_mappings('Brough_Road', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Brough_Road_Footbridge_IEM.xlsx")
	# discover_joint_mappings('Toome', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Toome_Arch_Bridge_IEM.xlsx")
	# discover_joint_mappings('Baker', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Baker_Bridge_IEM.xlsx")
	# discover_joint_mappings('Humber', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Humber_Bridge_IEM.xlsx")
	# discover_joint_mappings('Bosphorous_Original', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Bosphorous_Original_IEM.xlsx")
	# discover_joint_mappings('Bosphorous_Repaired', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Bosphorous_Repaired_IEM.xlsx")

	# print(joint_type_list)

	# import_IE_from_excel_new('Aeroplane 1', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Aeroplane 1.xlsx")
	# import_IE_from_excel_new('Bridge 1', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 1.xlsx")
	# import_IE_from_excel_new('Aeroplane 2', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Aeroplane 2.xlsx")
	# import_IE_from_excel_new('Bridge 2', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 2.xlsx")
	# import_IE_from_excel_new('Bridge 3', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 3.xlsx")
	# import_IE_from_excel_new('Turbine 1', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Turbine 1.xlsx")
	# import_IE_from_excel_new('Castledawson', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Castledawson_Deck_Bridge_IEM.xlsx")
	# import_IE_from_excel_new('Randallstown', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Randallstown_West_Deck_Bridge_IEM.xlsx")
	# import_IE_from_excel_new('Drumderg', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Drumderg_Footbridge_IEM.xlsx")
	# import_IE_from_excel_new('Brough_Road', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Brough_Road_Footbridge_IEM.xlsx")
	# import_IE_from_excel_new('Toome', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Toome_Arch_Bridge_IEM.xlsx")
	# import_IE_from_excel_new('Baker', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Baker_Bridge_IEM.xlsx")
	# import_IE_from_excel_new('Humber', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Humber_Bridge_IEM.xlsx")
	# import_IE_from_excel_new('Bosphorous_Original', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Bosphorous_Original_IEM.xlsx")
	# import_IE_from_excel_new('Bosphorous_Repaired', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/04-12-20/Bosphorous_Repaired_IEM.xlsx")

	import_IE_from_excel_new('Z24-measurements', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Z24.xlsx", population="realbridges")
	import_IE_from_excel_new('S101-no-measurements', "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Z24.xlsx", population="realbridges")