import os
from xml.dom import minidom
import random
import string
import copy
import time
from file_utilities import *
from generation_utilities import *

##### Prints genotype to a file (pytest code) and measures code coverage
#TODO: GET COVERAGE VALUE FROM SCRIPT INSTEAD OF A XML FILE ---- Some times this process bugs when in a loop.
#temporary workaround: Delay between creating and reading the XML file
def getCoverage(solution):
    writeToFile(metadata, solution.test_suite)
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
def calculateFitness(solution):
    #fitness = coverage percentage - a small penalty for the number of tests
    a = float(getCoverage(solution))
    b = float(len(solution.test_suite))/10
    solution.fitness = a*100 - b

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
    
def changeRandomParameter(test_suite, increment):
    nTestCases = len(test_suite) - 1
    testCaseSelected = random.randint(0,nTestCases)
    nActions = len(test_suite[testCaseSelected]) - 1
    actionSelected = random.randint(0,(nActions))

    # Constructor
    if  test_suite[testCaseSelected][actionSelected][0] == -1:
        nParameters = len(test_suite[testCaseSelected][actionSelected][1]) - 1
        parmeterSelected = random.randint(0,nParameters)
        test_suite[testCaseSelected][actionSelected][1][parmeterSelected] = test_suite[testCaseSelected][actionSelected][1][parmeterSelected] + increment
    # Action
    elif "parameters" in metadata["actions"][test_suite[testCaseSelected][actionSelected][0]] and len(metadata["actions"][test_suite[testCaseSelected][actionSelected][0]]["parameters"]) > 0:
        nParameters = len(test_suite[testCaseSelected][actionSelected][1]) - 1
        parmeterSelected = random.randint(0,nParameters)
        test_suite[testCaseSelected][actionSelected][1][parmeterSelected] = test_suite[testCaseSelected][actionSelected][1][parmeterSelected] + increment
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
        — Change parameters of an action (limited range of values, increment or decrement integer a fixed amount)
        — Add a new test case with a constructor
        — Remove a test case
    '''

    new_solution = Solution()
    suite = copy.deepcopy(solution.test_suite)
    action = random.randint(1,6)
        
    #SHOULD WE DELETE AND ADD TEST CASES INSTEAD OF ACTIONS? -------
    
    if action == 1: #1 delete an action
        new_solution.test_suite = deleteRandomAction(suite)
    elif action == 2: #add an action
        new_solution.test_suite = addRandomAction(suite)
    elif action == 3: #change random parameter - increment by 1
        new_solution.test_suite = changeRandomParameter(suite, 1)    
    elif action == 4: #change random parameter - decrement by 1
        new_solution.test_suite = changeRandomParameter(suite, -1)
    elif action == 5: #add a test case
        new_solution.test_suite = addTestCase(suite)
    elif action == 6: #delete a test case
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
solution_soft = copy.deepcopy(solution_current)

print('Initial fitness: ' + str(solution_current.fitness))

gen = 1
maxGen = 2
nSoftResets = 0

while (gen < maxGen): 
    tries = 30
    changed = False
    #SHOULD WE KEEP MUTATING THE MUTATED VERSION INSTEAD OF THE BEST? --------------------
    for i in range(tries):
        solution_new = mutate(solution_current)
        calculateFitness(solution_new)
        print(solution_new.fitness)
        solution_current = copy.deepcopy(solution_new)
        
        if solution_new.fitness > solution_best.fitness:
            changed = True
            solution_best = copy.deepcopy(solution_current)
            fitness_best = solution_new.fitness
    
    #Because we keep mutating the mutated version, solution_current might get to an irreversible state. I thought of a way to make a "soft" and a "hard" reset. 
    if not changed:
        if nSoftResets < 10:
            #get solution_current to what it was before mutating
            solution_current = copy.deepcopy(solution_soft)
            nSoftResets = nSoftResets + 1
        else:
            #if 3 soft resets doesn't work, time to generate a completely new solution_current
            maxTestsCases = 20
            maxActions = 20
            solution_current = Solution()
            solution_current.test_suite = generateTestSuite(metadata, maxTestsCases, maxActions)
            solution_soft = copy.deepcopy(solution_current)
            nSoftResets = 0

    # Increment generation
    gen += 1

print("Best Test Suite:")
print(solution_best.test_suite)
print("Best Fitness: " + str(solution_best.fitness))
print("Number of generations used: " + str(gen))
