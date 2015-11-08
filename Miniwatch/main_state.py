from pico2d import *
import random
import json
import os
import math
import game_framework
import title_state


name = "MainState"
paladin = None
monster = None
font = None
wall = None
timer = 0

#0 = 우하, 1 = 하, 2 = 좌하, 3 = 좌, 4 = 좌상, 5 = 상, 6 = 우상, 7 = 우
Rightdown = 0
Down = 1
Leftdown = 2
Left = 3
Leftup = 4
Up = 5
Rightup = 6
Right = 7

class Wall:
    def __init__(self):
        self.image = load_image('Resource\MapTile\Ground_Tile1.png')
        self.tilestate = [[0]*100 for i in range(100)]

    def draw(self):
        global paladin
        for x in range(25):
            for y in range(19):
                self.image.draw(x * 32 - paladin.x, y * 32 - paladin.y)

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
        global paladin
        if math.sqrt(math.pow(paladin.x - self.x, 2.0) + math.pow(paladin.y - self.y, 2.0)) < 200:
            self.state = 1
            if math.sqrt(math.pow(paladin.x - self.x, 2.0) + math.pow(paladin.y - self.y, 2.0)) < 30:
                self.attack += 1
                if self.attack > 50:
                    self.attack = 0
                    paladin.hp -= self.damage
        else:
            self.state = 0
            self.attack = 0

        if self.state == 1:
            if paladin.x < self.x:
                self.x -= 1
            elif paladin.x > self.x:
                self.x += 1
            if paladin.y < self.y:
                self.y -= 1
            elif paladin.y > self.y:
                self.y += 1
        else:
            pass

    def draw(self):
        global paladin
        self.image.clip_draw(self.frame % 4 * 50, self.dir * 50, 50, 50, 400 - (paladin.x - self.x), 300 - (paladin.y - self.y))


class Hero:
    def __init__(self):
        self.x, self.y = 0, 0
        self.sector = 0     #충돌체크 검사용 섹터
        self.timer = 0
        self.frame = 0
        self.image = load_image('Resource\Character\Paladin.png')
        self.dir = Rightdown      #0 = 우하, 1 = 하, 2 = 좌하, 3 = 좌, 4 = 좌상, 5 = 상, 6 = 우상, 7 = 우
        self.action = 0     #움직임 판단용
        self.speed = 3      #이동속도
        self.hp = 100
        self.ui = load_image('Resource\etc\StateUI.png')
        self.blood = load_image('Resource\etc\healthbar.png')

        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0

    def update(self):
        global timer
        if timer > 6:
            timer = 0
            self.frame += 1
        if self.action == 1:
            if self.dir == Rightdown:
                self.x += self.speed
                self.y -= self.speed
            elif self.dir == Down:
                self.y -= self.speed
            elif self.dir == Leftdown:
                self.x -= self.speed
                self.y -= self.speed
            elif self.dir == Left:
                self.x -= self.speed
            elif self.dir == Leftup:
                self.x -= self.speed
                self.y += self.speed
            elif self.dir == Up:
                self.y += self.speed
            elif self.dir == Rightup:
                self.x += self.speed
                self.y += self.speed
            elif self.dir == Right:
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
    global paladin, wall, monster, ui
    paladin = Hero()
    wall = Wall()
    monster = Monster()


def exit():
    global paladin, wall, monster
    del(paladin)
    del(wall)
    del(monster)


def pause():
    pass


def resume():
    pass


def handle_events():
    global paladin
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            paladin.action = 1
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_DOWN:
                paladin.down = 1
            elif event.key == SDLK_LEFT:
                paladin.left = 1
            elif event.key == SDLK_UP:
                paladin.up = 1
            elif event.key == SDLK_RIGHT:
                paladin.right = 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_DOWN:
                paladin.down = 0
            elif event.key == SDLK_LEFT:
                paladin.left = 0
            elif event.key == SDLK_UP:
                paladin.up = 0
            elif event.key == SDLK_RIGHT:
                paladin.right = 0
            if paladin.down == 0 and paladin.up == 0 and paladin.left == 0 and paladin.right == 0:
                paladin.action = 0


def update():
    global timer
    delay(0.016666)
    timer += 1
    paladin.update()
    monster.update()
    checksystem()
    dircheck()


def draw():
    global ui
    clear_canvas()
    wall.draw()
    monster.draw()
    paladin.draw()
    update_canvas()


def Crashcheck(): #벽과의 충돌체크
    global paladin, wall
    if paladin.x > 400:
        paladin.x = 400
    elif paladin.x < -400:
        paladin.x = -400
    elif paladin.y > 300:
        paladin.y = 300
    elif paladin.y < -300:
        paladin.y = -300


def checksystem():
    global paladin
    if paladin.hp < 0:
        paladin.hp = 0


def dircheck():
    global paladin
    if paladin.down == 1:
        if paladin.left == 1:
            paladin.dir = Leftdown
        elif paladin.right == 1:
            paladin.dir = Rightdown
        elif paladin.up == 1 and paladin.dir == Down:
            paladin.dir = Up
        else:
            paladin.dir = Down
    elif paladin.left == 1:
        if paladin.up == 1:
            paladin.dir = Leftup
        elif paladin.down == 1:
            paladin.dir = Leftdown
        elif paladin.right == 1 and paladin.dir == Left:
            paladin.dir = Right
        else:
            paladin.dir = Left
    elif paladin.up == 1:
        if paladin.left == 1:
            paladin.dir = Leftup
        elif paladin.right == 1:
            paladin.dir = Rightup
        elif paladin.down == 1 and paladin.dir == Up:
            paladin.dir = Down
        else:
            paladin.dir = Up
    elif paladin.right == 1:
        if paladin.up == 1:
            paladin.dir = Rightup
        elif paladin.down == 1:
            paladin.dir = Rightdown
        elif paladin.left == 1 and paladin.dir == Right:
            paladin.dir = Left
        else:
            paladin.dir = Right
