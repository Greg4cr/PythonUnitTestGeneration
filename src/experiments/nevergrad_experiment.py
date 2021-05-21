import random
import nevergrad as ng

# Partial BMI calculation
def getCategory(bmi):
    if bmi < 18.5:
        return 'underweight'
    elif bmi < 25:
        return 'normal'
    elif bmi < 30:
        return 'overweight'
    elif bmi < 35:
        return 'obese'
    else:
        return 'severly obese'

# Generate random solution
def generateSolution():
    solution = []

    for trial in range(1, random.randint(1, 5)):
        solution.append(random.randint(1, 50))

    return solution

# Score coverage of outcomes
# nevergrad aims to minimize scores, so score = uncovered outcomes
def calculateFitness(solution):
    outcomes = ['underweight', 'normal', 'overweight', 'obese', 'severly obese']
    found = 0.0

    for sol in solution:
        result = getCategory(sol)
        if result in outcomes:
            found += 1.0
            del outcomes[outcomes.index(result)]

    return 5.0-found


if __name__ == '__main__':

    # nevergrad does not seem to like solutions of variable size. 
    # If we use it, all tests must start the same length
    solution = ng.p.Array(shape=(5,), lower=1, upper=50).set_integer_casting()

    optimizer = ng.optimizers.NGOpt(parametrization=solution, budget=100)
    recommendation = optimizer.minimize(calculateFitness)
    print (recommendation.value)

    """ 
    Thoughts - nevergrad is not an ideal choice for test generation.
    1) It is limited in the structures it can optimize
    (e.g., it can only generate numeric arrays)
    2) Solutions must be a constant size (so all tests would be same length)
    """
