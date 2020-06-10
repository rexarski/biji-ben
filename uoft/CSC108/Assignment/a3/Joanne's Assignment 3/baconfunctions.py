def find_connection(actor_name, actor_dict, movie_dict):
    '''Return a list of (movie, actor) tuples that represent a shortest 
    connection between actor_name and Kevin Bacon that can be found in the 
    actor_dict and movie_dict. If there is no connection between actor_name
    and Kevin Bacon, the returned list is empty.
    '''
    
    # actor_distance is a dict, mapping each investigated actor to 
    # to his/her distance to "actor_name"
    actor_distance = actor_distance_dict(actor_name, actor_dict, movie_dict)

    connection = []
    bacon_num = actor_distance["Kevin Bacon"]
    current_actor = "Kevin Bacon"
    next_actor = ""
    
    # Built the shortest connection from Kevin Bacon to "actor_name" 
    for current_distance in range(bacon_num, 0, -1):
        next_actor, movie = get_previous_link(current_distance, current_actor,\
                                          actor_dict, movie_dict)
        connection.insert(0, (movie, current_actor))       
        current_actor = next_actor
    
    return connection

def get_previous_link(current_distance, current_actor, actor_dict, movie_dict):
    '''Return the actor who comes before current_actor and the movie they share
    in the shortest path between Kevin Bacon and the actor_name inputted 
    by user. 
    '''
    
    for movie in actor_dict[current_actor]:
        for actor in movie_dict[movie]:
            if actor_distance[actor] == current_distance - 1:
                return actor, movie
    
def actor_distance_dict(actor_name, actor_dict, movie_dict):
    '''Return the number of movies required to connect actor_name and 
    Kevin Bacon that can be found in actor_dict and movie_dict.
    Return -1 if there is no connection.'''
    
    investigated = {actor_name: 0}
    to_investigate = [actor_name]
    to_investigate_distances = [0]
    
    path = []
    
    while to_investigate != []:
        investigating = to_investigate.pop([0])
        current_distance = distances.pop([0])
        investigated[investigating] = current_distance
        
        if investigating == "Kevin Bacon":
            return investigated
        
        for movie in actor_dict[investigating]:
            for co_star in movie_dict[movie]:
                if co_star == "Kevin Bacon":
                    distance = current_distance + 1
                    investigated["Kevin Bacon"] = distance
                    return investigated
                
                if co_star not in investigated and co_star not in to_investigate:
                    to_investigate.append(co_star)
                    to_investigate_distance.append(current_distance + 1)
                
    return investigated