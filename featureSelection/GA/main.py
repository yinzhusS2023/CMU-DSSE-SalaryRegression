from time import time
from .population import Population


def genetic_algorithm(
        # Required Parameters
        X,
        y,
        classifier,
        # Validation that outputs the validate result
        validation_function,
        # Threshold that determines whether to terminate current execution
        threshold_function,
        # Optional Parameters
        population_size=100,
        mutation_rate=0.03,
        max_iterations=1000,
        selection_size=20,
        cross_over_rate=0.8):

    try:
        # Create a population randomly
        # Evaluate the population
        # Loop until stop condition is true
        # Natural selection
        # Generate new population
        # Evaluate the new populations
        # End loop
        GA_start_time = time()

        population = Population(X,
                                y,
                                classifier,
                                validation_function,
                                threshold_function,
                                mutation_rate,
                                selection_size,
                                cross_over_rate)
        print(population)
        population.create_initial_population(population_size)
        iteration_count = 0
        while not population.finished and iteration_count < max_iterations:
            print("iteration: ", iteration_count)
            population.natural_selection()
            population.generate_new_population()
            population.evaluate()
            population.print_population_status()
            iteration_count += 1

        time_used = time()-GA_start_time
        return True, {'X': population.best_individual.get_selected_feature(X),
                      'mask': population.best_individual.genes,
                      'time_used': time_used,
                      'number_of_iterations': iteration_count,
                      'number_of_features': population.best_individual.get_number_of_features()}
    except Exception as e:
        print("GA Failed because: {}".format(e))
        return False, None
