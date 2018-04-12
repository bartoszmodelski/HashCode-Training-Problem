# -*-coding:Utf-8 -*

def get_valid_shapes(maxx, maxy, maxarea):
    slices = []
    
    for x in range(1, maxx+1):
        for y in range(1, maxy+1):
            if x * y > 1 and x * y <= maxarea:
                slices.append([x, y])
                
    return slices
    

if __name__ == "__main__":
    
    print get_valid_shapes(5, 3, 5)