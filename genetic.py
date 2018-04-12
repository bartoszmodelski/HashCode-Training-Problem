from board import *
from individual_new import *
from random import randint, uniform
from copy import deepcopy
import numpy as np
import operator
import time

current_milli_time = lambda: int(round(time.time() * 1000))

from IPython import embed

def fitness(board, individual):
    score = 0
    #for i in range(0, individual.length):
    #    if individual.check_validity(i):
    #        shape = individual.get_shape_for_slice_index(i)
    #        score += shape[0] * shape[1]
    
    #if individual.get_fitness() != individual.get_fitness_new():
        #print(individual.get_fitness(), " - ", individual.get_fitness_new())
        #embed()
    return individual.get_fitness_new()
    

PROB_CROSSOVER = 1.7
PROB_MUTATION = 0.5

def reproduce(ind1, ind2):
    new1 = deepcopy(ind1)
    new2 = deepcopy(ind2)
    
    crossover(new1, new2)
    
    new1.build_occupied_structure()
    new2.build_occupied_structure()
    
    return new1, new2
    
def mutate(ind1, percent):
    new1 = deepcopy(ind1)
    
    new1.mutate_new(percent)
    return new1
        
    
def crossover(ind1, ind2):
    length = ind1.length
    crossover_point1 = randint(0, length)
    crossover_point2 = randint(crossover_point1, length)
    
    a = ind1.genome 
    b = ind2.genome 
    
    c = np.append(a[:crossover_point1], np.append(b[crossover_point1:crossover_point2], a[crossover_point2:], axis=0), axis = 0)
    d = np.append(b[:crossover_point1], np.append(a[crossover_point1:crossover_point2], b[crossover_point2:], axis=0), axis = 0)
    
    ind1.genome = c
    ind2.genome = d
    

population = []
POPULATION_SIZE = 500
INDIV_LEN = 10000
COPULATING = 2
COPULATING_PAIRS = 220
MUTATING = 300
def init_population():
    global population
    for i in range(0, POPULATION_SIZE):
        population.append(Individual(INDIV_LEN))
        
    
def step():
    time_buffer = current_milli_time()
    global population
    scores = {}
    
    for individual in population:
        scores[individual] = fitness(BOARD, individual)
    
    sorted_indivs = sorted(scores.items(), key=operator.itemgetter(1))[::-1]
    best = sorted_indivs[0]
    sorted_indivs = sorted_indivs[0:POPULATION_SIZE]
    
    print("Getting fitnesses took: " + str(current_milli_time() - time_buffer) + "ms")
    time_buffer = current_milli_time()
    
    newsorted = []
    for ind in sorted_indivs:
        newsorted.append(ind[0])
    sorted_indivs = newsorted
    
    population = sorted_indivs
    
    for i in range(0, COPULATING):
        for j in range(i+1, COPULATING):
            new1, new2 = reproduce(population[i], population[j])
            population.append(new1)
            population.append(new2)
    
    for i in range(COPULATING, COPULATING + COPULATING_PAIRS, 2):
        new1, new2 = reproduce(population[i], population[i+1])
        population.append(new1)
        population.append(new2)
            
    for i in range(0, COPULATING+MUTATING + COPULATING_PAIRS):
        new_ind = mutate(population[i], 0.2)
        population.append(new_ind)
    
    population.append(Individual(INDIV_LEN))
    
    print("Reproduction took: " + str(current_milli_time() - time_buffer) + "ms")
    print("Population: " + str(len(population)) + ", best: " + str(best[1]) + ", active genes: " + str(best[0].get_num_of_active_regions()) + "/" + str(INDIV_LEN))
    print("--")
    return best
    
if __name__ == "__main__":
    init_population()
    
    for i in range(0, 50):
        print("ITERATION: " + str(i) + " / 50")
        best = step()
        
    best = step()
    print best
    best[0].print_genome()
    best[0].print_pretty()
    best[0].get_regions(best[1])