# -*- coding: utf-8 -*-
"""
Created on Sat May  7 13:55:34 2022

@author: Sandeep Nag
"""

import pgzrun
from random import randint
from pgzero.builtins import Actor

WIDTH = 800
HEIGHT = 600
GRAVITY_STRENGTH = 1

balloon = Actor('balloon')
balloon.pos = 400, 300

bird = Actor('bird-up')
bird.pos = randint(800, 1600), randint(10, 200)

bird2 = Actor("bird-up")
bird2.pos = randint(600, 1600), randint(10, 200)

house = Actor('house')
house.pos = randint(800, 1600), 460

tree = Actor('tree')
tree.pos = randint(800, 1600), 450

bird_up = True
up = False
game_over = False
score = 0
number_of_updates = 0

scores = []
lives = 3

            
def update_high_scores():
    global score, scores
    filename = (r'high-scores.txt')
    scores = []
    with open(filename, 'r') as file:
        line = file.readline()
        high_scores = line.split()
        for high_score in high_scores:
            if(score > int(high_score)):
                scores.append(str(score) + ' ')
                score = int(high_score)
            else:
                scores.append(str(high_score) + ' ')
    with open(filename, 'w') as file:
        for high_score in scores:
            file.write(high_score)


def display_high_scores():
    screen.draw.text('HIGH SCORES', (350, 150), color='yellow')
    y = 175
    position = 1
    for high_score in scores:
        screen.draw.text(str(position) + '.  ' + high_score, (350, y),
                         color='black')
        y += 25
        position += 1


def draw():
    screen.blit('background', (0,0))
    if not game_over:
        balloon.draw()
        bird.draw()
        bird2.draw()
        house.draw()
        tree.draw()
        screen.draw.text('Score: ' + str(score), (700, 5), color='black')
    else:
        display_high_scores()

def on_mouse_down():
    global up
    up = True
    balloon.y -= 50

def on_mouse_up():
    global up
    up = False

def flap():
    global bird_up
    if bird_up:
        bird.image = 'bird-down'
        bird2.image = 'bird-down'
        bird_up = False
    else:
        bird.image = 'bird-up'
        bird2.image = 'bird-up'

        bird_up = True
        
def update():
    global game_over, score, number_of_updates
    if not game_over:
        if not up:
            balloon.y += GRAVITY_STRENGTH  # gravity
        if bird.x > 0:
            bird.x -= 5
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            bird.x = randint(800, 1600)
            bird.y = randint(10, 200)
            score += 1
            number_of_updates = 0

        if bird2.x > 0:
            bird2.x -= 10
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            bird2.x = randint(800, 1600)
            bird2.y = randint(10, 200)
            score += 1
            number_of_updates = 0

        if house.right > 0:
            house.x -= 2
        else:
            house.x = randint(800, 1200)
            score += 1

        if tree.right > 0:
            tree.x -= 2
        else:
            tree.x = randint(800, 1600)
            score += 1
        if bird.x == house.x:
            house.x+1
        if tree.x == house.x:
            house.x+1
            
        if balloon.top < 0 or balloon.bottom > 560:
            game_over = True

            update_high_scores()

        if (balloon.collidepoint(bird.x, bird.y) or 
                balloon.collidepoint(bird2.x, bird2.y) or
                balloon.collidepoint(house.x, house.y) or
                balloon.collidepoint(tree.x, tree.y)):
            game_over = True

            update_high_scores()  

pgzrun.go()