###################################################################
# Simple genetic algorithm for generating pytest-formatted Python unit tests
#
# Command-Line parameters:
# -m <metadata file location>
# -g <search budget, the maximum number of generations before printing the best solution found>
# -p <population size>
# -s <tournament size, for selection>
# -t <mutation probability>
# -x <crossover probability>
# -o <crossover operator (choices: single, uniform)>
# -e <number of generations before search terminates due to lack of improvement>
# -c <maximum number of test cases in a randomly-generated test suite>
# -a <maxmium number of actions (variable assignments, method calls) in a randomly-generated test case>
# -z <test suite size penalty>
# -l <test length penalty>
###################################################################

import copy
import getopt
import random
import sys
from file_utilities import *
from generation_utilities import *
from fitness_functions import *

###################################################################
# Mutation and crossover functions, used in the genetic algorithm to manipulate solutions
###################################################################

# Delete a random action from an existing test
def delete_random_action(test_suite):
    suite_size = len(test_suite) - 1
    test_case_selected = random.randint(0, suite_size)

    if len(test_suite[test_case_selected]) > 1:
        num_actions = len(test_suite[test_case_selected]) - 1
        action_selected = random.randint(1, num_actions)
        test_suite[test_case_selected].remove(test_suite[test_case_selected][action_selected])

    return test_suite

# Add a random action to an existing test
def add_random_action(test_suite):
    suite_size = len(test_suite) - 1
    test_selected = random.randint(0, suite_size)
    test_suite[test_selected].append(generate_action(metadata))
    return test_suite

# Change a parameter of an existing action
def change_random_parameter(test_suite):

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
def add_test_case(test_suite):
    num_actions = random.randint(0, max_actions)
    new_test = generate_test_suite(metadata, 1, num_actions)
    test_suite.extend(new_test)
    return test_suite

# Delete a random test case from a suite
def remove_test_case(test_suite):
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
        new_solution.test_suite = delete_random_action(suite)
    elif action == 2: # add an action
        new_solution.test_suite = add_random_action(suite)
    elif action == 3: # change random parameter 
        new_solution.test_suite = change_random_parameter(suite)    
    elif action == 4: # add a test case
        new_solution.test_suite = add_test_case(suite)
    elif action == 5: # delete a test case
        new_solution.test_suite = remove_test_case(suite)

    calculate_fitness(metadata, fitness_function, num_tests_penalty, length_test_penalty, new_solution)

    return new_solution

# Creates an initial population of test suites.
def create_population(size):
    population = []

    for i in range(size):
        new_solution = Solution()
        new_solution.test_suite = generate_test_suite(metadata, max_test_cases, max_actions)
        calculate_fitness(metadata, fitness_function, num_tests_penalty, length_test_penalty, new_solution)
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
# Single-point crossover (pick an index and swap between parents at that index.
def crossover(parent1, parent2):

    if len(parent1.test_suite) > len(parent2.test_suite):
        pos = random.randint(1, len(parent2.test_suite))
    else:
        pos = random.randint(1, len(parent1.test_suite))

    offspring1 = Solution()
    offspring2 = Solution()
    offspring1.test_suite = parent1.test_suite[:pos] + parent2.test_suite[pos:]
    offspring2.test_suite = parent2.test_suite[:pos] + parent1.test_suite[pos:]
    calculate_fitness(metadata, fitness_function, num_tests_penalty, length_test_penalty, offspring1)
    calculate_fitness(metadata, fitness_function, num_tests_penalty, length_test_penalty, offspring2)

    return (offspring1, offspring2)

# Creates new "child" test suites by swapping test cases between the parents
# Uniform crossover (Choose a parent source at each test case)
def uniform_crossover(parent1, parent2):

    # Get maximum index where both have test cases
    if len(parent1.test_suite) > len(parent2.test_suite):
        stop = len(parent2.test_suite)
        leftovers = parent1.test_suite[len(parent2.test_suite):]
    else:
        stop = len(parent1.test_suite)
        leftovers = parent2.test_suite[len(parent1.test_suite):]

    offspring1 = Solution()
    offspring2 = Solution()

    # For each test
    for test in range(stop):
        # Flip a coin
        choice = random.randint(1, 2)
        # Option 1: Offspring 1 gets test from Parent 1, Offspring 2 gets test from Parent 2
        if choice == 1:
            offspring1.test_suite.append(parent1.test_suite[test])
            offspring2.test_suite.append(parent2.test_suite[test])
        # Option 2: Offspring 1 gets test from Parent 2, Offspring 2 gets test from Parent 1
        else:
            offspring1.test_suite.append(parent2.test_suite[test])
            offspring2.test_suite.append(parent1.test_suite[test])
   
    # Divide leftover tests between children
    mid = int(len(leftovers)/2)

    offspring1.test_suite = offspring1.test_suite + leftovers[:mid]
    offspring2.test_suite = offspring2.test_suite + leftovers[mid:]

    calculate_fitness(metadata, fitness_function, num_tests_penalty, length_test_penalty, offspring1)
    calculate_fitness(metadata, fitness_function, num_tests_penalty, length_test_penalty, offspring2)

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

# Crossover operator
crossover_operator = "uniform"

# Tournament size
tournament_size = 6

# Exhaustion (number of generations before GA terminates due to lack of improvement)
exhaustion = 30

# Test suite size penalty
num_tests_penalty = 10

# Test length penalty
length_test_penalty = 30

# Get command-line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],"hm:c:a:g:t:p:x:s:e:o:z:l:")
except getopt.GetoptError:
        print("genetic_algorithm.py -m <metadata file location> -c <maximum number of test cases> -a <maximum number of actions> -g <maximum number of generations> -p <population size> -t <mutation probability> -x <crossover probability> -s <tournament size> -e <max generations before exhaustion> -o <crossover operator> -z <test suite size penalty> -l <test length penalty>")
        sys.exit(2)
													  		
for opt, arg in opts:
    if opt == "-h":
        print("genetic_algorithm.py -m <metadata file location> -c <maximum number of test cases> -a <maximum number of actions> -g <maximum number of generations> -p <population size> -t <mutation probability> -x <crossover probability> -s <tournament size> -e <max generations before exhaustion> -o <crossover operator> -z <test suite size penalty> -l <test length penalty>")
        sys.exit()
    elif opt == "-m":
        metadata_location = arg
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
    elif opt == "-e":
        exhaustion = int(arg)

        if exhaustion < 1:
            raise Exception("exhaustion cannot be < 1.")
    elif opt == "-o":
        crossover_operator = arg
 
        if crossover_operator != "single" and crossover_operator != "uniform":
            raise Exception("Crossover operator should be either 'single' or 'uniform'")
    elif opt == "-z":
        num_tests_penalty = int(arg)

        if num_tests_penalty < 1:
            raise Exception("num_tests_penalty cannot be < 1.")
    elif opt == "-l":
        length_test_penalty = int(arg)

        if length_test_penalty < 1:
            raise Exception("length_test_penalty cannot be < 1.")


# Import metadata.
metadata = parse_metadata(metadata_location)

# Create initial population.
population = create_population(population_size)

# Initialize best solution as the first member of that population.
solution_best = copy.deepcopy(population[0])

# Continue to evolve until the generation budget is exhausted.
# Stop if no improvement has been seen in some time (stagnation).
gen = 1
stagnation = -1

while gen <= max_gen and stagnation <= exhaustion:
    # Form a new population.
    new_population = []

    while len(new_population) < len(population):
        # Choose a subset of the population and identify the best solution in that subset (selection).
        offspring1 = selection(population, tournament_size)
        offspring2 = selection(population, tournament_size)

        # Create new children by breeding elements of the best solutions (crossover)
        if random.random() < crossover_probability:
            if crossover_operator == "single":
                (offspring1, offspring2) = crossover(offspring1, offspring2)
            else:
                (offspring1, offspring2) = uniform_crossover(offspring1, offspring2)

        # Introduce a small, random change to the population (mutation).
        if random.random() < mutation_probability:
            offspring1 = mutate(offspring1)
        if random.random() < mutation_probability:
            offspring2 = mutate(offspring2)

        # Add the new members to the population.
        new_population.append(offspring1)
        new_population.append(offspring2)

        # If either offspring is better than the best-seen solution, make it the new best.
        if offspring1.fitness > solution_best.fitness:
            solution_best = copy.deepcopy(offspring1)
            stagnation = -1
        if offspring2.fitness > solution_best.fitness:
            solution_best = copy.deepcopy(offspring2)
            stagnation = -1

    # Set the new population as the current population.
    population = new_population

    print("Best fitness at generation %d: %.8f, number of tests: %d, average test length: %d" % (gen, solution_best.fitness, len(solution_best.test_suite), solution_best.average_length()))

    # Increment the generation.
    gen += 1
    stagnation += 1

# Print information about the best test suite seen

print("Best Test Suite:")
print(solution_best.test_suite)
print("Best Fitness: " + str(solution_best.fitness))
print("Number of generations used: " + str(gen))
print("Number of tests: " + str(len(solution_best.test_suite)))
print("Average test length:" + str(solution_best.average_length()))

# Print the best test suite to a file
write_to_file(metadata, solution_best.test_suite)
