from shape_gen import *

class Board:
    
    def __init__(self, filename):
        file = open(filename)
        line = file.readline()
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        meta = line.split(" ")
        
        self.rows = int(meta[0])
        self.columns = int(meta[1])
        
        self.min_each = int(meta[2])
        self.max_cells = int(meta[3])
        
        self.board = []
        for i in range(0, self.columns):
            self.board.append([])
        
        self.ingredients = []
        line = file.readline()
        while line:
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            row = list(line)
            for i in range(0, len(row)):
                if row[i] not in self.ingredients: self.ingredients.append(row[i])
                self.board[i].append(row[i])
            line = file.readline()
            
        self.width = len(self.board)
        self.height = len(self.board[0])
        self.valid_shapes = get_valid_shapes(self.width, self.height, self.max_cells)
            
    def get_valid_shapes(self):
        return self.valid_shapes
        
    def is_acceptable_shape(self, x, y, shape_index):
        count = {
            self.ingredients[0]: 0,
            self.ingredients[1]: 0,
        }
        keys = count.keys()
        shape = self.valid_shapes[shape_index]
    
        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                x_coord = x + i
                y_coord = y + j
                
                count[self.ingredient_at_point(x_coord, y_coord)] += 1
                if count[keys[0]] >= self.min_each and count[keys[1]] >= self.min_each:
                    return True
        
        return False
    
        
    def ingredient_at_point(self, x, y):
        return self.board[x][y]
            
            
    def pretty_print(self):
        print "Rows:", self.rows
        print "Columns:", self.columns
        print "Min Each Ingedient:", self.min_each
        print "Max Cells per slice", self.max_cells
        print
        
        for row in range(0, self.rows):
            for col in range(0, self.columns):
                print self.board[col][row], 
            print
            
BOARD = Board("datasets/medium.in")     
            
if __name__ == "__main__":
    board = Board("datasets/example.in")
    board.pretty_print()
    print board.get_valid_shapes()
    

