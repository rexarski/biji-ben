import bacon_functions

actor_data = open("large_actor_data.txt")
actor_dict = bacon_functions.parse_actor_data(actor_data)
movie_dict = bacon_functions.invert_actor_dict(actor_dict)
print bacon_functions.find_connection("Roy Rodgers", actor_dict, movie_dict)

print actor_data.readline()