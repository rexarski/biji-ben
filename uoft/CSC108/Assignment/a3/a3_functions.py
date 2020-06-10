'''A friend recommendation system.

In a "person to friends" dictionary, each key is a person (str) and each value
is that person's friends (list of strs).

In a "person to networks" dictionary, each key is a person (str) and each value
is the networks that person belongs to (list of strs).

In a "network to people" dictionary, each key is a network (str) and each value
is the people belonging to that network (list of strs).'''


def load_profiles(profiles_file, person_to_friends, person_to_networks):
    '''(file, dict of {str : list of strs},
    dict of {str : list of strs}) -> NoneType
    Update the two dictionaries to include the data from the open file.'''

    # Doesn't work!!!

    f = profiles_file.readline()
    new_profile = True

    while f:
	f = f.strip()
	# A line of profile name
        if ',' in f and new_profile == True:
            a = f.split(', ')
	    key = a[1] + " " + a[0]
	    new_profile = False

	# A line of network
	elif ',' not in f and " " in f:
	    if key in person_to_networks:
		if f not in person_to_networks[key]:
		    person_to_networks[key].append(f)
	    else:
		person_to_networks[key] = [f]

	# A line of current friend
	elif ',' in f:
	    a = f.split(', ')
	    value = a[1] + " " + a[0]
	    if key in person_to_friends:
		if value not in person_to_friends[key]:
		    person_to_friends[key].append(value)
	    else:
		person_to_friends[key] = [value]
	    if value in person_to_friends:
		if key not in person_to_friends[value]:
		    person_to_friends[value].append(key)
	    else:
		person_to_friends[value] = [key]

	# Blank line
	else:
	    new_profile = True

	f = profiles_file.readline()


def invert_networks_dict(person_to_networks):
    '''(dict of {str : list of strs}) -> dict of {str : list of strs}
    Return a "network to people" dictionary based on the given
    "person to networks" dictionary. '''

    dic = {}
    keys = person_to_networks.keys()
    for i in keys:
	values = person_to_networks[i]
	for j in values:
	    if j in dic:
		dic[j].append(i)
	    else:
		dic[j] = [i]
    return dic


def make_recommendations(person, person_to_friends, person_to_networks):
    '''(str, dict of {str : list of strs},
    dict of {str : list of strs}) -> list of (str, int) tuples
    Using the recommendation system described above, return the friend
    recommendations for the given person in a list of tuples where the
    first element of each tuple is a potential friend's name (in the same
    format as the dictionary keys) and the second element is that potential
    friend's score. Only potential friends with non-zero scores should be
    included in the list. '''

    if person not in person_to_friends.keys():
	return []

    f = []
    myfriend = person_to_friends[person]
    key_names = person_to_friends.keys()
    for i in key_names:
	if i not in myfriend and i != person:
	    score = 0

	    for j in person_to_friends[i]:
		if j in myfriend:
		    score += 1

	    mynetwork = []
	    hisnetwork = []
	    if person in person_to_networks.keys():
		mynetwork = person_to_networks[person]
	    if i in person_to_networks.keys():
		hisnetwork = person_to_networks[i]
	    for network in hisnetwork:
		if network in mynetwork:
		    score += 1

	    if score != 0:
		mylastname = person.split(' ')[1]
		hislastname = i.split(' ')[1]
		if hislastname == mylastname:
		    score += 1
		f.append((i, score))
    return f


def sort_recommendations(recommendations):
    '''(list of (str, int) tuples) -> list of strs
    In the given list of tuples, the first element of each tuple is a potential
    friend's name (in the same format as the dictionary keys) and the second
    element is that potential friend's score.
    Return a list of potential friend's
    names ordered by score (highest to lowest).'''

    b = recommendations
    name = []
    score_name = []

    if len(b) == 0:
	return []
    else:
	for i in b:
	    tempname = i[0]
	    tempp = i[1]
	    score_name.append((tempp, tempname))
	score_name.sort()
	score_name.reverse()

	temp = [score_name[0]]
	for j in range(1, len(score_name)):
	    if score_name[j][0] == temp[0][0]:
		temp.append(score_name[j])
		temp.sort()
	    else:
		for i in temp:
		    name.append(i[1])
		temp = [score_name[j]]
	for i in temp:
	    name.append(i[1])
    return name
