import pandas as pd
import json
import time

timestamp_conversion_factor = 10**9
json_export_directory = "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json"

def import_IE_from_excel(structure, file_path, population=None):
	if structure == None or file_path == None: return 

	name = structure

	timestamp = time.time() * timestamp_conversion_factor

	structure_dict = {"name": name,
					  "population": population,
					  "timestamp": int(timestamp),
					  "irreducible_element_model": {
						  "number_of_elements": 0,
						  "number_of_joints": 0,
						  "metadata": {},
						  "elements": [],
						  "joints": []
					  	}
					 }

	elements = pd.read_excel (file_path, sheet_name='Elements')
	elements_json_str = elements.to_json(indent=2).lower()
	elements_json_dict = json.loads(elements_json_str)
	
	# print('Excel Sheet to JSON:\n', elements_json_str)

	if "name" in elements_json_dict:
		for i, element in enumerate(elements_json_dict["name"].values()):
			element_dict = {"name": f"element-{i}",
							"description": element,
							"type": "regular",
							"metadata": {}}
			structure_dict["irreducible_element_model"]["elements"].append(element_dict)
			print('Excel Sheet to JSON:\n', element)

	# joints = pd.read_excel (file_path, sheet_name='Joints')
	# boundary_conditions = pd.read_excel (file_path, sheet_name='Boundary conditions')

	with open (f"{json_export_directory}/{structure}.json", "w") as outfile:
		json.dump(structure_dict, outfile, indent=4)

if __name__ == "__main__":
	import_IE_from_excel('Aeroplane 1', 
						 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Aeroplane 1.xlsx")
	# import_IE_from_excel('Bridge 1', 
	# 					 "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/Excel/Bridge 1.xlsx")