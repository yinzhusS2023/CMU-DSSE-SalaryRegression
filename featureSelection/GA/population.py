import random
from .individual import Individual


class Population:

    def __init__(self,
                 X,
                 y,
                 classifier,
                 validation_function,
                 threshold_function,
                 mutation_rate,
                 selection_size,
                 cross_over_rate):

        # Fetched Params
        self.X = X
        self.Y = y
        self.mutation_rate = mutation_rate
        self.selection_size = selection_size
        self.cross_over_rate = cross_over_rate
        self.classifier = classifier
        self.validation_function = validation_function
        self.threshold_function = threshold_function
        # Related Params
        self.population = []
        self.generation = 0
        self.childSize = X.shape[1]
        self.best_individual = None
        self.finished = False
        self.max_fitness = 0.0
        self.average_fitness = 0.0
        self.mating_pool = []

    # Create a random initial population

    def create_initial_population(self, size):
        for _ in range(size):
            individual = Individual(self.childSize)
            individual.calculate_fitness(
                self.X, self.Y, self.classifier, self.validation_function)

            # Update max fitness
            if individual.fitness > self.max_fitness:
                self.max_fitness = individual.fitness
                self.best_individual = individual

            self.average_fitness += individual.fitness
            self.population.append(individual)
        self.average_fitness /= size

    # Generate a mating pool based on the individual fitness (probability)
    def natural_selection(self):
        self.mating_pool = []
        for index, individual in enumerate(self.population):
            self.mating_pool.append([individual.fitness, index])

    # Generate a new population from the mating pool

    def generate_new_population(self):
        new_population = []
        population_size = len(self.population)
        crossover_fraction = int(population_size * self.cross_over_rate)
        remained_fraction = population_size - crossover_fraction
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        new_population.extend(self.population[:remained_fraction])

        self.average_fitness = 0.0

        for item in new_population:
            self.average_fitness += item.fitness
            item.mutate(self.mutation_rate)

        for _ in range(crossover_fraction):
            partner_a, partner_b = self.selection()

            offspring = partner_a.crossover(partner_b)
            offspring.mutate(self.mutation_rate)
            offspring.calculate_fitness(self.X, self.Y, self.classifier, self.validation_function)

            self.average_fitness += offspring.fitness
            new_population.append(offspring)

        self.population = new_population
        self.generation += 1
        self.average_fitness /= population_size

    def selection(self):
        first_parent_pool = random.choices(
            self.mating_pool, k=self.selection_size)
        second_parent_pool = random.choices(
            self.mating_pool, k=self.selection_size)
        return self.population[sorted(first_parent_pool, reverse=True)[0][1]], self.population[sorted(second_parent_pool, reverse=True)[0][1]]
        # return self.population[random.choice(self.mating_pool)], self.population[random.choice(self.mating_pool)]

    # Evaluate the population
    def evaluate(self):
        best_fitness = 0.0
        for individual in self.population:
            if individual.fitness > best_fitness:
                best_fitness = individual.fitness
                self.max_fitness = best_fitness
                self.best_individual = individual

        if self.threshold_function(best_fitness):
            self.finished = True

    def print_population_status(self):
        print("\nGeneration: " + str(self.generation))
        print("\nAverage Fitness: " + str(self.average_fitness))
        print("\nBest Individual: " + str(self.best_individual))
