from board import *
import numpy as np

class Occupied:
    def __init__(self, genome):
        self.board = np.full((BOARD.width, BOARD.height), -1, dtype=int)
        self.shapes = BOARD.get_valid_shapes()
        self.genome = genome
        self.fitness = 0 
    
    def remove_gene(self, index):    
        gene = self.genome[index]
        if gene[3] == 0:
            #print("ERROR: CANNOT REMOVE DEACTIVATED GENE FROM OCCUPIED")
            return
        
        x = gene[0]
        y = gene[1]
        shape_index = gene[2]
        
        rectangle_width = self.shapes[shape_index][0]
        rectangle_height = self.shapes[shape_index][1]
        
        self.board[x:x+rectangle_width, y:y+rectangle_height] = -1
        self.fitness -= rectangle_width * rectangle_height
        self.genome[index, 3] = 0
        
    def add_gene(self, index, popout_clashing = False):
        gene = self.genome[index]
        x = gene[0]
        y = gene[1]
        shape_index = gene[2]
        
        rectangle_width = self.shapes[shape_index][0]
        rectangle_height = self.shapes[shape_index][1]
        
        
        if not ((x + rectangle_width <= BOARD.width) and (y + rectangle_height <= BOARD.height)):
            self.genome[index][3] = 0
            return 
        
        # check if shape meets minimal conditions
        if not (BOARD.is_acceptable_shape(x, y, shape_index)):
            self.genome[index][3] = 0
            return
        
        # if we can remove stuff, remove every gene in the way
        if popout_clashing:
            
            # collect all the original indices 
            needed_area = self.board[x:x+rectangle_width, y:y+rectangle_height].flatten()
            blocking_indices = np.unique(needed_area)
                
            # remove all found indices
            for i in blocking_indices:
                if i != -1:
                    self.remove_gene(i)
        
        
        #check collisions with other rectangles
        if not (self.board[x:x+rectangle_width, y:y+rectangle_height] == -1).all():
            self.genome[index][3] = 0
            return
        
        # no collisions, just put on the occupied and increase the score
        self.board[x:x+rectangle_width, y:y+rectangle_height] = index
        self.genome[index][3] = 1
        self.fitness += rectangle_width * rectangle_height
                
    
