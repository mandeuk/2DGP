import random
import json
import os

from pico2d import *

import game_framework
import title_state



name = "MainState"

boy = None
grass = None
font = None



class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)



class Hero:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.image = load_image('Resource\Character\Paladin.png')
        self.dir = 1      #0 = 우하, 1 = 하, 2 = 좌하, 3 = 좌, 4 = 좌상, 5 = 상, 6 = 우상, 7 = 우
        self.action = 0     #움직임 판단용
        self.speed = 5

    def update(self):
        self.frame = (self.frame + 1) % 4
        delay(0.1)
        if self.action == 1:
            if self.dir == 0:
                self.x += self.speed
                self.y -= self.speed
            elif self.dir == 1:
                self.y -= self.speed
            elif self.dir == 2:
                self.x += self.speed
                self.y -= self.speed
            elif self.dir == 3:
                self.x -= self.speed
            elif self.dir == 4:
                self.x -= self.speed
                self.y += self.speed
            elif self.dir == 5:
                self.y += self.speed
            elif self.dir == 6:
                self.x += self.speed
                self.y += self.speed
            elif self.dir == 7:
                self.x += self.speed
#        self.x += self.dir
#        if self.x >= 800:
#            self.dir = -1
#        elif self.x <= 0:
#            self.dir = 1

    def draw(self):
        if self.action == 1:
            self.image.clip_draw(self.frame * 50, self.dir * 50, 50, 50, self.x, self.y)
        elif self.action == 0:
            self.image.clip_draw(0, self.dir * 50, 50, 50, self.x, self.y)


def enter():
    global boy, grass
    boy = Hero()
    grass = Grass()


def exit():
    global boy, grass
    del(boy)
    del(grass)


def pause():
    pass


def resume():
    pass


def handle_events():
    global boy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_DOWN:#하
                boy.dir = 1
                boy.y -= 3
                boy.action = 1
            elif event.key == SDLK_3:#좌하
                boy.dir = 2
                boy.action = 1
            elif event.key == SDLK_LEFT:#좌
                boy.dir = 3
                boy.x -= 3
                boy.action = 1
            elif event.key == SDLK_9:#좌상
                boy.dir = 4
                boy.action = 1
            elif event.key == SDLK_UP:#상
                boy.dir = 5
                boy.y += 3
                boy.action = 1
            elif event.key == SDLK_7:#우상
                boy.dir = 6
                boy.action = 1
            elif event.key == SDLK_RIGHT  :#우
                boy.dir = 7
                boy.x += 3
                boy.action = 1
            elif event.key == SDLK_1:#우하
                boy.dir = 0
                boy.action = 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_DOWN:#하
                boy.dir = 1
                boy.y -= 3
                boy.action = 0
            elif event.key == SDLK_3:#좌하
                boy.dir = 2
                boy.action = 0
            elif event.key == SDLK_LEFT:#좌
                boy.dir = 3
                boy.x -= 3
                boy.action = 0
            elif event.key == SDLK_9:#좌상
                boy.dir = 4
                boy.action = 0
            elif event.key == SDLK_UP:#상
                boy.dir = 5
                boy.y += 3
                boy.action = 0
            elif event.key == SDLK_7:#우상
                boy.dir = 6
                boy.action = 0
            elif event.key == SDLK_RIGHT  :#우
                boy.dir = 7
                boy.x += 3
                boy.action = 0
            elif event.key == SDLK_1:#우하
                boy.dir = 0
                boy.action = 0
            Crashcheck() #벽과의 충돌체크

def update():
    boy.update()


def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()


def Crashcheck(): #벽과의 충돌체크
    global boy
    if boy.x > 780:
        boy.x = 780
    elif boy.x < 20:
        boy.x = 20
    elif boy.y > 580:
        boy.y = 580
    elif boy.y < 20:
        boy.y = 20