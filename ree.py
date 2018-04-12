from board import *
from individual import *
from random import randint, uniform
import copy
import numpy as np

from IPython import embed

def fitness(board, individual):
    score = 0
    for i in range(0, individual.length):
        if individual.check_validity(i):
            shape = individual.get_shape_for_slice_index(i)
            score += shape[0] * shape[1]
            
    return score


PROB_CROSSOVER = 1.0
PROB_MUTATION = 1.0

def reproduce(ind1, ind2):
    new1 = copy.deepcopy(ind1)
    new2 = copy.deepcopy(ind2)
    if uniform(0.0, 1.0) <= PROB_CROSSOVER:
        crossover(new1, new2)
        
    if uniform(0.0, 1.0) <= PROB_MUTATION:
        new1.mutate()
        new2.mutate()
        
    return new1, new2
    
def crossover(ind1, ind2):
    length = ind1.length
    crossover_point = randint(0, length)
    #print "COREES OV:", crossover_point
    
    a = ind1.genome 
    b = ind2.genome 
    
    c = np.append(a[:crossover_point], b[crossover_point:], axis = 0)
    d = np.append(b[:crossover_point], a[crossover_point:], axis = 0)
    
    ind1.genome = c
    ind2.genome = d

    
if __name__ == "__main__":
    length = BOARD.width * BOARD.height
    indiv1 = Individual(6)
    indiv1.initialise_random_slices()
    
    length = BOARD.width * BOARD.height
    indiv2 = Individual(6)
    indiv2.initialise_random_slices()
    
    offspring1, offspring2 = reproduce(indiv1, indiv2)
    
    embed()