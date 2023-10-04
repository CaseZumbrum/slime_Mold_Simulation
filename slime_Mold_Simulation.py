import pygame
import numpy as np
import math
import time
from Video import Video
from numba import jit

xsize = 400
ysize = xsize
n = 5000
nsize = 1 
decay_Rate = 5
decaying = []
weight = .8
speed = 1

class agent:
    def __init__(self, startx, starty,velocity):
        self.x = np.random.randint(10,xsize - 10)
        self.y = np.random.randint(10,ysize - 10)
        self.x,self.y = randomOnCircle()
        self.velocity = velocity
        self.angle = 2* 3.141592 * np.random.rand()
        if(self.x != xsize/2):
            self.angle = np.arctan((self.y-ysize/2)/(self.x-xsize/2))
        elif(self.y > ysize/2):
            self.angle = -1* math.pi
        else:
            self.angle = math.pi

        if(self.x > xsize/2):
            self.angle = -math.pi + self.angle
    
    def updateLoc(self):

        posx,posy = self.check()
        if((not (0<posx < xsize))):
            self.angle = -1*(self.angle - math.pi)
        if((not (0 <posy < ysize))):
            self.angle = -1*(self.angle)
        posx,posy = self.check()
        self.x = posx
        self.y = posy

        
        maxangle = 0
        maxbright = 0
        curbright = 0
        curangle = self.angle
        self.angle = self.angle  + (np.random.rand()-.5)/10
        for i in range (11):
            change = (i-5)/10
            curangle = self.angle + change
            posx,posy = self.checkAtAngle(curangle)
            if(0 < round(posx) < xsize and 0 < round(posy) < ysize):
                curbright = surface.get_at((round(posx),round(posy)))[0]
                
                if(curbright > maxbright):
                    maxbright = curbright
                    
                    maxangle = change
                    
        self.angle = self.angle + maxangle * weight
        #print(maxangle)
        #if(0 < math.ceil(posxneg) < xsize and 0 < math.ceil(posyneg) < ysize and 0 < math.ceil(posxplus) < xsize and 0 < math.ceil(posyplus) < ysize and surface.get_at((math.ceil(posxneg),math.ceil(posyneg)))[0] > surface.get_at((math.ceil(posxplus),math.ceil(posyplus)))[0] ):
        #    self.angle = self.angle -angle_Pull
        #elif(0 < math.ceil(posxneg) < xsize and 0 < math.ceil(posyneg) < ysize and 0 < math.ceil(posxplus) < xsize and 0 < math.ceil(posyplus) < ysize and surface.get_at((math.ceil(posxneg),math.ceil(posyneg)))[0] < surface.get_at((math.ceil(posxplus),math.ceil(posyplus)))[0] ):
        #    self.angle = self.angle +angle_Pull

        #self.x = (self.x + self.velocity * np.cos(self.angle))
        #self.y = (self.y + self.velocity * np.sin(self.angle))
        
        
        #if((not (0<self.x < xsize)) or (not (0 <self.y < ysize))):
        #    self.angle = 2* 3.141592 * np.random.rand()
        #posx,posy = self.check()
        #while((not (0<posx < xsize)) or (not (0 <posy < ysize))):
        #    self.angle = 2* 3.141592 * np.random.rand()
        #    posx,posy = self.check()
        #self.x = posx
        #self.y = posy
        #self.x = (self.x + self.velocity * np.cos(self.angle))
        #self.y = (self.y + self.velocity * np.sin(self.angle))
        
    def check(self):
        posx = (self.x + self.velocity * np.cos(self.angle))
        posy = (self.y + self.velocity * np.sin(self.angle))
        return posx,posy
    
    def checkAtAngle(self,theta):
        posx = (self.x + self.velocity * np.cos(theta))
        posy = (self.y + self.velocity * np.sin(theta))
        return posx,posy
    
def updateSur(surface,a):
    pygame.draw.rect(surface,(200, 200, 200), (a.x, a.y, nsize, nsize))
    a.updateLoc()
    #pygame.draw.rect(surface,(255, 255, 255), (a.x, a.y, nsize, nsize))

    
@jit(nopython=True)
def findBrightPoints(board):
    toBeRected = []
    for x in range(xsize):
        for y in range (ysize):
            cur = board[x][y]
            if(cur >= decay_Rate):
                toBeRected.append([cur,x,y,0])
                board
            elif(cur > 0):
                toBeRected.append([cur,x,y,1])
    return toBeRected

def darkenSurface(surface):
    testarr = pygame.surfarray.array_red(surface)
    to_Be_Rected = findBrightPoints(testarr)
    for i in to_Be_Rected:
        if(i[3] == 0):
            pygame.draw.rect(surface,(i[0]-decay_Rate,i[0]-decay_Rate,i[0]-decay_Rate),(i[1],i[2],1,1))
        elif(i[3] == 1):
            pygame.draw.rect(surface,(i[0]-1,i[0]-1,i[0]-1),(i[1],i[2],1,1))
    #for x in range(xsize):
    #   for y in range(ysize):
    #       cur = surface.get_at((x,y))
    #        
    #        if(cur[0] >= decay_Rate):
    #            pygame.draw.rect(surface,(cur[0]-decay_Rate,cur[1]-decay_Rate,cur[2]-decay_Rate),(x,y,1,1))
    #        elif(cur[0] > 0):
    #            pygame.draw.rect(surface,(cur[0]-1,cur[1]-1,cur[2]-1),(x,y,1,1))
            #else:
             #   mean = 0
              #  for x2 in range(-1,2):
               #     for y2 in range(-1,2):
                #        if(not x == 0 and not x == xsize - 1 and not y == 0 and not y == ysize - 1):
                 #           mean = mean + surface.get_at((x+x2,y+y2))[0]
                  #          
                   # mean = mean/5
                #if(not mean == 0):
                 #   to_Be_Rected.append([mean,(x,y,1,1)])
    #for i in to_Be_Rected:
    #    pygame.draw.rect(surface,(i[0],i[0],i[0]),i[1])
        
def randomOnCircle():
    xcor = np.random.randint(-150,151)
    ycor = round(math.sqrt(150**2 - xcor**2))
    if(np.random.rand() > .5):
        ycor = -1 * ycor      
    return xcor + xsize/2, ycor + ysize/2      
pygame.init()

video = Video((500,500))

surface = pygame.display.set_mode((xsize, ysize))
pygame.display.set_caption("failures")
agents = []
for t in range(n):
    agents.append(agent(math.floor((xsize-nsize)/2),math.floor((ysize+nsize)/2),speed))
for x in range (10000):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
    darkenSurface(surface)
    for i in agents:
        updateSur(surface,i)
    for i in agents:
        pygame.draw.rect(surface,(255, 255, 255), (i.x, i.y, nsize, nsize))
        pygame.draw.rect(surface,(255, 255, 255), (140, 190, 10, 10))
        pygame.draw.rect(surface,(255, 255, 255), (240, 190, 10, 10))
    video.make_png(surface)
    pygame.display.update()