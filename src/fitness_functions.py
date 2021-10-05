import subprocess
from file_utilities import *

# Measures statement coverage of a test suite.
# Fitness is on scale 1-100. 
# The goal is to maximize the fitness
def statement_fitness(metadata, solution):
    fitness = 0.0
    write_to_file(metadata, solution.test_suite)
    process = subprocess.Popen(["pytest", "--cov=" + metadata["file"], metadata["location"] + "/test_" + metadata["file"] + ".py"], stdout=subprocess.PIPE)
    stdout = str(process.communicate()[0])
    lines = stdout.split("\\n")
    for line in lines:
        # Line we want starts with TOTAL
        if "TOTAL" in line:
            words = line.split(" ")
            coverage = words[len(words)-1]
            fitness = coverage[:len(coverage)-1]

    return float(fitness)

def calculate_fitness(metadata, fitness_function, solution):
    fitness = 0.0

    if fitness_function == "statement": 
        fitness += statement_fitness(metadata, solution)
    else:
        raise Exception("Not a valid fitness function.")

    # Add a penalty to control test suite size
    fitness -= float(len(solution.test_suite)/10)

    # Add a penalty to control the length of individual test cases
    # Get the average test suite length)
    total_length = 0
    for i in range(len(solution.test_suite)):
        total_length += len(solution.test_suite[i]) 
    total_length /= len(solution.test_suite)
    fitness -= float(total_length/30)

    solution.fitness = fitness
