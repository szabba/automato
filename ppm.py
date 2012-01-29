#!/usr/bin/env python2

class Cell(object):


    def __init__(self, r=0, g=0, b=0):
        self.color = [r, g, b]

    def get_color(self):
        return "%d %d %d \n" %(self.color[0], self.color[1], self.color[2])

    def set_color(self, r=0, g=0, b=0):
        self.color = [r,g,b]

class Grid(object):


    def __init__(self, x=0, y=0):
        self.cells = []
        self.x = x
        self.y = y
        
    def get_height(self):
        return self.x

    def set_height(self, x):
        self.x=x

    def get_width(self):
        return self.y

    def set_width(self, y):
        self.y=y
    

    def get_pixels(self):
        return self.cells

    def get_grid(self, *l):
        for line in l:
            self.cells.append([])
            for point in line:
                if point:
                    self.cells[-1].append(Cell(255, 255, 255))
                else:
                    self.cells[-1].append(Cell())

class PpmImage(object):

    
    def __init__(self, filename="img"):
        self.filename=filename + ".ppm"
    
    def get_header(self, obj, rng=255):
        s = "P3 \n %d %d \n %d" % (obj.get_width(), obj.get_height(), rng)
        return s

    def get_content(self, obj):
        s = ""
       
        for row in obj.get_pixels(): # get_pixels ma zwrocic liste list pixeli
            for pixel in row:
                s += pixel.get_color()
         
        return s
            
    def make_image(self, obj):
        file = open(self.filename, 'w')
        file.write(self.get_header(obj) )
        file.write(self.get_content(obj) )


if __name__ == "__main__":
    g = Grid(100,100)
    i = PpmImage()
    i.make_image(g)
