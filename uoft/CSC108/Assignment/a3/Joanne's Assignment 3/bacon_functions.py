def parse_actor_data(actor_data):
    '''Return the actor information in the open reader actor_data 
    as a dictionary. actor_data contains movie and actor information 
    in IMDB's format. The returned dictionary contains the names of 
    actors (string) as keys and lists of movies (string) the actor 
    has been in as values.
    '''
    
    # Actor_dict is the dictionary that will map actors to lists of movies
    actor_dict = {}
    
    read_header(actor_data)
    
    # Read_header(actor_data) stops at the line starts with '----',
    # Therefore, one more line should be read to get the first actor-movie line.
    line = actor_data.readline()
    
    # Using while loop to exclude the footer. 
    while not line.startswith('-') and line.strip() != '':
        # String name is the sliced string which the actor's name is in
        # But it is not in the correct format.
        # Therefore I name it raw_name
        raw_name = line[:line.find('\t')]
        
        # If the actor has last name,
        # Get the last name of the actor.
        if raw_name.find(',') != -1:
            # Last name is always before',', use find(',') to find the last name.
            last_name = raw_name[:raw_name.find(',')].strip()
            
            # Get the actor's first name
            first_name = raw_name[raw_name.find(',')+1:].strip()
            
            last_name_list = last_name.split()
            last_name = ''
            # In case the actor's last name has two words or even more,
            # Have each word in last_name capitalized by using for loop.
            for i in range(len(last_name_list)):
                last_name_list[i] = last_name_list[i].capitalize()
                last_name = last_name + ' ' + last_name_list[i]
            last_name = last_name.strip()
            
        # If the actor does not have a last name,
        # Then first name is the name.
        else:
            last_name = ''
            first_name = raw_name
            
        # Exclude the Roman numerals like '(I)' following after the first name.
        if '(' in first_name:
            first_name = first_name[:first_name.find('(')].strip()
        first_name_list = first_name.split()
        
        # In case the actor's first name has two words or more,
        # Have each word in first_name capitalized by using for loop.
        first_name = ''
        for i in range(len(first_name_list)):
            first_name_list[i] = first_name_list[i].capitalize()
            first_name = first_name + ' ' + first_name_list[i]
        first_name = first_name.strip()
        
        # Combine the first_name and last_name with a blank between them,
        # We get the actor's full name.
        actor = first_name+ ' ' + last_name
        actor = actor.strip()      
        
        # sliced_line is the line that has the name of actor sliced off.
        sliced_line = line[line.find('\t'):].strip()
        
        # Find the movie's name with the year it produced in sliced_line.
        # The movie's name always ends with a ')'.
        movie = sliced_line[:sliced_line.find(')')+1]
        
        if actor not in actor_dict:
            actor_dict[actor] = [movie]
        elif movie not in actor_dict[actor]:
            actor_dict[actor].append(movie)
        append_movies(actor, actor_data, actor_dict)
        
        # Move on to the next line.
        line = actor_data.readline()
    return actor_dict

def append_movies(actor, actor_data, actor_dict):
    '''According to the open reader actor_data, append the remaining movies 
    of the 'actor' to the list which is the value of the key 'actor' 
    in actor_dict.  
    '''
    
    line = actor_data.readline()
    
    # While there is still a movie, append it. 
    while line.strip() != '':
        movie = line[:line.find(')')+1].strip()
        if movie not in actor_dict[actor]:
            actor_dict[actor].append(movie)
        line = actor_data.readline()
    
    
def read_header(f):
    '''Read the header of the open reader f.
    '''
    
    line = f.readline()
    
    # Stop at the line starts with 'THE ACTORS LIST'.
    while not line.startswith('THE ACTORS LIST'):
        line=f.readline()
        
    # Stop at the line starts with '----'.
    # All lines above and including the line starts with '----' is the header.
    while not line.startswith('----'):
        line=f.readline()
        
def invert_actor_dict (actor_dict):
    '''Return a dictionary that is the inverse of actor_dict. 
    The original actor_dict maps actors (string) to lists of movies (string) 
    in which they have appeared. The returned dictionary maps movies (string) 
    to lists of actors (string) appearing in the movie.
    '''
    
    movie_dict = {}
    for actor, movies_list in actor_dict.items():
        for movie in movies_list:
            if movie not in movie_dict:
                movie_dict[movie] = [actor]
            else:
                movie_dict[movie].append(actor)
    return movie_dict

def find_connection(actor_name, actor_dict, movie_dict):
    '''Return a list of (movie, actor) tuples that represent a shortest 
    connection between "actor_name" and Kevin Bacon. If there is no connection 
    between "actor_name and Kevin Bacon or "actor_name" is Kevin Bacon, 
    the returned list is empty. "movie_dict" is the inversion of "actor_dict".
    '''
    
    path = []
    single_connections = find_links(actor_name, actor_dict, movie_dict)
    
    # If Kevin Bacon is connected to "actor_name", trace from Kevin Bacon
    # back to "actor_name" to get the shortest path.
    # Otherwise, return empty list.
    if single_connections.has_key("Kevin Bacon"):
        
        current_actor = "Kevin Bacon"
        # Keep tracing until back to "actor_name"
        while current_actor != actor_name:
            link = single_connections[current_actor]
            previous_actor = link[0]
            movie_shared = link[1]
            
            # Update "path" when "previous_actor" of "current_actor" is found
            # in the shortest path from "actor_name" to Kevin Bacon
            path.insert(0, (movie_shared, current_actor))
            current_actor = previous_actor
            
    return path

def find_links(actor_name, actor_dict, movie_dict):
    '''Apply breadth-first search using "actor_dict" and "movie_dict". Start 
    from "actor_name" until Kevin Bacon is found.
       Return dict "single-connections" that maps each "enountered-actor" 
    during the search to tuple (link-actor, movie). The "link-actor" is in
    "movie" with "encountered-actor" and comes before "encountered-actor" in
    the first found shortest path from "actor_name" to "encountered-actor".
    '''
    
    if not actor_dict.has_key(actor_name):
        return {}
    
    single_connections = {actor_name: (None, None)}
    
    # A list of actors who we have looked through their movies and co-stars
    investigated = []
    
    # A list of actors who we encounter but not yet investigated
    to_investigate = [actor_name]
    
    # If "actor_name" is Kevin Bacon, return empty dict.
    # Otherwise, investigate one actor at a time unless we find Kevin Bacon 
    # or run out of actors to investigate.
    while to_investigate != [] and to_investigate[0] != "Kevin Bacon":
        
        # Investigate actors in first_come_first_served order
        investigating = to_investigate.pop(0)
        investigated.append(investigating)
                
        for movie in actor_dict[investigating]:
            for co_star in movie_dict[movie]:
                
                # If this "co_star" is encountered for the first time, the path
                # from "actor_name" to this "co_star" is the first found 
                # shortest path between them. Link him/her to the actor 
                # "investigating" by the movie they shared.
                if not (co_star in investigated or co_star in to_investigate):
                    to_investigate.append(co_star)
                    single_connections[co_star] = (investigating, movie)
                
                # If find Kevin Bacon, quit the function
                if co_star == "Kevin Bacon":
                    return single_connections
    
    # At this stage, it indicates that either "actor_name" is Kevin Bacon,
    # or actor_name and Kevin Bacon are not connected.
    return {}