import random
import math

def randPos(minX, maxX, minY, maxY):
    return (random.randrange(minX, maxX), random.randrange(minY, maxY))

def getRectangele(pos1, pos2):
    pos1X, pos1Y = pos1
    pos2X, pos2Y = pos2
    width = (pos1X - pos2X)
    height = (pos1Y - pos2Y)
    return (width, height)

def calcLine(pos1, pos2, speed):
    xn, yn = pos1
    line = [pos1]
    width, height = getRectangele(pos2, pos1)
    c = getDistance((width, height))
    x = 0
    while not(x == width):
        if x > width:
            x = x - 1
        else:
            x = x + 1
        m = c / width * x
        y = math.sqrt(m*m-x*x)
        if(height < 0):
            y = y * -1
        line.append((int(x+xn),int(y+yn)))
    line.append(pos2)
    return line

def getDistance(rectangle):
    width, height = rectangle
    return math.sqrt(width*width+height*height)