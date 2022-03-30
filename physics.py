

import random
import math
from constants import *

class Ball: # Assuming all the balls have the same density
    
    def __init__(self, balls):
        while True:
            x = (random.random()) * (WIDTH - BALL_RADIUS - 2*PADDING) + PADDING # random initial position
            y= (random.random()) * (HEIGHT - BALL_RADIUS - 2*PADDING) + PADDING # random initial position
            point1 = [x, y]
            

            for ball in balls:
                point2 = [ball.x, ball.y]
                if Ball.points_distance(point1, point2) < 2*BALL_RADIUS: # one ball inside another
                    continue
                else:
                    pass
            
            self.x = x
            self.y = y
            theta = (random.random()) * 2 * math.pi
            self.vel_x = MAX_SPEED * math.cos(theta) # random initial velocity
            self.vel_y = MAX_SPEED * math.sin(theta) # random initial velocity
            if RANDOM_MASS:
                self.mass = (random.random()) * (MAX_MASS-MIN_MASS) + MIN_MASS
            else:
                self.mass = 1
            self.color = random.choice(COLOR_LIST)
            break
                
    
    @classmethod # general function so needs to be class function
    def points_distance(cls, point1, point2):
        sqrd_distance = (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2
        return math.sqrt(sqrd_distance)

    
    @classmethod # all the balls are passed so need to be a class function
    def motion(cls, balls):
        for ball in balls:
            ball.x += ball.vel_x
            ball.y += ball.vel_y
    
    def angle_calc(self, ball2): # angle from a ball to another so calculated for each ball seperately
        if ball2.x < self.x:
            theta = (math.atan((ball2.y - self.y)/(ball2.x - self.x))) # will be +ve
            theta = math.pi + theta
        else:   
            theta = math.atan((ball2.y - self.y)/(ball2.x - self.x)) # in radians
        
        return theta
    


    @classmethod
    def circleCollision(cls, ball1, ball2):
        point1 = [ball1.x, ball1.y]
        point2 = [ball2.x, ball2.y]

        distance_between_centers = Ball.points_distance(point1, point2)
        
        if distance_between_centers < 2*BALL_RADIUS:
            return True
        else:
            return False
        


    @classmethod
    def SeperateSmall(cls, ball1, ball2=None): # changes the distance after collision but not their velocities
        #changes the distance wrt to the velocities (along the line of impact) directions so that furthur collision can be avoided
        ball1.x += ball1.vel_x
        ball1.y += ball1.vel_y
        if ball2:
            ball2.x += ball2.vel_x
            ball2.y += ball2.vel_y


                
    @classmethod
    def ballCollision(cls, balls): # returns true if balls collide
        for ball in balls:
            if Ball.elasticWallCollision(ball):
                Ball.SeperateSmall(ball)
            for x in balls:
                if x != ball:
                    if Ball.circleCollision(ball, x):
                        Ball.elasticBallCollision(ball, x) #They have collided time to seperate them along the line of collision
                        Ball.SeperateSmall(ball, x)
        



    @classmethod
    def elasticWallCollision(cls, ball): # change the velocities of the bodies after the elastic collision according to physics
        # we need to calculate the velocities along the line of collision
        isTrue = False
        if (ball.x - BALL_RADIUS < 0) or (ball.x + BALL_RADIUS > WIDTH): # Left wall collision -> reverse the x-velocity of the ball
            ball.vel_x *= -1
            isTrue = True
        if (ball.y - BALL_RADIUS < 0) or (ball.y + BALL_RADIUS > HEIGHT): # Top Wall collision -> reverse the y-velocity of the ball
            ball.vel_y *= -1
            isTrue = True
        return isTrue




    @classmethod
    def elasticBallCollision(cls, ball1, ball2): # change the velocities of the bodies after the elastic collision according to physics
        # we need to calculate the velocities along the line of collision
        # theta1 = ball1.angle_calc(ball2)
        # theta2 = ball2.angle_calc(ball1)
        m1 = ball1.mass
        m2 = ball2.mass

        u1_x = ball1.vel_x
        u2_x = ball2.vel_x

        u1_y = ball1.vel_y
        u2_y = ball2.vel_y


        # Physics calculations -------- Based on conservation of linear momentum and conservation of energy
        v1_x = ((m1-m2)/(m1+m2))*u1_x + ((2*m2)/(m1+m2))*u2_x
        v1_y = ((m1-m2)/(m1+m2))*u1_y + ((2*m2)/(m1+m2))*u2_y

        v2_x = ((2*m1)/(m1+m2))*u1_x - ((m1-m2)/(m1+m2))*u2_x
        v2_y = ((2*m1)/(m1+m2))*u1_y - ((m1-m2)/(m1+m2))*u2_y
        # Physics calculations -------- Based on conservation of linear momentum and conservation of energy


        ball1.vel_x = v1_x
        ball1.vel_y = v1_y

        ball2.vel_x = v2_x
        ball2.vel_y = v2_y
