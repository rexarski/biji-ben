def average_grade(grade_list):
    '''(list of [str, int] lists) -> float
    Return the average grade for all of the
    students in grade_list.'''
    
    total = 0.0
    
    # student is a [str, int] list
    for student in grade_list:
        total += student[1]
        
    return total / len(grade_list)

def get_student_IDs(grade_list):
    ''' (list of [str, int] lists) -> list of strs
    Return the student IDs from grade_list.'''
    
    ids = []
    
    # item is a [str, int] list
    for item in grade_list:
        ids = ids.append(item[0])
        print ids
    
    return ids
        