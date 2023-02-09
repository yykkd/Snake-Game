from turtle import Turtle
import random


class Obstacle(Turtle):

    def __init__(self, difficulty):
        super().__init__()
        self.all_obstacles = []
        self.difficulty = difficulty
        self.obstacle_num = 0

        if self.difficulty == "medium":
            self.obstacle_num = 3
        elif self.difficulty == "difficult":
            self.obstacle_num = 4

    def create_obstacle(self):
        for i in range(self.obstacle_num):
            new_obstacle = Turtle("square")
            new_obstacle.color("blue")
            new_obstacle.penup()
            new_obstacle.shapesize(stretch_len=3, stretch_wid=3)
            newrandomx = random.randint(-280, 280)
            newrandomy = random.randint(-280, 250)
            new_obstacle.goto(newrandomx, newrandomy)
            self.all_obstacles.append(new_obstacle)

    def getObstacleNum(self):
        return self.obstacle_num
