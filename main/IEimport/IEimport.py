import pandas as pd

def import_IE_from_excel(structure, file_path, network=None):
	if structure == None or file_path == None: return network
	"""Read an excel file containing an IE model and add the AG 
	to a structure object"""
	# Import necessary information for the IE from the excel file
	elements = pd.read_excel (file_path, sheet_name='Elements', usecols="A:I")
	joints = pd.read_excel (file_path, sheet_name='Joints', usecols="A:H")
	boundary_conditions = pd.read_excel (file_path, sheet_name='Boundary conditions', usecols="A:C")