from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.color("red")
        self.speed("fastest")
        randomx = random.randint(-240, 240)
        randomy = random.randint(-260, 200)
        self.goto(randomx, randomy)

    def refresh(self):
        newrandomx = random.randint(-280, 280)
        newrandomy = random.randint(-280, 260)
        self.goto(newrandomx, newrandomy)