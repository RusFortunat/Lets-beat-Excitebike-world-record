# Excitebike with AI player
import sys, time

import pgzrun
import pygame
from pygame.locals import *
import pygame_ai as pai

# I follow Pygame guide for now: https://pygame-ai.readthedocs.io/en/latest/guide.html
# All to be later tested & changed accordingly
class Player(pai.gameobject.GameObject):
    def __init__(self, pos = (0, 0), speed = 0, laneY = 375):
        # First we create the image by filling a surface with blue color
        img = pygame.Surface( (10, 15) ).convert()
        img.fill('bike0')
        # Call GameObject init with appropiate values
        super(Player, self).__init__(img_surf = img, pos = pos, max_speed = 5)
        self.pos_y = pos[1]
        self.speed = speed
        self.laneY = laneY

    def update(ai_input, y): 
        # change speed
        if ai_input == 0 and y == laneY: self.speed = limit(self.speed+0.1, 1, 5)
        if ai_input == 1 and y == laneY: self.speed = limit(self.speed-0.1, 1, 5)
        # change lanes
        if ai_input == 2 and y == laneY: self.pos_y = limit(self.pos_y-50, 375, 525)
        if ai_input == 3 and y == laneY: self.pos_y = limit(self.pos_y+50, 375, 525)
      
    def limit(n, minn, maxn): # limits speed and helps to stay on track
        return max(min(maxn, n), minn)

def generate_track():
    # right now it is not random, because I don't know what these arrays mean
    track = [0,2,0,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,0,
         0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,1,1,1,0,
         0,0,1,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0,0]  
    dirt = [0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,2,1,
             0,0,4,0,1,0,0,0,0,2,0,0,0,3,0,0,0,0,0,
             3,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    return track, dirt        

def main():

    startTime = time.time()
    laps = 5 # ride 5 laps for now
    track, dirt = generate_track() # generate a random track
    AI_rider = Player() # call an instance of the Player class, create an AI bot player
    
    while(lap < laps):

        # here should be the code for deciding how to update the AI speed & position 
        # -- get the environment observation first
        # -- do some random action based on observation (dirt ahead -- change lane; ramp ahead -- adjust speed; nothing -- increase speed)
        
        # update the position of AI rider accordingly
        trackPos -= AI_rider.speed # x(t+1) = x(t) + v*dt
        if(trackPos < -4800): # 4800 is size of the track i presume
            trackPos = 0
            lap +=1
            lastLap = int(time.time() - startTime)
            startTime = time.time()
        if round(AI_rider.pos_y/2) == round(AI_rider.laneY/2):
            bike.y = bike.laneY
            bike.angle = 0
        if bike.direction != 0:
            if bike.y <= 375 or bike.y >= 525 or bike.y == bike.laneY:
                bike.direction = 0
            else: bike.y += bike.direction*2
        if(gametime%(int(8-bike.speed)) == 0): bike.frame = 1 - bike.frame
        a = bike.angle
        bike.image = "bike" + str(bike.frame)
        bike.angle = a
        checkBikeRamp()
        
        def checkBikeRamp():
            tp = trackPos + 25
            trackOffset = tp%100
            trackBlock = int((-tp)/100)+2
            trackheight = 0
            if trackOffset == 0: trackBlock -= 1
            if track[trackBlock] == 1:
                trackheight = (100-trackOffset)
                if bike.y >= bike.laneY-trackheight:
                    bike.y = bike.laneY-trackheight
                    if bike.angle < 45: bike.angle += bike.speed
                if bike.angle < -25:
                    bike.speed = 1
                    bike.angle = 0
                if bike.angle >= -25 and bike.angle < 0: bike.angle = 0
            else:
                if int(bike.y) == int(bike.laneY) and bike.angle < -25:
                    bike.angle = 0
                    bike.speed = 1
            if bike.y < bike.laneY-trackheight and bike.direction != 1:
                bike.y += (2-(bike.speed/3))
                if bike.direction == 0: bike.angle -= 1
                if bike.speed > 1: bike.speed -= 0.02
            muckLane = int((bike.laneY-375)/50)+1
            if muck[trackBlock] == muckLane and int(bike.y) == int(bike.laneY) : bike.speed = bike.speed/1.1    

    



bike = Actor('bike0',center=(150,350), anchor=('center','bottom')) # draws graphics on the screen
bike.speed = 1
bike.frame = bike.direction = 0
bike.laneY = 375
score = trackPos = gametime = lastLap = 0


def draw():
    screen.blit("background", (0, 0))
    drawTrack()
    bike.draw()
    screen.draw.text("LAP TIME: "+str(int(time.time() - startTime)), (20, 555),color=(255,255,255) , fontsize=50)
    screen.draw.text("LAST LAP: "+str(lastLap), topright = (780, 555),color=(255,255,255) , fontsize=50)



def on_key_down(key):
    if key.name == "UP":
        bike.direction = -1
        bike.laneY = limit(bike.laneY-50, 375, 525)
    if key.name == "DOWN":
        bike.direction = 1
        bike.laneY = limit(bike.laneY+50, 375, 525)
    bike.y += bike.direction
        


if __name__ == '__main__':
    pygame.init()
    maim()
    pygame.quit()
  
    #pgzrun.go()
