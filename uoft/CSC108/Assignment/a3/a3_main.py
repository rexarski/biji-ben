from a3_functions import *

if __name__ == '__main__':

    # During testing, we may change the values of these variables.
    friendships = {}
    networks = {}
    profiles_file = open('profiles.txt')

    # Add your code here.

    load_profiles(profiles_file, friendships, networks)
    persons = friendships.keys()
    name = raw_input("Please enter a person (or press return to exit): ")
    while name != '':
        if name not in persons:
            print "There are no recommendations for this person. \n"
        else:
            recommendations = sort_recommendations(make_recommendations(name, \
            friendships, networks))
            if recommendations != []:
                for i in recommendations:
                    print i
                print ""
            else:
                print "There are no recommendations for this person. \n"
        name = raw_input("Please enter a person (or press return to exit): ")
    print "Thank you for using the recommendation system!"
