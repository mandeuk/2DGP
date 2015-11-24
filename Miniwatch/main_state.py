from pico2d import *
import random
import json
import os
import math
import game_framework
import title_state
import lose_state


name = "MainState"
paladin = None
monster = [None] * 100
font = None
wall = None
stage = 1
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
        self.image1 = load_image('Resource/MapTile/Ground_Tile1.png')
        self.image2 = load_image('Resource/MapTile/Pillar_Top.png')
        self.image3 = load_image('Resource/MapTile/Wall_RRTile1.png')
        self.image4 = load_image('Resource/MapTile/Wall_UUTile1.png')
        self.image5 = load_image('Resource/MapTile/Pillar_Mid.png')
        self.tilestate = [[0]*100 for i in range(100)]

    def draw(self):
        global paladin
        x = (paladin.x)/32 - 12
        y = (paladin.y)/32 - 10
        if x < 0:
            x = 0
        elif x > 99:
            x = 99
        if y < 0:
            y = 0
        elif y > 99:
            y = 99
        print(x,   paladin.x,   paladin.y)######
        for i in range(int(y), int(y)+25):
            for j in range(int(x), int(x)+30):
                if j > 99:
                    j = 99
                if i > 99:
                    i = 99
                tempx = (j * 32 - paladin.x)+400
                tempy = (i * 32 - paladin.y)+300
                if self.tilestate[i][j] == '01':
                    self.image1.draw(tempx, tempy)
                elif self.tilestate[i][j] == '02':
                    self.image2.draw(tempx, tempy)
                elif self.tilestate[i][j] == '03':
                    self.image3.draw(tempx, tempy)
                elif self.tilestate[i][j] == '04':
                    self.image4.draw(tempx, tempy)
                elif self.tilestate[i][j] == '05':
                    self.image5.draw(tempx, tempy)
                else:
                    pass

    def stage(self):
        f = open('Resource/text.txt', 'r')
        for i in range(100):
            for j in range(100):
                self.tilestate[i][j] = f.read(2)
                #print(self.tilestate[i][j])#######
        f.close()
        pass


class Monster:
    def __init__(self):
        self.x, self.y = random.randrange(2000), random.randrange(2000)
        self.image = load_image('Resource\Monster\Bug.png')
        self.frame = 0
        self.state = 0#0:주인공미발견, 1:주인공발견
        self.dir = 0
        self.attack = 0
        self.damage = 5

        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0

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
                self.left = 1
                self.right = 0
            elif paladin.x > self.x:
                self.x += 1
                self.left = 0
                self.right = 1
            else:
                self.left = 0
                self.right = 0
            if paladin.y < self.y:
                self.y -= 1
                self.up = 0
                self.down = 1
            elif paladin.y > self.y:
                self.y += 1
                self.up = 1
                self.down = 0
            else:
                self.up = 0
                self.down = 0
        else:
            pass

    def draw(self):
        global paladin
        self.image.clip_draw(self.frame % 4 * 50, self.dir * 50, 50, 50, 400-(paladin.x - self.x), 300-(paladin.y - self.y))


class Hero:
    def __init__(self):
        self.x, self.y = 0, 0
        self.sector_x = 0     #충돌체크 검사용 섹터
        self.sector_y = 0

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
            Crashcheck()#벽과의 충돌체크

    def draw(self):
        if self.action == 1:
            self.image.clip_draw(self.frame % 4 * 50, self.dir * 50, 50, 50, 400, 300)
        elif self.action == 0:
            self.image.clip_draw(0, self.dir * 50, 50, 50, 400, 300)
        self.ui.draw(400, 25)
        self.blood.clip_draw(0, 0, self.hp, 14, 412, 25)


def enter():
    global paladin, wall, monster, ui
    paladin = Hero()
    wall = Wall()
    for i in range(100):
        monster[i] = Monster()
    wall.stage()


def exit():
    global paladin, wall, monster, font, stage, timer, Rightdown, Down, Leftdown, Left, Leftup, Up, Rightup, Right
    del(paladin)
    del(wall)
#    del(monster)
#    del(font)
#    del(stage)
#    del(timer)
#    del(Rightdown)
#    del(Down)
#    del(Leftdown)
#    del(Left)
#    del(Leftup)
#    del(Up)
#    del(Rightup)
#    del(Right)


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
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_DOWN:
                paladin.down = 1
                paladin.action = 1
            elif event.key == SDLK_LEFT:
                paladin.left = 1
                paladin.action = 1
            elif event.key == SDLK_UP:
                paladin.up = 1
                paladin.action = 1
            elif event.key == SDLK_RIGHT:
                paladin.right = 1
                paladin.action = 1
            elif event.key == SDLK_a:
                pass
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
    #delay(0.01)
    timer += 1
    dircheck()
    paladin.update()
    for i in range(100):
        monster[i].update()
    checksystem()


def draw():
    global ui
    clear_canvas()
    wall.draw()
    for i in range(100):
        monster[i].draw()
    paladin.draw()
    update_canvas()


def Crashcheck(): #벽과의 충돌체크
    global paladin, wall
    if paladin.x > 2750:
        paladin.x = 2750
    elif paladin.x < -400:
        paladin.x = -400
    if paladin.y > 2850:
        paladin.y = 2850
    elif paladin.y < -300:
        paladin.y = -300
    #for x in range(100):
        #for y in range(100):


def createwall():
    pass


def checksystem():
    global paladin
    if paladin.hp < 0:
        paladin.hp = 0
        game_framework.change_state(lose_state)


def dircheck():
    global paladin, monster
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

    for i in range(100):
        if monster[i].down == 1:
            if monster[i].left == 1:
                monster[i].dir = Leftdown
            elif monster[i].right == 1:
                monster[i].dir = Rightdown
            elif monster[i].up == 1 and monster[i].dir == Down:
                monster[i].dir = Up
            else:
                monster[i].dir = Down
        elif monster[i].left == 1:
            if monster[i].up == 1:
                monster[i].dir = Leftup
            elif monster[i].down == 1:
                monster[i].dir = Leftdown
            elif monster[i].right == 1 and monster[i].dir == Left:
                monster[i].dir = Right
            else:
                monster[i].dir = Left
        elif monster[i].up == 1:
            if monster[i].left == 1:
                monster[i].dir = Leftup
            elif monster[i].right == 1:
                monster[i].dir = Rightup
            elif monster[i].down == 1 and monster[i].dir == Up:
                monster[i].dir = Down
            else:
                monster[i].dir = Up
        elif monster[i].right == 1:
            if monster[i].up == 1:
                monster[i].dir = Rightup
            elif monster[i].down == 1:
                monster[i].dir = Rightdown
            elif monster[i].left == 1 and monster[i].dir == Right:
                monster[i].dir = Left
            else:
                monster[i].dir = Right