class Handler:
    
    def __init__(self):
        self.storage = {}
    
    def process(self, line):
        if len(line) == 0:
            print("You must enter something.")
            return
        
        actions = line.split()
        rootCommand = actions[0]
        commandLength = len(actions)
        
        if rootCommand == 'store' and commandLength == 3:
            self.store(actions[1], actions[2])
            return True
        elif rootCommand == 'lookup' and commandLength == 2:
            self.lookup(actions[1])
            return True
        elif commandLength == 3 and (rootCommand == 'add' or rootCommand == 'subtract' or rootCommand == 'multiply' or rootCommand == 'divide' or rootCommand == 'power'):
            self.op(actions[0], actions[1], actions[2])
            return True
        elif rootCommand == 'execute' and commandLength == 2:
            self.executeFile(actions[1])
            return True
        
        return False
    
    def store(self, name, value = ''):
        if name in self.storage:
            oldValue = self.storage[name]
            self.storage[name] = value
            print("{0} has been updated from {1} to {2}.".format(name, oldValue, value))
        else:
            self.storage[name] = value
            print("{0} has been stored with the value {1}.".format(name, value))
    
    def lookup(self, name):
        if name not in self.storage:
            print("{0} does not exist.".format(name))
        else:
            print("{0} has the value {1}.".format(name, self.storage[name]))
    
    def op(self, operation, a, b):
        if not (self.isNumber(a) and self.isNumber(b)):
            print("Integers only!")
            return
        
        a = int(a)
        b = int(b)
        
        if operation == 'add':
            print("{0} + {1} = {2}".format(a, b, a+b))
        elif operation == 'subtract':
            print("{0} - {1} = {2}".format(a, b, a-b))
        elif operation == 'multiply':
            print("{0} * {1} = {2}".format(a, b, a*b))
        elif operation == 'divide':
            if b == 0:
                print("What have you done? You can't divide by 0.")
            else:
                print("{0}/{1} = {2}".format(a, b, a/b))
        elif operation == 'power':
            print("{0} ^ {1} = {2}".format(a, b, a**b))
    
    def executeFile(self, fileName):
        try:        
            with open(fileName, 'r') as commandFile:
                for command in commandFile:
                    print("Command: {0}".format(command))
                    self.process(command)
        except IOError:
            print("{0} does not exist!".format(fileName))
    
    def isNumber(self, i):
        i = str(i)
        if len(i) > 1:
            if i[:1] in ['+', '-']:
                return i[1:].isdigit()
        return i.isdigit()
        
        