###################################################################
# Simple genetic algorithm for generating pytest-formatted Python unit tests
#
# Command-Line parameters:
# -m <metadata file location>
# -f <fitness function (choices: statement, output)>
# -g <search budget, the maximum number of generations before printing the best solution found>
# -p <population size>
# -s <tournament size, for selection>
# -t <mutation probability>
# -x <crossover probability>
# -c <maximum number of test cases in a randomly-generated test suite>
# -a <maxmium number of actions (variable assignments, method calls) in a randomly-generated test case>
###################################################################

import copy
import getopt
import random
import sys
from file_utilities import *
from generation_utilities import *
from fitness_functions import *

###################################################################
# Mutation an crossover functions, used in the genetic algorithm to manipulate solutions
###################################################################

# Delete a random action from an existing test
def deleteRandomAction(test_suite):
    suite_size = len(test_suite) - 1
    test_case_selected = random.randint(0, suite_size)

    if len(test_suite[test_case_selected]) > 1:
        num_actions = len(test_suite[test_case_selected]) - 1
        action_selected = random.randint(1, num_actions)
        test_suite[test_case_selected].remove(test_suite[test_case_selected][action_selected])

    return test_suite

# Add a random action to an existing test
def addRandomAction(test_suite):
    suite_size = len(test_suite) - 1
    test_selected = random.randint(0, suite_size)
    test_suite[test_selected].append(generateAction(metadata))
    return test_suite

# Change a parameter of an existing action
def changeRandomParameter(test_suite):

    # Select a test, action, and parameter
    suite_size = len(test_suite) - 1
    test_case_selected = random.randint(0, suite_size)
    num_actions = len(test_suite[test_case_selected]) - 1
    action_selected = random.randint(0,(num_actions))

    # Increment or decrement by a random amount  
    increment = random.randint(-10, 10)

    # If the action is a constructor call
    if test_suite[test_case_selected][action_selected][0] == -1:
        # Select the parameter to modify
        num_parameters = len(test_suite[test_case_selected][action_selected][1]) - 1
        parameter_selected = random.randint(0, num_parameters)
        parameter_data = metadata["constructor"]["parameters"][parameter_selected]

        # Get the current value of that parameter
        value = test_suite[test_case_selected][action_selected][1][parameter_selected]

        if "min" in parameter_data.keys():
            if value + increment < parameter_data["min"]:
                increment = parameter_data["min"] - value 
        if "max" in parameter_data.keys():
            if value + increment > parameter_data["max"]:
                increment = parameter_data["max"] - value 

        test_suite[test_case_selected][action_selected][1][parameter_selected] += increment

    # If the parameter is an action (assignment or method call)
    elif "parameters" in metadata["actions"][test_suite[test_case_selected][action_selected][0]] and len(metadata["actions"][test_suite[test_case_selected][action_selected][0]]["parameters"]) > 0:
        # Select the parameter to modify
        num_parameters = len(test_suite[test_case_selected][action_selected][1]) - 1
        parameter_selected = random.randint(0, num_parameters)
        parameter_data = metadata["actions"][test_suite[test_case_selected][action_selected][0]]["parameters"][parameter_selected]

        # Get the current value of that parameter
        value = test_suite[test_case_selected][action_selected][1][parameter_selected]

        if "min" in parameter_data.keys():
            if value + increment < parameter_data["min"]:
                increment = parameter_data["min"] - value 
        if "max" in parameter_data.keys():
            if value + increment > parameter_data["max"]:
                increment = parameter_data["max"] - value 

        test_suite[test_case_selected][action_selected][1][parameter_selected] += increment

    return test_suite

# Add a test case to a suite
def addTestCase(test_suite):
    num_actions = random.randint(0, max_actions)
    new_test = generateTestSuite(metadata, 1, num_actions)
    test_suite.extend(new_test)
    return test_suite

# Delete a random test case from a suite
def removeTestCase(test_suite):
    suite_size = len(test_suite) - 1

    if suite_size > 1:
        test_case_selected = random.randint(0, suite_size)
        test_suite.remove(test_suite[test_case_selected])

    return test_suite

def mutate(solution):
    '''
    When we mutate a solution, we make one small change to it. That change can include:
        — Add an action to a test case
        — Delete an action from a test case
        — Change parameters of an action (limited range of values, increment value by [-10, +10])
        — Add a new test case to the suite
        — Remove a test case from the suite
    '''

    new_solution = Solution()
    suite = copy.deepcopy(solution.test_suite)
    action = random.randint(1,5)
    
    if action == 1: # delete an action
        new_solution.test_suite = deleteRandomAction(suite)
    elif action == 2: # add an action
        new_solution.test_suite = addRandomAction(suite)
    elif action == 3: # change random parameter 
        new_solution.test_suite = changeRandomParameter(suite)    
    elif action == 4: # add a test case
        new_solution.test_suite = addTestCase(suite)
    elif action == 5: # delete a test case
        new_solution.test_suite = removeTestCase(suite)

    calculateFitness(metadata, fitness_function, new_solution)

    return new_solution

# Creates an initial population of test suites.
def createPopulation(size):
    population = []

    for i in range(size):
        new_solution = Solution()
        new_solution.test_suite = generateTestSuite(metadata, max_test_cases, max_actions)
        calculateFitness(metadata, fitness_function, new_solution)
        population.append(new_solution)

    return population

# Selects a random proportion of the population and identifies the best solution in that sample (selection)
def selection(population, tournament_size):
    if not tournament_size > 1:
        raise Exception("Variable tournament_size must be greater than 1.")

    competition = random.sample(population, tournament_size)
    solution_best = copy.deepcopy(competition[0])

    for i in range(1, (tournament_size-1)):
        if competition[i].fitness > solution_best.fitness:
            solution_best = copy.deepcopy(competition[i])

    # Return a copy of the best solution
    return solution_best

# Creates new "child" test suites by swapping test cases between the parents
# TODO: This is a very simple single point crossover. An alternative would be to potentially swap at each test case. This could be better, so think about it.
# TODO: We could also perform a more complex crossover where we swap actions as well. We should think about whether that makes sense. For now, I think what we have is OK.
def crossover(parent1, parent2):

    if len(parent1.test_suite) > len(parent2.test_suite):
        pos = random.randint(1, len(parent2.test_suite))
    else:
        pos = random.randint(1, len(parent1.test_suite))

    offspring1 = Solution()
    offspring2 = Solution()
    offspring1.test_suite = parent1.test_suite[:pos] + parent2.test_suite[pos:]
    offspring2.test_suite = parent2.test_suite[:pos] + parent1.test_suite[pos:]
    calculateFitness(metadata, fitness_function, offspring1)
    calculateFitness(metadata, fitness_function, offspring2)

    return (offspring1, offspring2)

###################################################################
#Genetic Algorithm
###################################################################

# Default parameters

# Location of the metadata on the CUT
metadata_location = "example/BMICalc_metadata.json" 

# Fitness function
fitness_function = "statement" 

# Maximum number of test cases in a generated suite
max_test_cases = 20 

# Maximum number of actions in a generated test case
max_actions = 20

# Maximum number of generations
max_gen = 200

# Population size
population_size = 20

# Mutation probability
mutation_probability = 0.7

# Crossover probability
crossover_probability = 0.7

# Tournament size
tournament_size = 6

# Get command-line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],"hm:f:c:a:g:t:p:x:s:")
except getopt.GetoptError:
        print("genetic_algorithm.py -m <metadata file location> -f <fitness function> -c <maximum number of test cases> -a <maximum number of actions> -g <maximum number of generations> -p <population size> -t <mutation probability> -x <crossover probability> -s <tournament size>")
        sys.exit(2)
													  		
for opt, arg in opts:
    if opt == "-h":
        print("genetic_algorithm.py -m <metadata file location> -f <fitness function> -c <maximum number of test cases> -a <maximum number of actions> -g <maximum number of generations> -p <population size> -t <mutation probability> -x <crossover probability> -s <tournament size>")
        sys.exit()
    elif opt == "-m":
        metadata_location = arg
    elif opt == "-f":
        fitness_function = arg
    elif opt == "-c":
        max_test_cases = int(arg)

        if max_test_cases < 1:
            raise Exception("max_test_cases cannot be < 1.")
    elif opt == "-a":
        max_actions = int(arg)

        if max_actions < 1:
            raise Exception("max_actions cannot be < 1.")
    elif opt == "-g":
        max_gen = int(arg)

        if max_gen < 1:
            raise Exception("max_gen cannot be < 1.")
    elif opt == "-t":
        mutation_probability = float(arg)

        if mutation_probability < 0.0 or mutation_probability > 1.0:
            raise Exception("mutation_probability must be between 0 and 1.")
    elif opt == "-x":
        crossover_probability = float(arg)

        if crossover_probability < 0.0 or crossover_probability > 1.0:
            raise Exception("crossover_probability must be between 0 and 1.")
    elif opt == "-p":
        population_size = int(arg)

        if population_size < 3:
            raise Exception("population_size cannot be < 3.")
    elif opt == "-s":
        tournament_size = int(arg)

        if tournament_size < 3:
            raise Exception("tournament_size cannot be < 3.")


# Import metadata
metadata = parseMetadata(metadata_location)

#create initial population
population = createPopulation(population_size)

#Initialize best solution
solution_best = copy.deepcopy(population[0])

# Continue to evolve until the generation budget is exhausted.
gen = 1

while gen <= max_gen:
    new_population = []

    while len(new_population) < len(population):
        # Selection
        offspring1 = selection(population, tournament_size)
        offspring2 = selection(population, tournament_size)

        # Crossover
        if random.random() < crossover_probability:
            (offspring1, offspring2) = crossover(offspring1, offspring2)

        # Mutation
        if random.random() < mutation_probability:
            offspring1 = mutate(offspring1)
        if random.random() < mutation_probability:
            offspring2 = mutate(offspring2)

        new_population.append(offspring1)
        new_population.append(offspring2)

        # Store best
        if offspring1.fitness > solution_best.fitness:
            solution_best = copy.deepcopy(offspring1)
        if offspring2.fitness > solution_best.fitness:
            solution_best = copy.deepcopy(offspring2)

    # Set the new population as the current population.
    population = new_population

    print("Best fitness at generation %d: %.8f" % (gen, solution_best.fitness))

    # Increment Generation
    gen += 1

# Print the best test suite to a file
writeToFile(metadata, solution_best.test_suite)
