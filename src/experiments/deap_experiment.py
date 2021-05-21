import random
from deap import base, creator, tools

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

# Generate a random solution
def generate():
    return getCategory(random.randint(1, 50))

# Score coverage of outcomes
# Lower scores indicate fewer uncovered outcomes
def evaluate(solution):
    outcomes = ['underweight', 'normal', 'overweight', 'obese', 'severly obese']
    found = 0.0

    for sol in solution:
        if sol in outcomes:
            found += 1.0
            del outcomes[outcomes.index(sol)]

    return [5.0-found]

# Mutation operator
# Can change one random entry to another
def mutate(solution):
    index = random.randint(0, len(solution) - 1)
    solution[index] = getCategory(random.randint(1, 50))
    return solution


if __name__ == '__main__':

    # Initialize fitness function
    # This is a single-objective problem, with a fitness function that we minimize.
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

    # Define an individual solution
    # An individual is a list of BMI results of length 5
    # If we want to use a library, an issue we may run into is that all tests will need to be the same length.
    # If they are not, we will have to write more code ourselves (mutation, crossover, at least)

    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("attr_category", generate)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_category, n = 5)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Register fitness function
    toolbox.register("evaluate", evaluate)

    # Register mutation operator
    toolbox.register("mutate", mutate)

    # Register crossover operator
    toolbox.register("mate", tools.cxTwoPoint)

    # Register selection operator
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Simple EA
    pop = toolbox.population(n=20)
    CXPB = 0.5
    MUTPB = 0.2

    for g in range(10):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop = offspring

    print(pop)
