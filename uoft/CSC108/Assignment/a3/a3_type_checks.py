'''This module should be used to test the parameter and return types of your
functions.  Run this on your a3_functions.py and make sure there are no errors
before submitting.'''

import a3_functions

if __name__ == '__main__':
	
	# Type check a3_functions.load_profiles
	profiles_file = open('profiles.txt')
	person_to_friends = {}
	person_to_networks = {}
	
	result = a3_functions.load_profiles(profiles_file, person_to_friends, 
	person_to_networks)
	assert isinstance(result, type(None)),\
	'''a3_functions.load_profiles should return a None, 
	but returned %s.''' % (type(result))
	
	
	# Type check a3_functions.invert_networks_dict
	person_to_networks = \
	{'Cameron Tucker': ['Clown School', 'Wizard of Oz Fan Club'],
	'Gloria Pritchett': ['Parent Teacher Association']}
	
	result = a3_functions.invert_networks_dict(person_to_networks)
	assert isinstance(result, dict),\
	'''a3_functions.invert_networks_dict should return a 
	dict of {str : list of strs}, but returned %s.''' % (type(result))

	for (key, value) in result.items():	
		assert isinstance(key, str),\
		'''a3_functions.invert_networks_dict should return a 
		dict of {str : list of strs}, but a key in the dict has %s.'''\
		 % (type(key))
		assert isinstance(value, list),\
		'''a3_functions.invert_networks_dict should return a 
		dict of {str : list of strs}, but a value in the dict has %s.'''\
		 % (type(value))
		for item in value:
			assert isinstance(item, str),\
			'''a3_functions.invert_networks_dict should return a 
			dict of {str : list of strs}, but an item in a values list
			has %s.'''\
			 % (type(item))
			
			
	# Type check a3_functions.make_recommendations
	person = 'Claire Dunphy'
	person_to_friends = \
	{'Jay Pritchett': ['Gloria Pritchett', 'Manny Delgado', 'Claire Dunphy'], 
	'Claire Dunphy': ['Phil Dunphy', 'Mitchell Pritchett', 'Jay Pritchett'], 
	'Manny Delgado': ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], 
	'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], 
	'Alex Dunphy': ['Luke Dunphy'], 
	'Cameron Tucker': ['Mitchell Pritchett', 'Gloria Pritchett'], 
	'Haley Gwendolyn Dunphy': ['Dylan D-Money'], 
	'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 
	'Dylan D-Money': ['Haley Gwendolyn Dunphy'], 
	'Gloria Pritchett': ['Jay Pritchett', 'Cameron Tucker', 'Manny Delgado'], 
	'Luke Dunphy': ['Manny Delgado', 'Alex Dunphy', 
	'Phil Dunphy', 'Mitchell Pritchett']}
	person_to_networks = \
	{'Phil Dunphy': ['Real Estate Association'], 
	'Claire Dunphy': ['Parent Teacher Association'], 
	'Manny Delgado': ['Chess Club'], 
	'Mitchell Pritchett': ['Law Association'], 
	'Alex Dunphy': ['Orchestra', 'Chess Club'], 
	'Cameron Tucker': ['Clown School', 'Wizard of Oz Fan Club'], 
	'Gloria Pritchett': ['Parent Teacher Association']}
	
	result = a3_functions.make_recommendations(\
	person, person_to_friends, person_to_networks)
	assert isinstance(result, list),\
	'''a3_functions.make_recommendations should return 
	a list of (str, int) tuples, but returned %s.''' % (type(result))

	for (name, score) in result:	
		assert isinstance(name, str),\
		'''a3_functions.make_recommendations should return a 
		list of (str, int) tuples, but the first element of a
		list tuple has %s.''' % (type(name))
		assert isinstance(score, int),\
		'''a3_functions.make_recommendations should return a 
		list of (str, int) tuples, but the second element of a 
		list tuple has %s.''' % (type(score))
		
		
	# Type check a3_sort_recommendations
	recommendations_list = [('Cameron Tucker', 1), ('Manny Delgado', 1)]
	
	result = a3_functions.sort_recommendations(recommendations_list)
	assert isinstance(result, list),\
	'''a3_functions.sort_recommendations should return a list of strs,
	 but returned %s.''' % (type(result))
	
	for item in result:
		assert isinstance(item, str),\
		'''a3_functions.sort_recommendations should return a list of strs,
		 but a list element has  %s.''' % (type(item))