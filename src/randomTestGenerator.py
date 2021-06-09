import simpleBMI
import os
from xml.dom import minidom
import random
import string

# TODO - split reusable methods into a helper functions file

# TODO - pass through command line
file = 'simpleBMI'
cut = 'BMICalc'

# TODO - either scrape actions from file or define and document a generic format and expect the user to define the list of actions

# For each constructor, note number of parameters.
# All parameters are assumed to be integers
inits = [4]

# Actions
# Format is [name of action, type of action (assign, method), number of parameters
# All parameters are assumed to be integers
actions = [['gender', 'assign', 1], ['height', 'assign', 1], ['weight', 'assign', 1], ['age', 'assign', 1], ['calculateBMI', 'method', 2], ['classifyBMI_teensAndChildren', 'method', 0], ['classifyBMI_adults', 'method', 0]]

''' Example test case:
[
[0, [1]],
[1, [5]],
[4, [6,7]],
[6, []]
]

Each step is [ index in action list , [ parameter values] ]
'''

# Generates a constructor call
# Picks a random constructor and generates random (integer) input for that constructor
def generateConstructor():
    which_constructor = random.randint(0, len(inits) - 1)
    num_parameters = inits[which_constructor]
    parameters = []

    for parameter in range(num_parameters):
        parameters.append(random.randint(-99,999))
   
    return [-1, parameters]
   
# Generate a random action on the CUT
# Selects a random action, then generates random (integer) input for that action
def generateAction():
    which_action = random.randint(0, len(actions) - 1)
    num_parameters = actions[which_action][2]
    parameters = []

    for parameter in range(num_parameters):
        parameters.append(random.randint(-99,999))
   
    action = [which_action, parameters]

    return action

# Prints genotype representation to a file (pytest code)

def writeToFile(test_suite):
    #CREATE AND SAVE A TEST CASE PYTHON FILE
    outfile = 'test_' + file + '.py'
    f= open(outfile,"w+") #overwrites the old file with this name
    f.write('import ' + file + '\nimport pytest\n')

    for test in range(len(test_suite)):
       test_case = test_suite[test]
       f.write("\ndef test_%d():\n" % test)

       # Initialize the constructor
       parameters = test_case[0][1]
       init_string = '\tcut = ' + file + '.' + cut + '(' + str(parameters[0])
       for parameter in range(1, len(parameters)):
           init_string = init_string + ',' + str(parameters[parameter])

       init_string += ')\n'

       f.write(init_string)

       # Print each test step

       for action in range(1, len(test_case)): 
           name = actions[test_case[action][0]][0]
           parameters = test_case[action][1]
           type = actions[test_case[action][0]][1]

           out_string = ''

           if type == 'assign':
               out_string = '\tcut.' + name + ' = ' + str(parameters[0]) + '\n'
           elif type == 'method':
               if parameters != []: 
                   out_string = '\tcut.' + name + '(' + str(parameters[0]) 
                   for parameter in range(1, len(parameters)):
                       out_string = out_string + ',' + str(parameters[parameter])
                   out_string += ')\n'
               else:
                   out_string = '\tcut.' + name + '()\n' 

           f.write(out_string)
   
    f.close() #changes are only saved after closed

# Prints genotype to a file (pytest code) and measures code coverage

def getCoverage(test_suite):
    writeToFile(test_suite)
    os.system('pytest -v --cov=' + file + ' --cov-report term-missing --cov-report xml')
    xmldoc = minidom.parse('coverage.xml')
    tag = xmldoc.getElementsByTagName('coverage') 
    print (tag[0].attributes['line-rate'].value)


######### Generate a random test suite (1-20 tests), each with 1-20 actions

test_suite = []
nTestsCases = random.randint(1,20)

for i in range(nTestsCases):
    test_case = []    
    # Initialize the CUT
    test_case.append(generateConstructor()) 
    # Generate actions
    nActions = random.randint(1,20)
    for j in range(nActions):
        test_case.append(generateAction())
    test_suite.append(test_case)

# Print genotype
print(test_suite)

# Print to file and measure coverage
getCoverage(test_suite)

