from CanvasImage import *
from statistics import mean
import numpy as np

class calcZoom(CanvasImage):
    def __init__(self, mainframe, path):
        self.points = [] # list of points clicked by user. Max of 2 points
        self.line = 0 # id for the line created by user
        CanvasImage.__init__(self, mainframe, path)
        self.canvas.bind('<Button-1>', self.makePoint)

    # handles the creation of a point
    def makePoint(self, event):
        self.points.append(self.placeDot(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)))
        if len(self.points) == 2:
            self.drawLine()
        elif len(self.points) == 3:
            for i in range(2):
                self.canvas.delete(self.points[i])
            self.canvas.delete(self.line)
            self.line = 0
            self.points = [self.points[2]]

    # places a dot on the canvas
    def placeDot(self, x, y):
        bnd = 3
        return self.canvas.create_oval(x-bnd, y-bnd, x+bnd, y+bnd, fill='red')

    # draws a line between the two points that have been created
    def drawLine(self):
        pnt1 = self.canvas.coords(self.points[0])
        x1 = (mean((pnt1[0], pnt1[2])),mean((pnt1[1], pnt1[3])))
        pnt2 = self.canvas.coords(self.points[1])
        x2 = (mean((pnt2[0], pnt2[2])),mean((pnt2[1], pnt2[3])))
        self.line = self.canvas.create_line(x1[0], x1[1], x2[0], x2[1], fill='red', width=3)
    
    # returns the number of pixels the line is, when image is at original scale
    def getPixelLen(self):
        if self.line != 0:
            x0, y0, x1, y1 = self.canvas.coords(self.line)
            hyp = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            scale = self.imscale # original image * scale = displayed image
            return hyp / scale
        else: 
            return None
