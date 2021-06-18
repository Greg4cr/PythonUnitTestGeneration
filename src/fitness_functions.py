import subprocess
from file_utilities import *

# TODO: Add branch coverage, output coverage

# Measures statement coverage of a test suite.
# Fitness is on scale 1-100. 
# The goal is to maximize the fitness
def statementFitness(metadata, solution):
    fitness = 0.0
    writeToFile(metadata, solution.test_suite)
    process = subprocess.Popen(["pytest", "--cov=" + metadata["file"]], stdout=subprocess.PIPE)
    stdout = str(process.communicate()[0])
    lines = stdout.split("\\n")
    for line in lines:
        # Line we want starts with TOTAL
        if "TOTAL" in line:
            words = line.split(" ")
            coverage = words[len(words)-1]
            fitness = coverage[:len(coverage)-1]

    return float(fitness)

# Measures coverage of different outputs of a test suite
# The goal is to maximize the fitness
def outputFitness(metadata, solution):
    # Initialize fitness
    fitness = 0.0
    # Numeric output
    num_output = []
    # Other output
    str_output = []
    
    writeToFileLogging(metadata, solution.test_suite)
    process = subprocess.Popen(["pytest", "-s", "-o", "log_cli=true", "-o", "log_cli_level=INFO"], stdout=subprocess.PIPE)
    stdout = str(process.communicate()[0])
    lines = stdout.split("\\n")
    for line in lines:
        # Line we want starts with INFO
        if "INFO" in line:
            words = line.split(" ")
            output = " ".join(words[6:])
 
            # Is output a number or string?
            # Add to appropriate collection if not already present
            try:
                value = float(output)
                if output not in num_output:
                    num_output.append(float(output))
            except:
                if output not in str_output:
                    str_output.append(output)

    # Measure diversity of numeric output and add to score
    outcomes = discretizeNumbers(num_output, 10)
    fitness += len(outcomes)

    # Add each string outcome
    fitness += len(str_output)

    return float(fitness)

# Transform list of numbers into a set of covered discrete outcomes
# TODO - not sure if equal size bins are good
def discretizeNumbers(num_output, bins):
    # Chop numbers into 10 bins, add covered bins
    min_value = min(num_output)
    max_value = max(num_output)
    range = max_value - min_value
    division = range/bins

    outcomes = []
    for num in num_output:
        outcome = round(num/division)
        if outcome not in outcomes:
            outcomes.append(outcome)

    return outcomes

def calculateFitness(metadata, fitness_function, solution):
    fitness = 0.0

    if fitness_function == "statement": 
        fitness += statementFitness(metadata, solution)
    elif fitness_function == "output":
        fitness += outputFitness(metadata, solution)
    else:
        raise Exception("Not a valid fitness function.")

    # Add a penalty to control test suite size
    fitness -= float(len(solution.test_suite)/10)

    # Add a penalty to control each test case size
    for i in range(len(solution.test_suite)):
        fitness -= float(len(solution.test_suite[i])/20)


    solution.fitness = fitness
