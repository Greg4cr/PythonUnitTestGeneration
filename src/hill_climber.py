import subprocess
from xml.dom import minidom
import random
import string
import copy
import time
from file_utilities import *
from generation_utilities import *

##### Measures statement coverage
def getCoverage(solution):
    fitness = 0.0
    writeToFile(metadata, solution.test_suite)
    process = subprocess.Popen(['pytest', '--cov=' + metadata["file"]], stdout=subprocess.PIPE)
    stdout = str(process.communicate()[0])
    lines = stdout.split("\\n")
    for line in lines:
        # Line we want starts with TOTAL
        if "TOTAL" in line:
            words = line.split(" ")
            coverage = words[len(words)-1]
            fitness = coverage[:len(coverage)-1]

    return fitness

#ADDED A SMALL PENALTY FOR NUMBER OF TEST CASES USED. 
def calculateFitness(solution):
    #fitness = coverage percentage - a small penalty for the number of tests
    a = float(getCoverage(solution))
    b = float(len(solution.test_suite))/10
    solution.fitness = a - b

###################################################################
# Mutation functions, used in the hill climber to manipulate solutions
###################################################################

'''
Example test case:
[
[0, [1]],
[1, [5]],
[4, [6,7]],
[6, []]
]
Each step is [ index in action list , [ parameter values] ]

Actions are stored in the metadata dictionary at metadata["actions"][index]. 

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
    test_suite[testSelected].append(generateAction(metadata))
    return test_suite
    
def changeRandomParameter(test_suite):
    nTestCases = len(test_suite) - 1
    testCaseSelected = random.randint(0,nTestCases)
    nActions = len(test_suite[testCaseSelected]) - 1
    actionSelected = random.randint(0,(nActions))
    # Increment or decrement by a random amount  
    increment = random.randint(-10, 10)

    # Constructor
    if  test_suite[testCaseSelected][actionSelected][0] == -1:
        nParameters = len(test_suite[testCaseSelected][actionSelected][1]) - 1
        parameterSelected = random.randint(0,nParameters)
        value = test_suite[testCaseSelected][actionSelected][1][parameterSelected]
        parameter_data = metadata["constructor"]["parameters"][parameterSelected]
        if "min" in parameter_data.keys():
            if value + increment < parameter_data["min"]:
                increment = parameter_data["min"] - value 
        if "max" in parameter_data.keys():
            if value + increment > parameter_data["max"]:
                increment = parameter_data["max"] - value 

        test_suite[testCaseSelected][actionSelected][1][parameterSelected] += increment
    # Action
    elif "parameters" in metadata["actions"][test_suite[testCaseSelected][actionSelected][0]] and len(metadata["actions"][test_suite[testCaseSelected][actionSelected][0]]["parameters"]) > 0:
        nParameters = len(test_suite[testCaseSelected][actionSelected][1]) - 1
        parameterSelected = random.randint(0,nParameters)
        value = test_suite[testCaseSelected][actionSelected][1][parameterSelected]
        parameter_data = metadata["actions"][test_suite[testCaseSelected][actionSelected][0]]["parameters"][parameterSelected]
        if "min" in parameter_data.keys():
            if value + increment < parameter_data["min"]:
                increment = parameter_data["min"] - value 
        if "max" in parameter_data.keys():
            if value + increment > parameter_data["max"]:
                increment = parameter_data["max"] - value 

        test_suite[testCaseSelected][actionSelected][1][parameterSelected] += increment
    return test_suite

def addTestCase(test_suite):
    nActions = random.randint(0, 20)
    new_testCase = generateTestSuite(metadata,1,nActions)
    test_suite.extend(new_testCase)
    return test_suite

def removeTestCase(test_suite):
    nTestCases = len(test_suite) - 1
    if nTestCases > 1:
        testCaseSelected = random.randint(0,nTestCases)
        test_suite.remove(test_suite[testCaseSelected])
    return test_suite

def mutate(solution):
    '''
    Mutation - constrain possible actions - Pick one test case, make one change to actions in that test case:
        — Add an action
        — Delete an action
        — Change parameters of an action (limited range of values, increment or decrement integer by a random change from a Gaussian distribution)
        — Add a new test case with a constructor
        — Remove a test case
    '''

    new_solution = Solution()
    suite = copy.deepcopy(solution.test_suite)
    action = random.randint(1,5)
        
    #SHOULD WE DELETE AND ADD TEST CASES INSTEAD OF ACTIONS? -------
    
    if action == 1: #1 delete an action
        new_solution.test_suite = deleteRandomAction(suite)
    elif action == 2: #add an action
        new_solution.test_suite = addRandomAction(suite)
    elif action == 3: #change random parameter by random amount
        new_solution.test_suite = changeRandomParameter(suite)    
    elif action == 4: #add a test case
        new_solution.test_suite = addTestCase(suite)
    elif action == 5: #delete a test case
        new_solution.test_suite = removeTestCase(suite)

    return new_solution

###################################################################
#Hill Climbing, using random ascent
###################################################################

# Import metadata
metadata = parseMetadata('example/BMICalc_metadata.json')

maxTestsCases = 20
maxActions = 20

# Generate an initial solution.
# This is a random test suite (1-20 tests), each with 1-20 actions
solution_current = Solution()
solution_current.test_suite = generateTestSuite(metadata,maxTestsCases, maxActions)
calculateFitness(solution_current)

solution_best = copy.deepcopy(solution_current)

print('Initial fitness: ' + str(solution_current.fitness))

gen = 1
maxGen = 50

while gen < maxGen: 
    tries = 50
    changed = False

    for i in range(tries):
        solution_new = mutate(solution_current)
        calculateFitness(solution_new)

        if solution_new.fitness > solution_current.fitness:
            print("New fitness: " + str(solution_new.fitness))
            solution_current = copy.deepcopy(solution_new)
            changed = True
       
            if solution_new.fitness > solution_best.fitness:
                solution_best = copy.deepcopy(solution_current)

    # Reset the search if no better mutant is found within 50 attempts.
    if changed == False:
        solution_current = Solution()
        solution_current.test_suite = generateTestSuite(metadata, maxTestsCases, maxActions)
        calculateFitness(solution_current)

    # Increment generation
    gen += 1

print("Best Test Suite:")
print(solution_best.test_suite)
print("Best Fitness: " + str(solution_best.fitness))
print("Number of generations used: " + str(gen))
