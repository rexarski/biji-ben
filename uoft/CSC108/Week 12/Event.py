class Event(object):
    '''A calendar event.'''
    
    # This is called a "constructor" and it overrides the
    # default version of __init__.  It is called automatically
    # any time we construct a new Event object.
    def __init__(self, start, end, name, date):
        '''A new calendar event.'''
        
        self.start_time = start
        self.end_time = end
        self.description = name
        self.date = date
    
    # This overrides the default version of __str__ and is called automatically
    # anytime we use an Event object where a string is needed (e.g., print).
    def __str__(self):
        '''(Event) -> str'''
        
        return "From %s to %s do this: %s on this date %s." % (self.start_time, self.end_time, self.description, self.date)
    
    # This is used by the comparison operators: >, <, ==, ...
    def __cmp__(self, other):
        '''(Event, Event) -> int
        Return -1 self is less than other,
        0 if they are equal, and
        +1 if self is greater than other.'''
        
        if self.description < other.description:
            return -1
        elif self.description == other.description:
            return 0
        else:
            return +1

    # EXERCISE: add an new method called make_all_day that has no parameters (besides self).  
    # It sets the start and end times to 9 and 5.

    # EXERCISE: add a new method called overlap that co
    
    def rename(self, new_name):
        '''(Event, str) -> NoneType
        Change the name of this event to new_name.'''
        
        self.description = new_name
        
    def duration(self):
        '''(Event) -> int
        Return the duration of this event.'''
        
        return self.end_time - self.start_time