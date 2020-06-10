class Building:
    def __init__(self, address, rooms):
        """(Building, str, list of Room) -> NoneType """
        self.address = address
        self.rooms = rooms
        
    def __str__(self):
        """(Building) -> str"""
        sum = 0
        for room in self.rooms:
            sum += room.size
        return str(sum)
    
    def add_room(self, room):
        """(Building, Room) -> NoneType"""
        self.rooms.append(room)
    
class Room:
    def __init__(self, name, size):
        """(Room, str, float) -> NoneType"""
        self.name = name
        self.size = size
        
class House(Building):
    def __init__(self, address, rooms):
        if len(rooms) > 10:
            raise TooManyRoomsError
        else:
            self.address = address
            self.rooms = rooms
            
    def __str__(self):
        s = 'Welcome to our house\n'
        for room in self.roos:
            s += room.name + ' ' + str(room.size) + '\n'
        return s