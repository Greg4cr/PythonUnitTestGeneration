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
    solution = []
    for step in range(1, random.randint(2, 6)):
        solution.append(getCategory(random.randint(1, 50)))
    return solution

# Score coverage of outcomes
# Lower scores indicate fewer uncovered outcomes
def evaluate(solution):
    outcomes = ['underweight', 'normal', 'overweight', 'obese', 'severly obese']
    found = 0.0

    for sol in solution[0]:
        if sol in outcomes:
            found += 1.0
            del outcomes[outcomes.index(sol)]

    return [5.0-found]

# Mutation operator
# Can change one random entry to another, delete an entry, or add an entry
def mutate(solution):
    action = random.randint(1,3)

    if action == 1: # Change
        index = random.randint(0, len(solution[0]) - 1)
        solution[0][index] = getCategory(random.randint(1, 50))
    elif action == 2 and len(solution[0]) > 1: # Delete
        del solution[0][random.randint(0, len(solution[0]) - 1)]
    elif action == 3: # Add
        solution[0].append(getCategory(random.randint(1, 50)))

    return solution


if __name__ == '__main__':

   # Initialize fitness function
   # This is a single-objective problem, with a fitness function that we minimize.
   creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

   # Define an individual solution
   # An individual is a list of BMI results of varying length 

   creator.create("Individual", list, fitness=creator.FitnessMin)
   toolbox = base.Toolbox()
   toolbox.register("attr_category", generate)
   toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_category, n = 1)

   # Register fitness function
   toolbox.register("evaluate", evaluate)

   # Register mutation operator
   toolbox.register("mutate", mutate)

   ind1 = toolbox.individual()
   ind1.fitness.values = evaluate(ind1)
   
   print(ind1)
   print(ind1.fitness)
