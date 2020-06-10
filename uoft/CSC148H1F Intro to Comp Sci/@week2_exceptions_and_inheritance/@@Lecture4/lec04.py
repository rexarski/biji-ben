class Building:
    def __init__(self, address, rooms):
        """ (Building, str, list of Room) -> NoneType """
        self.address = address
        self.rooms = rooms
        self.occupancy = 0

    def __str__(self):
        """ (Building) -> str """
        sum = 0
        for room in self.rooms:
            sum += room.size
        return str(sum)

    def add_room(self, room):
        """ (Building, Room) -> NoneType """
        self.rooms.append(room)
    
    def rent_room(self, person, room):
        # rent out the room
        print('Welcome, ' + person)

class Room:
    def __init__(self, name, size):
        """ (Room, str, float) -> NoneType """
        self.name = name
        self.size = size
    
class House:
    # House is a subclass of Building
    # Building is a superclass of House
    #def __init__(self, address, rooms):
    #    self.address = address
    #    if len(rooms) > 10:
    #        raise Exception
    #    else:
    #        self.rooms = rooms
    def __init__(self, address, rooms, family):
        Building._init__(self, address, rooms)
        # Now House has all of the attributes from its superclass
        self.occupancy = 10
        # Can we change the attribute of superclass by
        # changing the subclass.
        # actually this does change it, because there is only one attribute, it
        # is the same attribute but said in two different places.
        self.family = family
    
    # Overriding a method
    def rent_room(self, person, room):
        if person == 'michael':
            print('Okay!')
        else:
            print('Get out!')
        # now if we rent room to michael, either from house or from building would be ok;
        # however, if we rent room to david, works from building, but rejected from house.
        # The execution order is: House -> Building.
        
        
        