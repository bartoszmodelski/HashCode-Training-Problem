import numpy as np
from board import *
from IPython import embed
from occupied import Occupied

class Individual:
    def __init__(self, length):
        self.genome = np.zeros([length, 4], dtype=int)
        #x, y, shape, activation
        self.length = length
        self.shapes = BOARD.get_valid_shapes()
        self.initialise_random_slices()
        self.build_occupied_structure()
        
    def build_occupied_structure(self):
        self.occupied = Occupied(self.genome)
        
        for index in range(self.length):
            if self.genome[index, 3] == 1:
                self.occupied.add_gene(index, popout_clashing = False)
        
    
    def get_shape_for_slice_index(self, slice_index):
        return self.shapes[self.genome[slice_index, 2]]
    
    
    def get_fitness_new(self):
        return self.occupied.fitness
    
    def mutate_new(self, percent_of_information_to_mutate, max_change_in_coords = -1):
        if max_change_in_coords == -1:
            max_change_in_coords = int(BOARD.width / 2)
        mutations_to_introduce = int(self.length * percent_of_information_to_mutate)
        
        if mutations_to_introduce == 0:
            print("Number of mutations to introduce equals 0, too small percent_of_information_to_mutate")
        
        for i in range(0, mutations_to_introduce):
            
            gen_index = np.random.randint(self.length)
            self.occupied.remove_gene(gen_index)
            value_index = np.random.randint(3)
            
            # shape mutation
            if value_index == 2:
                self.genome[gen_index, 2] = np.random.randint(len(self.shapes))
            # coords mutation
            else:
                self.mutate_coords(gen_index, max_change_in_coords)
                if not self.are_coords_within_board(gen_index):
                    self.randomize_coords(gen_index)
            self.occupied.add_gene(gen_index, np.random.randint(10) > 8)
            
            
    def randomize_coords(self, gen_index):
        self.genome[gen_index, 0] = np.random.randint(BOARD.width - 2)
        self.genome[gen_index, 1] = np.random.randint(BOARD.height - 2)

    def mutate_coords(self, gen_index, max_change):
        self.genome[gen_index, 0] += max_change / 2  - np.random.randint(max_change)
        self.genome[gen_index, 1] += max_change / 2 - np.random.randint(max_change)
    
    def are_coords_within_board(self, gen_index):
        b = (self.genome[gen_index, 0] >= 0) and (self.genome[gen_index, 0] <= BOARD.width - 2)
        a = (self.genome[gen_index, 1] >= 0) and (self.genome[gen_index, 1] <= BOARD.height - 2)
        return a and b
    
    
    def mutate(self, max_change = 10, keep_correct = True, to_mutate_value = -1, to_mutate_gen = -1, range = 5):
        if to_mutate_value == -1:
            to_mutate_value = np.random.randint(2)
            
        if to_mutate_gen == -1:
            to_mutate_gen = np.random.randint(self.length)
    
        if to_mutate_value == 1:
            self.genome[to_mutate_gen, to_mutate_value] = np.random.randint(len(self.shapes))
        else:
            self.genome[to_mutate_gen, 0] += max_change / 2  - np.random.randint(max_change)
            self.genome[to_mutate_gen, 1] += max_change / 2 - np.random.randint(max_change)
            
            if  (self.genome[to_mutate_gen, 0] < 0) or (self.genome[to_mutate_gen, 0] >= BOARD.width):
                self.genome[to_mutate_gen, 0] = np.random.randint(BOARD.width - 2)
            
            if  (self.genome[to_mutate_gen, 1] < 0) or (self.genome[to_mutate_gen, 1] >= BOARD.height):
                self.genome[to_mutate_gen, 1] = np.random.randint(BOARD.height - 2)
        
    def print_genome(self):
        for i in range(0, self.length):
            shape_index = self.genome[i, 2]
            print(i, " - ", self.genome[i, 0], self.genome[i, 1], " - ", self.shapes[shape_index][0], self.shapes[shape_index][1], " - ", self.genome[i, 3])
    
    ''' SLOW, Check if slice_index is within borders and isn't clashing with anything '''
    def check_validity(self, slice_index):
        
        occupied = np.zeros([BOARD.width, BOARD.height], dtype=int)
        
        for index in range(self.length):
            x = self.genome[index, 0]
            y = self.genome[index, 1]
            shape_index = self.genome[index, 2]
            
            rectangle_width = self.shapes[shape_index][0]
            rectangle_height = self.shapes[shape_index][1]
            
            
            if (x + rectangle_width <= BOARD.width) and (y + rectangle_height <= BOARD.height):
                if (BOARD.is_acceptable_shape(x, y, shape_index)):
                    if (occupied[x:x+rectangle_width, y:y+rectangle_height] == 0).all():
                        occupied[x:x+rectangle_width, y:y+rectangle_height] += 1
                        if slice_index == index:
                            return True
            
            if (index == slice_index):
                return False
        
        print("If we here, something's fucked up")
        
    def get_fitness(self):
        occupied = np.zeros([BOARD.width, BOARD.height], dtype=int)
        score = 0
        
        for index in range(self.length):
            x = self.genome[index, 0]
            y = self.genome[index, 1]
            shape_index = self.genome[index, 2]
            
            rectangle_width = self.shapes[shape_index][0]
            rectangle_height = self.shapes[shape_index][1]
            if (x + rectangle_width <= BOARD.width) and (y + rectangle_height <= BOARD.height):
                if (BOARD.is_acceptable_shape(x, y, shape_index)):
                    if (occupied[x:x+rectangle_width, y:y+rectangle_height] == 0).all():
                        occupied[x:x+rectangle_width, y:y+rectangle_height] += 1
                        #add points
                        score += rectangle_width * rectangle_height
        
                        
        return score
        
    def initialise_random_slices(self):
        # x coordinants
        x = np.random.randint(BOARD.width, size=(self.length))
        # y coordinants
        y = np.random.randint(BOARD.height, size=(self.length))
        # shape indices
        shape_indices = np.random.randint(len(self.shapes), size=self.length)
        activations = np.random.randint(2, size=self.length)
        
        self.genome[:, 0] = x
        self.genome[:, 1] = y
        self.genome[:, 2] = shape_indices
        self.genome[:, 3] = activations

    def print_pretty(self):
        # REGION WITH INVERTED X,Y COORDINATES
        occupied = np.zeros([BOARD.height,  BOARD.width], dtype=int)
        for index in range(self.length):
            x = self.genome[index, 0]
            y = self.genome[index, 1]
            shape_index = self.genome[index, 2]
            
            rectangle_width = self.shapes[shape_index][0]
            rectangle_height = self.shapes[shape_index][1]
            
            #created inversely for printing
            if self.genome[index, 3] == 1:
                occupied[y:y+rectangle_height, x:x+rectangle_width] += index + 1

        print(occupied)
        # END OF INVERTED
    
    def get_num_of_active_regions(self):

        occupied = np.zeros([BOARD.width, BOARD.height], dtype=int)
        regions = 0
        
        for index in range(self.length):
            x = self.genome[index, 0]
            y = self.genome[index, 1]
            shape_index = self.genome[index, 2]
            
            rectangle_width = self.shapes[shape_index][0]
            rectangle_height = self.shapes[shape_index][1]
            
            if (x + rectangle_width <= BOARD.width) and (y + rectangle_height <= BOARD.height):
                if (BOARD.is_acceptable_shape(x, y, shape_index)):
                    if (occupied[x:x+rectangle_width, y:y+rectangle_height] == 0).all():
                        occupied[x:x+rectangle_width, y:y+rectangle_height] += 1
                        regions += 1
        
                        
        return regions



    def get_regions(self, score):
        # REGION WITH INVERTED X,Y COORDINATES
        regions_indices = []
        occupied = np.zeros([BOARD.height,  BOARD.width], dtype=int)
        for index in range(self.length):
            x = self.genome[index, 0]
            y = self.genome[index, 1]
            shape_index = self.genome[index, 2]
            
            rectangle_width = self.shapes[shape_index][0]
            rectangle_height = self.shapes[shape_index][1]
            
            #created inversely for printing
            if self.check_validity(index):
                occupied[y:y+rectangle_height, x:x+rectangle_width] += index
                regions_indices.append(index)
        # END OF INVERTED
        
        file = open("submission.txt", "w")
        file.write(str(len(regions_indices)))
        file.write("\n")
        
        for i in regions_indices:
            x1 = self.genome[i, 0]
            y1 = self.genome[i, 1]
            x2 = self.shapes[self.genome[i, 2]][0] + x1 - 1
            y2 = self.shapes[self.genome[i, 2]][1] + y1 - 1
            
            file.write(str(y1) + " " + str(x1) + " " + str(y2) + " " + str(x2))
            file.write("\n")
            
        file.close()
            
            
    
        
if __name__ == "__main__":
    a = Individual(3)
    a.initialise_random_slices()
    a.print_pretty()
    embed()