import bacon_functions

if __name__ == "__main__":
    actor_data = open("large_actor_data.txt")
    actor_dict = bacon_functions.parse_actor_data(actor_data)
    movie_dict = bacon_functions.invert_actor_dict(actor_dict)
    
    name_input = " "
    largest = 0
    
    while name_input != "":
        ask = "Please enter an actor (or press return to exit): "
        name = raw_input(ask)
        
        if name != "":
            name = name.title().strip()
        
            path = bacon_functions.find_connection(name, actor_dict, movie_dict)
            
            if len(path) != 0:
                bacon_num = len(path)
                if bacon_num > largest:
                    largest = bacon_num
            elif name == "Kevin Bacon":
                bacon_num = 0
            else:
                bacon_num = "Infinity"
                
            print name, "has a Bacon Number of", str(bacon_num) + "."
        
            for i in range(0, bacon_num):
                if i == 0:
                    previous_actor = name_input
                    current_actor = path[i][1]
                else:
                    previous_actor = path[i - 1][1]
                    current_actor = path[i][1]
            
                    movie_shared = path[i][0]
                    print previous_actor, "was in", movie_shared, "with", \
                          current_actor + "."
                    
        else:
            e = 'Thank you for playing! The largest Bacon Number you found was '
            print e + largest + "."
            
        print ""