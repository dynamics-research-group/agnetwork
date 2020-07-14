import pandas as pd
import json
import time
import re
import ast

timestamp_conversion_factor = 10**9
json_export_directory = "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json"

def import_IE_from_excel(structure, file_path, population=None):
	if structure == None or file_path == None: return 

	name = structure
	timestamp = time.time() * timestamp_conversion_factor
	structure_dict = {"name": name,
					  "timestamp": int(timestamp),
					  "irreducible_element_model": {
						  "number_of_elements": 0,
						  "number_of_joints": 0,
						  "metadata": {},
						  "elements": [],
						  "joints": []
					  	}
					 }
	if population != None:
		structure_dict["population"] = population

	elements_raw = pd.read_excel(file_path, sheet_name='Elements')
	elements = elements_raw.loc[:, ~elements_raw.columns.str.contains('^Unnamed')].dropna()
	elements_json_str = elements.to_json(indent=2, orient="records").lower()
	elements_list = json.loads(elements_json_str)

	for element in elements_list:
		element_dict = {}
		material_dict = {}
		shape_dict = {}

		for key, value in element.items():
			# print(f"Key:{key}, value: {value}")
			if "description" in key: element_dict["description"] = value
			if "name" in key: element_dict["name"] = value
			if "material" in key:
				if "class" not in key and "properties" not in key: 
					material_dict["name"] = value
			if "material" in key and "class" in key: material_dict["class"] = value
			if "material" in key and "properties" in key: material_dict["properties"] = create_properties_object(value)
			if "shape" in key: shape_dict["name"] = value
			if "geometry class" in key: shape_dict["class"] = value
			if "dimensions" in key: shape_dict["dimensions"] = create_properties_object(value)
		
		element_dict["material"] = material_dict
		element_dict["shape"] = shape_dict
		element_dict["metadata"] = {}
		element_dict["type"] = "regular"

		structure_dict["irreducible_element_model"]["elements"].append(element_dict)

	boundary_raw = pd.read_excel(file_path, sheet_name='Boundary conditions')
	boundary = boundary_raw.loc[:, ~boundary_raw.columns.str.contains('^Unnamed')].dropna()
	boundary_json_str = boundary.to_json(indent=2, orient="records").lower()
	boundary_list = json.loads(boundary_json_str)

	for boundary in boundary_list:
		boundary_dict = {key: str(value) for key, value in boundary.items()}
		boundary_dict["metadata"] = {}
		boundary_dict["type"] = "boundary-condition"
		structure_dict["irreducible_element_model"]["elements"].append(boundary_dict)

	joints_raw = pd.read_excel(file_path, sheet_name='Joints')
	joints = joints_raw.loc[:, ~joints_raw.columns.str.contains('^Unnamed')].dropna()
	joints_json_str = joints.to_json(indent=2, orient="records").lower()
	joints_list = json.loads(joints_json_str)

	for joint in joints_list:
		joint_dict = {}
		coordinates_dict = {}
		degrees_of_freedom_dict = {}
		displacement_dof_dict = {}
		rotational_dof_dict = {}

		for key, value in joint.items():
			# print(f"Key:{key}, value: {value}")
			if "name" in key: joint_dict["name"] = value
			if "element set" in key: joint_dict["element set"] = [e.strip() for e in re.split(",", value)]
			if "x-location" in key: coordinates_dict["x"] = value
			if "y-location" in key: coordinates_dict["y"] = value
			if "z-location" in key: coordinates_dict["z"] = value
			if "type" in key: joint_dict["type"] = value
			if "disp dof" in key: displacement_dof_dict = create_degrees_of_freedom_object(value)
			if "rot dof" in key: rotational_dof_dict = create_degrees_of_freedom_object(value)
			
			if displacement_dof_dict != {}:
				degrees_of_freedom_dict["displacement"] = displacement_dof_dict
			if rotational_dof_dict != {}:
				degrees_of_freedom_dict["rotational"] = rotational_dof_dict
			if degrees_of_freedom_dict != {}:
				joint_dict["restricted_degrees_of_freedom"] = degrees_of_freedom_dict

		joint_dict["coordinates"] = coordinates_dict
		joint_dict["metadata"] = {}
		structure_dict["irreducible_element_model"]["joints"].append(joint_dict)

	with open (f"{json_export_directory}/{structure}.json", "w") as outfile:
		json.dump(structure_dict, outfile, indent=4)

def create_properties_object(properties):
	properties_object = []
	split_properties = re.split(",", properties)
	for p in split_properties:
		split = re.split(":", p.strip())
		name = split[0]
		to_split = split[1].strip()
		for i, c in reversed(list(enumerate(to_split))):
			if c.isdigit():
				break	
		value=float(to_split[:i+1])
		units=to_split[i+1:]
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
		degrees_of_freedom_object[dof.strip()] = {}
	return degrees_of_freedom_object

if __name__ == "__main__":
	import_IE_from_excel('IE example', 
						 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/IE example.xlsx")
	# import_IE_from_excel('Aeroplane 1', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Aeroplane 1.xlsx")
	# import_IE_from_excel('Bridge 1', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 1.xlsx")