import subprocess
from file_utilities import *

# TODO: Add branch coverage, output coverage

# Measures statement coverage of a test suite.
# Fitness is on scale 1-100. 
# The goal is to maximize the fitness
def statementFitness(metadata, solution):
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

    return float(fitness)

def calculateFitness(metadata, fitness_function, solution):
    fitness = 0.0

    if fitness_function == "statement": 
        fitness += statementFitness(metadata, solution)

    # Add a penalty to control test suite size
        fitness -= float(len(solution.test_suite)/10)

    solution.fitness = fitness
