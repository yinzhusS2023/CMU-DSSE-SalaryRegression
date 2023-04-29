import random
import math
from time import time
from IO.ModelIO import ModelIO
from IO.ObjectWriter import ObjectManager

from trainer import ModelTrainer


class SimulatedAnnealing:

    @staticmethod
    def generate_initial_state(size):
        random_array = [random.choice([True, False]) for _ in range(size)]
        return random_array

    @staticmethod
    def get_neighbor(state):
        index = random.choice(range(len(state)))
        neighbor = state[:]
        neighbor[index] = not neighbor[index]
        # Reject the case where no feature is selected
        if all([(not item) for item in neighbor]):
            return SimulatedAnnealing.get_neighbor(state)
        return neighbor

    @staticmethod
    def get_X(X, state):
        return X[:, state]

    @staticmethod
    def get_number_of_features(state):
        return sum([(1 if item else 0) for item in state])

    @staticmethod
    def current_state_to_str(state):
        return '-'.join([str(item) for item in state])

    @staticmethod
    def simulated_annealing(X,
                            y,
                            classifier,
                            # Validation that outputs the validate result
                            validation_function,
                            # Threshold that determines whether to terminate current execution
                            threshold_function,
                            # Optional Parameters
                            temperature=0.07,
                            cooling_rate=0.8,
                            frozen_temperature=10**(-25),
                            temperature_constant=200,
                            max_iterations=1000
                            ):
        try:
            start_time = time()
            current_state = SimulatedAnnealing.generate_initial_state(
                X.shape[1])

            current_score = SimulatedAnnealing.objective(
                X, y, current_state, classifier, validation_function)
            best_state = current_state
            best_score = current_score

            this_iteration = 0

            while temperature > frozen_temperature and this_iteration < max_iterations:
                accepted_time = 0
                average_score = 0
                for _ in range(temperature_constant):
                    # Generate a new candidate state by flipping one bit of the current state
                    candidate_state = SimulatedAnnealing.get_neighbor(
                        current_state)

                    # Evaluate the candidate state
                    candidate_score = SimulatedAnnealing.objective(
                        X, y, current_state, classifier, validation_function)
                    average_score += candidate_score

                    # Determine whether to accept the candidate state
                    delta = current_score - candidate_score

                    if delta < 0 or SimulatedAnnealing.energy_magnitude_equation_accepted(delta, temperature):
                        # print("Iter {} Accepted".format(this_iteration))
                        accepted_time += 1
                        current_state = candidate_state
                        current_score = candidate_score

                    # Update the best state and cost
                    if current_score > best_score:
                        best_state = current_state
                        best_score = current_score

                average_score /= temperature_constant
                # print("Accepted time: {}".format(accepted_time))
                # print("Average Score: {}".format(average_score))
                # print(SimulatedAnnealing.current_state_to_str(current_state))

                print("Iter {}: temperature:{}  best_score: {}, best_state: {}".format(
                    this_iteration, temperature, best_score, SimulatedAnnealing.current_state_to_str(best_state)))

                if threshold_function(best_score):
                    break

                # Cool the temperature
                temperature *= cooling_rate
                this_iteration += 1

                train_success, train_result = ModelTrainer.train_by_grid_search(
                    X[:, best_state], y, classifier)
                if not train_success:
                    print(
                        "Error[in validation function]: training failed in model saving")
                # {
                #     "model_name": model_name,
                #     "training_time": training_time,
                #     "best_params": grid_search.best_params_,
                #     "best_model": grid_search.best_estimator_
                # }
                model = train_result['best_model']
                ModelIO.save_model(model,
                                   "result/SA/generation_{}_fit_{}.model".format(this_iteration, best_score))
                ObjectManager.write_object(
                    "result/SA/generation_{}_fit_{}.genes".format(this_iteration, best_score), best_state)

            total_time = time() - start_time

            # print("Iter {}: temperature:{}  best_score: {}, best_state: {}".format(
            #     this_iteration, temperature, best_score, SimulatedAnnealing.current_state_to_str(best_state)))

            return True, {
                "X": SimulatedAnnealing.get_X(X, best_state),
                "mask": current_state,
                "time_used": total_time,
                "number_of_iterations": this_iteration,
                "number_of_features": SimulatedAnnealing.get_number_of_features(best_state)
            }
        except Exception as e:
            print("SA failed because of: {}".format(e))
            return False, None

    # Define the objective function
    @staticmethod
    def objective(X, Y, current_state, classifier, validation_function):
        # A fitness of a gene with no selection is 0
        if all([(not item) for item in current_state]):
            return 0.0
        # Select the column by the gene(the mask)
        X = SimulatedAnnealing.get_X(X, current_state)
        # Calculate fitness by function provided
        calculate_success, fitness_result = validation_function(
            X, Y, classifier)
        # Fail for a zero fitness:
        if not calculate_success:
            print(
                "Error[In SA.individual.objective]: validation function failed")
            return 0.0
        return fitness_result

    @staticmethod
    def energy_magnitude_equation_accepted(delta, temperature):
        return random.random() < math.exp(float(-delta)/float(temperature))
