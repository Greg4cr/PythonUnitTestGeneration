import random


# Class that represents a solution. Contains a test suite and a fitness score
class Solution:
    test_suite = []
    fitness = -1

    def __init__(self):
        self.test_suite = []
        self.fitness = -1

    # Gets the average length of a test case
    def average_length(self):
        actions = 0.0

        for test in self.test_suite:
            actions += len(test)

        return actions / len(self.test_suite)


# Generates a test suite, containing between 1 and "max" test cases
# Each test case will contain 1 - "max" actions.
def generate_test_suite(metadata, max_test_cases, max_actions):
    num_test_cases = random.randint(1, max_test_cases)
    test_suite = []
    for i in range(num_test_cases):
        test_suite.append(generate_test_case(metadata, max_actions))
    return test_suite


# Generate a test case of length 1 - max number of actions
# A test case initializes the CUT, then performs actions on it
def generate_test_case(metadata, max_actions):
    test_case = []
    # Initialize the CUT
    test_case.append(generate_constructor(metadata))

    # Generate actions
    num_actions = random.randint(0, max_actions)
    for j in range(num_actions):
        test_case.append(generate_action(metadata))

    return test_case


# Generates a constructor call with random (integer) input
def generate_constructor(metadata):
    # If there are no constructors, or if it has no parameters, create an empty
    # parameter list
    if "constructor" not in metadata.keys() or "parameters" not in \
            metadata["constructor"].keys() or \
            len(metadata["constructor"]["parameters"]) == 0:
        parameter_data = []
    else:
        parameter_data = metadata["constructor"]["parameters"]

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
def generate_action(metadata):
    which_action = random.randint(0, len(metadata["actions"]) - 1)

    if "parameters" in metadata["actions"][which_action].keys():
        parameter_data = metadata["actions"][which_action]["parameters"]
    else:
        parameter_data = []

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

    action = [which_action, parameters]

    return action
