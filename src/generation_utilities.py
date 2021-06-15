import random

# Generates a test suite, containing between 1 and "max" test cases
# Each test case will contain 1 - "max" actions.
def generateTestSuite(metadata, maxTestsCases, maxActions):
    nTestsCases = random.randint(1,maxTestsCases)
    test_suite = []
    for i in range(nTestsCases):
        test_suite.append(generateTestCase(metadata,maxActions))    
    return test_suite

# Generate a test case of length 1 - max number of actions
# A test case initializes the CUT, then performs actions on it
def generateTestCase(metadata, maxActions):
    test_case = []    
    # Initialize the CUT
    test_case.append(generateConstructor(metadata)) 

    # Generate actions
    nActions = random.randint(0,maxActions)
    for j in range(nActions):
        test_case.append(generateAction(metadata))

    return test_case

# Generates a constructor call
# Picks a random constructor and generates random (integer) input for that constructor
def generateConstructor(metadata):
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
def generateAction(metadata):
    which_action = random.randint(0, len(metadata["actions"]) - 1)
    parameter_data = metadata["actions"][which_action]["parameters"]

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

