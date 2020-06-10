from Event import Event

class Day(object):
    '''A calendar day.'''
    
    def __init__(self, when):
        '''Create a new Day object with date when.'''

        self.date = when
        self.events = []
        
    def __str__(self):
        '''(Day) -> str
        Return a description of self.'''
        
        description = "Date: %s" % (self.date)
        for item in self.events:
            description += '\n%s' % (item)
        return description 

    # EXERCISE: update this method so that event e is only added to the list
    # if it does not overlap with any other events schedule for this day.
    def schedule_event(self, e):
        '''(Day, Event) -> NoneType
        Add event e to the schedule.'''
        
        self.events.append(e)
        
if __name__ == '__main__':
    
    e1 = Event(10, 11, 'csc108', 'Mar 30')
    today = Day('Mar 30 2012')
    today.schedule_event(e1)
    print today
        