import simpleBMI
import os
from xml.dom import minidom
import random
import string
from utilities import *

###### Import metadata

metadata = parseMetadata('BMICalc_metadata.json')

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

#TODO: Get global variables in each function (so they could work from a helper file)

# Generates a constructor call
# Picks a random constructor and generates random (integer) input for that constructor
def generateConstructor():
    which_constructor = random.randint(0, len(metadata["constructors"]) - 1)
    parameter_data = metadata["constructors"][which_constructor]["parameters"]

    parameters = []

    for parameter in range(len(parameter_data)):
        if "min" in parameter_data[parameter]:
            min = parameter_data[parameter]["min"]
        else:
            min = -999

        if "max" in parameter_data[parameter]:
            max = parameter_data[parameter]["max"]
        else:
            max = 999

        parameters.append(random.randint(min, max))
   
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
    outfile = 'test_' + metadata["file"] + '.py'
    f= open(outfile,"w+") #overwrites the old file with this name
    f.write('import ' + metadata["file"] + '\nimport pytest\n')

    for test in range(len(test_suite)):
        test_case = test_suite[test]
        f.write("\ndef test_%d():\n" % test)

        # Initialize the constructor
        parameters = test_case[0][1]
        init_string = '\tcut = ' + metadata["file"] + '.' + metadata["class"] + '(' + str(parameters[0])
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
   
    f.close() 



##### Prints genotype to a file (pytest code) and measures code coverage
#TODO: GET COVERAGE VALUE FROM SCRIPT INSTEAD OF A XML FILE ---- Some times this process bugs when in a loop.
#temporary workaround: Delay between creating and reading the XML file
import time
def getCoverage(test_suite):
    writeToFile(test_suite)
    os.system('pytest --cov=' + metadata["file"] + ' --cov-report term-missing --cov-report xml')
    #time.sleep(0.05*len(test_suite))
    try:
        xmldoc = minidom.parse('coverage.xml')
        tag = xmldoc.getElementsByTagName('coverage')
    except:
        time.sleep(0.05*len(test_suite))
        try:
            xmldoc = minidom.parse('coverage.xml')
            tag = xmldoc.getElementsByTagName('coverage')
        except:
            time.sleep(0.2)
            xmldoc = minidom.parse('coverage.xml')
            tag = xmldoc.getElementsByTagName('coverage')
    return (tag[0].attributes['line-rate'].value)


#ADDED A SMALL PENALTY FOR NUMBER OF TEST CASES USED. 
def fitness(test_suite):
    #fitness = coverage percentage - a small penalty for the number of tests
    a =  float(getCoverage(test_suite))
    b = float(len(test_suite))/10
    return a*100 - b


#SHOULD EVERY TASE CASE HAVE THE SAME AMMOUNT OF ACTIONS? --------------------
def generateTestSuite(maxTestsCases, maxActions):
    nTestsCases = random.randint(1,maxTestsCases)
    test_suite = []
    for i in range(nTestsCases):
        test_case = []    
        # Initialize the CUT
        test_case.append(generateConstructor()) 
        # Generate actions
        nActions = random.randint(0,maxActions)
        for j in range(nActions):
            test_case.append(generateAction())
        test_suite.append(test_case)    
    return test_suite



'''
Action library:
actions = [['gender', 'assign', 1], ['height', 'assign', 1], ['weight', 'assign', 1], ['age', 'assign', 1], ['calculateBMI', 'method', 2], ['classifyBMI_teensAndChildren', 'method', 0], ['classifyBMI_adults', 'method', 0]]

Example test case:
[
[0, [1]],
[1, [5]],
[4, [6,7]],
[6, []]
]
Each step is [ index in action list , [ parameter values] ]

Example test suite:
[[[-1, [642, 626, 53, -38]], [1, [612]], [4, [958, 46]]], [[-1, [257, 679, 337, 821]], [1, [74]], [0, [24]]], [[-1, [161, 409, 468, 675]], [1, [173]], [3, [926]]], [[-1, [870, -82, 949, 676]], [6, []], [4, [632, -88]]], [[-1, [235, 392, 366, 929]], [6, []], [6, []]], [[-1, [809, 508, 353, 706]], [6, []], [2, [72]]], [[-1, [276, 328, 691, -63]], [1, [538]], [3, [625]]], [[-1, [654, 69, 549, -1]], [3, [40]], [3, [741]]], [[-1, [147, 678, 485, 535]], [3, [321]], [6, []]], [[-1, [325, 291, 940, 169]], [6, []], [3, [484]]], [[-1, [745, 278, 232, 909]], [5, []], [0, [403]]], [[-1, [162, 993, 315, 186]], [4, [26, 980]], [1, [498]]], [[-1, [-95, 493, 68, 655]], [4, [881, 146]], [1, [295]]]]
'''

def deleteRandomAction(test_suite):
    nTestCases = len(test_suite) - 1
    testCaseSelected = random.randint(0,nTestCases)
    if len(test_suite[testCaseSelected]) > 1:
        nActions = len(test_suite[testCaseSelected]) - 1
        actionSelected = random.randint(1,(nActions))
        test_suite[testCaseSelected].remove(test_suite[testCaseSelected][actionSelected])
    return test_suite

def addRandomAction(test_suite):
    nTestCases = len(test_suite) - 1
    testSelected = random.randint(0,nTestCases)
    #print(testSelected)
    test_suite[testSelected].append(generateAction())
    return test_suite
    
def changeRandomParameter(test_suite, increment):
    nTestCases = len(test_suite) - 1
    testCaseSelected = random.randint(0,nTestCases)
    #print("test selected = %d" % testCaseSelected)
    nActions = len(test_suite[testCaseSelected]) - 1
    actionSelected = random.randint(0,(nActions))
    #print("actionSelected = %d" % actionSelected)
    #print(test_suite[testCaseSelected][actionSelected])

    if  test_suite[testCaseSelected][actionSelected][0] == -1:
        nParameters = len(test_suite[testCaseSelected][actionSelected][1]) - 1
        #print("nParameters = %d" % nParameters)
        parmeterSelected = random.randint(0,nParameters)
        #print("parmeterSelected = %d" % parmeterSelected)
        #print(test_suite[testCaseSelected][actionSelected][1][parmeterSelected])
        test_suite[testCaseSelected][actionSelected][1][parmeterSelected] = test_suite[testCaseSelected][actionSelected][1][parmeterSelected] + increment
    elif actions[test_suite[testCaseSelected][actionSelected][0]][2] > 0:
        nParameters = len(test_suite[testCaseSelected][actionSelected][1]) - 1
        parmeterSelected = random.randint(0,nParameters)
        #print(parmeterSelected)
        #print(test_suite[testCaseSelected][actionSelected][1][parmeterSelected])
        test_suite[testCaseSelected][actionSelected][1][parmeterSelected] = test_suite[testCaseSelected][actionSelected][1][parmeterSelected] + increment
    return test_suite

def addTestCase(test_suite):
    nActions = random.randint(0, 20)
    new_testCase = generateTestSuite(1,nActions)
    test_suite.extend(new_testCase)
    return test_suite

def removeTestCase(test_suite):
    nTestCases = len(test_suite) - 1
    if nTestCases > 1:
        testCaseSelected = random.randint(0,nTestCases)
        test_suite.remove(test_suite[testCaseSelected])
    return test_suite

def mutate(test_suite, action):
    '''
    Mutation - constrain possible actions - Pick one test case, make one change to actions in that test case:
        — Add an action
        — Delete an action
        — Change parameters of an action (limited range of values, increment or decrement integer a fixed amount)
        — Add a new test case with a constructor
        — Remove a test case
    '''
    
    try:
        assert action > 0 and action < 7
    except:
        raise RuntimeError('Function mutate receives two parameters. mutate(test_suite, action). Where action must be an integer from 1 to 6.')
        
    #SHOULD WE DELETE AND ADD TEST CASES INSTEAD OF ACTIONS? -------
    
    if action == 1: #1 delete an action
        test_suite = deleteRandomAction(test_suite)
    elif action == 2: #add an action
        test_suite = addRandomAction(test_suite)
    elif action == 3: #change random parameter - increment by 1
        test_suite = changeRandomParameter(test_suite, 1)    
    elif action == 4: #change random parameter - decrement by 1
        test_suite = changeRandomParameter(test_suite, -1)
    elif action == 5: #add a test case
        test_suite = addTestCase(test_suite)
    elif action == 6: #delete a test case
        test_suite = removeTestCase(test_suite)
    return test_suite


#Hill Climbing, using random ascent

maxTestsCases = 20
maxActions = 20

# Generate an initial solution.
# This is a random test suite (1-20 tests), each with 1-20 actions

solution_current = generateTestSuite(maxTestsCases, maxActions)
fitness_current = fitness(solution_current)
solution_best = solution_current
fitness_best = fitness_current
solution_soft = solution_current

print('Initial fitness: ' + str(fitness_current))

gen = 1
maxGen = 0
nSoftResets = 0

while (gen < maxGen):
    
    fitness_new = fitness_current
    tries = 30
    changed = False
    #SHOULD WE KEEP MUTATING THE MUTATED VERSION INSTEAD OF THE BEST? --------------------
    for i in range(tries):
        action = random.randint(1,6)
        solution_new = mutate(solution_current, action)
        fitness_new = fitness(solution_new)
        print(fitness_new)
        solution_current = solution_new
        
        if fitness_new > fitness_best:
            changed = True
            solution_best = solution_current
            fitness_best = fitness_new
    
    #Because we keep mutating the mutated version, solution_current might get to an irreversible state. I thought of a way to make a "soft" and a "hard" reset. 
    if not changed:
        if nSoftResets < 10:
            #get solution_current to what it was before mutating
            solution_current = solution_soft
            nSoftResets = nSoftResets + 1
        else:
            #if 3 soft resets doesn't work, time to generate a completely new solution_current
            maxTestsCases = 20
            maxActions = 20
            newTestSuite = generateTestSuite(maxTestsCases, maxActions)
            solution_current = newTestSuite
            solution_soft = solution_current
            nSoftResets = 0

    # Increment generation
    gen += 1

print("Best Test Suite: %d" %solution_best)
print("Best Fitness: %d" %fitness_best)
print("Number of generations used: %d" %gen)        
