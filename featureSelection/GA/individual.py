import random


class Individual:
    # Size of the individual is the number of genes required
    def __init__(self, size) -> None:
        '''
        size is the total number of features
        '''
        self.size = size
        self.genes = self.generate_random_genes(size)
        self.fitness = 0.0

    # Create random individual
    @staticmethod
    def generate_random_genes(size):
        """
        Randomly Generate Sequences of indexes that is a valid entry
        """
        random_array = [random.choice([True, False]) for _ in range(size)]
        return random_array

    def get_selected_feature(self, X):
        return X[:, self.genes]

    def get_number_of_features(self):
        return sum([(1 if item else 0) for item in self.genes])

    # Fitness function: it returns a floating point of "correct" characters

    def calculate_fitness(self, X, Y, classifier, validation_function):

        # A fitness of a gene with no selection is 0
        if all([(not item) for item in self.genes]):
            self.fitness = 0.0
            return 0.0
        # Select the column by the gene(the mask)
        X = self.get_selected_feature(X)
        # Calculate fitness by function provided
        calculate_success, fitness_result = validation_function(
            X, Y, classifier)
        # Fail for a zero fitness:
        if not calculate_success:
            print(
                "Error[In GA.individual.calculate_fitness]: validation function failed")
            self.fitness = 0.0
            return 0.0
        self.fitness = fitness_result
        return fitness_result

    # Crossover: offspring with half genes of both parents

    def crossover(self, partner):
        '''
        Merge parents genes together at a random position      
        '''
        chrome_length = len(self.genes) // 2
        child = Individual(self.size)
        child.genes = self.genes[:chrome_length] + \
            partner.genes[chrome_length:]
        return child

    # Mutation: base on the mutation rate, choose a random character

    def mutate(self, mutation_rate):
        # Pool for selection
        for i in range(len(self.genes)):
            if random.uniform(0, 1) < mutation_rate:
                self.genes[i] = not self.genes[i]

    def __str__(self):
        return '-'.join(([str(item) for item in sorted(self.genes)])) + ' -> fitness: ' + str(self.fitness)
