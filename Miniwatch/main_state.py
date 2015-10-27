from pico2d import *
import random
import json
import os
import math
import game_framework
import title_state


name = "MainState"
boy = None
monster = None
font = None
wall = None
timer = 0


class Wall:
    def __init__(self):
        self.image = load_image('Resource\MapTile\Ground_Tile1.png')
        self.tilestate = [[0]*100 for i in range(100)]

    def draw(self):
        global boy
        for x in range(25):
            for y in range(19):
                self.image.draw(x * 32 - boy.x, y * 32 - boy.y)

    def enter(self):
        open('tile.txt', 'r')
        for y in range(100):
            for x in range(100):
                self.tilestate[x][y] = 1
                pass
        pass


class Monster:
    def __init__(self):
        self.x, self.y = 100, 100
        self.image = load_image('Resource\Monster\Bug.png')
        self.frame = 0
        self.state = 0#0:주인공미발견, 1:주인공발견
        self.dir = 0
        self.attack = 0
        self.damage = 5

    def update(self):
        global boy
        if math.sqrt(math.pow(boy.x - self.x, 2.0) + math.pow(boy.y - self.y, 2.0)) < 200:
            self.state = 1
            if math.sqrt(math.pow(boy.x - self.x, 2.0) + math.pow(boy.y - self.y, 2.0)) < 30:
                self.attack += 1
                if self.attack > 50:
                    self.attack = 0
                    boy.hp -= self.damage
        else:
            self.state = 0
            self.attack = 0

        if self.state == 1:
            if boy.x < self.x:
                self.x -= 1
            elif boy.x > self.x:
                self.x += 1
            if boy.y < self.y:
                self.y -= 1
            elif boy.y > self.y:
                self.y += 1
        else:
            pass

    def draw(self):
        global boy
        self.image.clip_draw(self.frame % 4 * 50, self.dir * 50, 50, 50, 400 - (boy.x - self.x), 300 - (boy.y - self.y))


class Hero:
    def __init__(self):
        self.x, self.y = 0, 0
        self.sector = 0     #충돌체크 검사용 섹터
        self.timer = 0
        self.frame = 0
        self.image = load_image('Resource\Character\Paladin.png')
        self.dir = 1      #0 = 우하, 1 = 하, 2 = 좌하, 3 = 좌, 4 = 좌상, 5 = 상, 6 = 우상, 7 = 우
        self.action = 0     #움직임 판단용
        self.speed = 3      #이동속도
        self.hp = 100
        self.ui = load_image('Resource\etc\StateUI.png')
        self.blood = load_image('Resource\etc\healthbar.png')

    def update(self):
        global timer
        if timer > 6:
            timer = 0
            self.frame += 1
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
            Crashcheck() #벽과의 충돌체크

    def draw(self):
        if self.action == 1:
            self.image.clip_draw(self.frame % 4 * 50, self.dir * 50, 50, 50, 400, 300)
        elif self.action == 0:
            self.image.clip_draw(0, self.dir * 50, 50, 50, 400, 300)
        self.ui.draw(400, 25)
        self.blood.clip_draw(0, 0, self.hp, 14, 410, 25)


def enter():
    global boy, wall, monster, ui
    boy = Hero()
    wall = Wall()
    monster = Monster()


def exit():
    global boy, wall, monster
    del(boy)
    del(wall)
    del(monster)


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
            if event.key == SDLK_ESCAPE:#ESC 눌렀을 때
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
                boy.action = 1
            elif event.key == SDLK_9:#좌상
                boy.dir = 4
                boy.action = 1
            elif event.key == SDLK_UP:#상
                boy.dir = 5
                boy.action = 1
            elif event.key == SDLK_7:#우상
                boy.dir = 6
                boy.action = 1
            elif event.key == SDLK_RIGHT  :#우
                boy.dir = 7
                boy.action = 1
            elif event.key == SDLK_1:#우하
                boy.dir = 0
                boy.action = 1

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_DOWN:#하
                boy.dir = 1
                boy.action = 0
            elif event.key == SDLK_3:#좌하
                boy.dir = 2
                boy.action = 0
            elif event.key == SDLK_LEFT:#좌
                boy.dir = 3
                boy.action = 0
            elif event.key == SDLK_9:#좌상
                boy.dir = 4
                boy.action = 0
            elif event.key == SDLK_UP:#상
                boy.dir = 5
                boy.action = 0
            elif event.key == SDLK_7:#우상
                boy.dir = 6
                boy.action = 0
            elif event.key == SDLK_RIGHT  :#우
                boy.dir = 7
                boy.action = 0
            elif event.key == SDLK_1:#우하
                boy.dir = 0
                boy.action = 0


def update():
    global timer
    delay(0.016666)
    timer += 1
    boy.update()
    monster.update()
    checksystem()


def draw():
    global ui
    clear_canvas()
    wall.draw()
    monster.draw()
    boy.draw()
    update_canvas()


def Crashcheck(): #벽과의 충돌체크
    global boy, wall
    if boy.x > 400:
        boy.x = 400
    elif boy.x < -400:
        boy.x = -400
    elif boy.y > 300:
        boy.y = 300
    elif boy.y < -300:
        boy.y = -300


def checksystem():
    global boy
    if boy.hp < 0:
        boy.hp = 0