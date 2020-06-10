def double_first_item(data):
    ''' (list of floats) -> NoneType
    Double the value of the first item in data.'''
    
    data[0] = data[0] * 2
    
if __name__ == '__main__':
    
    values = [34.2, 45.3, 63.2]
    double_first_item(values)
    print values