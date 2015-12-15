from pico2d import *
import random
import json
import os
import math
import game_framework
import title_state
import lose_state

from sound import BGM_ingame
from sound import Attack_sound
from sound import Monster_dmgsound

name = "MainState"
paladin = None
monster = [None] * 100
wall = None
stage = 1
timer = 0
music = None
current_time = get_time()
old_time = get_time()

difficulty = 1
killstack = 0

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
        self.tilemap = load_image('Resource/MapTile/tilemap.png')
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
        for i in range(int(y)-1, int(y)+25):
            for j in range(int(x)-1, int(x)+30):
                if j > 99:
                    j = 99
                if i > 99:
                    i = 99
                tempx = (j * 32 - paladin.x)+416
                tempy = (i * 32 - paladin.y)+316
                if self.tilestate[i][j] == '41':
                    self.tilemap.clip_draw(32 * 0, 32*5, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '42':
                    self.tilemap.clip_draw(32 * 1, 32*5, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '43':
                    self.tilemap.clip_draw(32 * 2, 32*5, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '44':
                    self.tilemap.clip_draw(32 * 3, 32*5, 32, 32, tempx, tempy)

                elif self.tilestate[i][j] == '55':
                    self.tilemap.clip_draw(32 * 4, 32*4, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '56':
                    self.tilemap.clip_draw(32 * 5, 32*4, 32, 32, tempx, tempy)

                elif self.tilestate[i][j] == '61':
                    self.tilemap.clip_draw(0, 32*3, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '62':
                    self.tilemap.clip_draw(32 * 1, 32*3, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '63':
                    self.tilemap.clip_draw(32 * 2, 32*3, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '64':
                    self.tilemap.clip_draw(32 * 3, 32*3, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '65':
                    self.tilemap.clip_draw(32 * 4, 32*3, 32, 32, tempx, tempy)

                elif self.tilestate[i][j] == '71':
                    self.tilemap.clip_draw(0, 32*2, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '72':
                    self.tilemap.clip_draw(32 * 1, 32*2, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '73':
                    self.tilemap.clip_draw(32 * 2, 32*2, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '74':
                    self.tilemap.clip_draw(32 * 3, 32*2, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '75':
                    self.tilemap.clip_draw(32 * 4, 32*2, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '76':
                    self.tilemap.clip_draw(32 * 5, 32*2, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '77':
                    self.tilemap.clip_draw(32 * 6, 32*2, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '78':
                    self.tilemap.clip_draw(32 * 7, 32*2, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '79':
                    self.tilemap.clip_draw(32 * 8, 32*2, 32, 32, tempx, tempy)

                elif self.tilestate[i][j] == '81':
                    self.tilemap.clip_draw(0, 32*1, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '82':
                    self.tilemap.clip_draw(32 * 1, 32*1, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '83':
                    self.tilemap.clip_draw(32 * 2, 32*1, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '84':
                    self.tilemap.clip_draw(32 * 3, 32*1, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '85':
                    self.tilemap.clip_draw(32 * 4, 32*1, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '86':
                    self.tilemap.clip_draw(32 * 5, 32*1, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '87':
                    self.tilemap.clip_draw(32 * 6, 32*1, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '88':
                    self.tilemap.clip_draw(32 * 7, 32*1, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '89':
                    self.tilemap.clip_draw(32 * 8, 32*1, 32, 32, tempx, tempy)

                elif self.tilestate[i][j] == '91':
                    self.tilemap.clip_draw(0, 0, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '92':
                    self.tilemap.clip_draw(32 * 1, 0, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '93':
                    self.tilemap.clip_draw(32 * 2, 0, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '94':
                    self.tilemap.clip_draw(32 * 3, 0, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '95':
                    self.tilemap.clip_draw(32 * 4, 0, 32, 32, tempx, tempy)
                elif self.tilestate[i][j] == '96':
                    self.tilemap.clip_draw(32 * 5, 0, 32, 32, tempx, tempy)

                else:
                    pass

    def stage(self):
        f = open('Resource/txt.txt', 'r')
        for i in range(100):
            for j in range(100):
                self.tilestate[i][j] = f.read(2)
        f.close()
        pass


def enter():
    global paladin, wall, monster, music
    paladin = Hero()
    wall = Wall()
    wall.stage()
    for i in range(100):
        monster[i] = Monster()
    music = BGM_ingame()

    randnum = random.randrange(1, 5)
    if randnum == 1:
        music.bgm1.repeat_play()
    if randnum == 2:
        music.bgm2.repeat_play()
    if randnum == 3:
        music.bgm3.repeat_play()
    if randnum == 4:
        music.bgm4.repeat_play()


def exit():
    global paladin, wall, music
    #del(paladin)
    #del(wall)
    music = None


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
                paladin.attack()
                paladin.atk = True
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
    global timer, current_time, paladin, monster, old_time
    frame_time = get_time() - current_time
    current_time += frame_time

    if current_time - old_time > 1:
        for i in range(100):
            monster[i].frame += 1
            old_time = current_time
            if monster[i].frame > 1:
                monster[i].frame = 0


    timer += 1
    dircheck()
    paladin.update(frame_time)
    Crashcheck()#벽과의 충돌체크
    for i in range(100):
        monster[i].update(frame_time)
    checksystem()


def draw():
    global ui, paladin, wall, monster, killstack, difficulty
    clear_canvas()
    wall.draw()
    for i in range(100):
        monster[i].draw()
    paladin.draw()
    string = ('난이도 : %d   레벨 : %d   경험치 : %d' % (difficulty, paladin.level, int(paladin.exp)))
    debug_print(string)
    update_canvas()


def Crashcheck(): #벽과의 충돌체크
    global paladin, wall, monster
    if paladin.x > 3200:
        paladin.x = 3200
    elif paladin.x < 0:
        paladin.x = 0
    if paladin.y > 3200:
        paladin.y = 3200
    elif paladin.y < 0:
        paladin.y = 0
    Cx = int(paladin.x/32)
    Cy = int(paladin.y/32)
    for y in range(Cy-1, Cy+2):
        for x in range(Cx-1, Cx+2):
            if x < 0:
                x = 0
            elif x > 99:
                x = 99
            if y < 0:
                y = 0
            elif y > 99:
                y = 99
            if wall.tilestate[y][x] < '50':
                pass
            else:
                if x < Cx and y < Cy:
                    pass
                elif x < Cx and y > Cy:
                    pass
                elif x > Cx and y < Cy:
                    pass
                elif x > Cx and y > Cy:
                    pass
                elif x == Cx-1:
                    if paladin.x < ((x * 32)+48):
                        paladin.x = ((x * 32)+48)
                elif Cx+1 == x:
                    if ((x * 32)-16) < paladin.x:
                        paladin.x = ((x * 32)-16)
                elif y == Cy-1:
                    if paladin.y < ((y * 32) + 48):
                        paladin.y = ((y * 32) + 48)
                elif Cy+1 == y:
                    if ((y * 32)-16) < paladin.y:
                        paladin.y = ((y * 32)-16)
    for i in range(100):
        Bx = int(monster[i].x/32)
        By = int(monster[i].y/32)
        for y in range(By-1, By+2):
            for x in range(Bx-1, Bx+2):
                if x < 0:
                    x = 0
                elif x > 99:
                    x = 99
                if y < 0:
                    y = 0
                elif y > 99:
                    y = 99
                if int(wall.tilestate[y][x]) < int('50'):
                    pass
                else:
                    if x < Bx and y < By:
                        pass
                    elif x < Bx and y > By:
                        pass
                    elif x > Bx and y < By:
                        pass
                    elif x > Bx and y > By:
                        pass
                    elif x == Bx-1:
                        if monster[i].x < ((x * 32)+48):
                            monster[i].x = ((x * 32)+48)
                    elif Bx+1 == x:
                        if ((x * 32)-16) < monster[i].x:
                            monster[i].x = ((x * 32)-16)
                    elif y == By-1:
                        if monster[i].y < ((y * 32) + 48):
                            monster[i].y = ((y * 32) + 48)
                    elif By+1 == y:
                        if ((y * 32)-16) < monster[i].y:
                            monster[i].y = ((y * 32)-16)


def createwall():
    pass


def checksystem():
    global paladin, difficulty
    if paladin.hp < 0:
        paladin.hp = 0
        game_framework.change_state(lose_state)
    difficulty = int(killstack / 30) + 1
    if paladin.exp > 500 + ((paladin.level-1) * 2000):
        paladin.level += 1
        paladin.maxhp += 20
        paladin.hp = paladin.maxhp
        paladin.dmg += paladin.level


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


class Hero:
    def __init__(self):
        self.x, self.y = 1700, 1600
        self.sector_x = 0     #충돌체크 검사용 섹터
        self.sector_y = 0

        self.timer = 0
        self.frame = 0
        self.image = load_image('Resource\Character\Paladin.png')
        self.effectimg = load_image('Resource\Character\Paladin_effect_Sheet.png')
        self.dir = Rightdown      #0 = 우하, 1 = 하, 2 = 좌하, 3 = 좌, 4 = 좌상, 5 = 상, 6 = 우상, 7 = 우
        self.action = 0     #움직임 판단용
        self.ui = load_image('Resource\etc\StateUI.png')
        self.blood = load_image('Resource\etc\healthbar.png')

        self.maxhp = 100
        self.hp = 100
        self.level = 1
        self.exp = 0
        self.atk = False
        self.atkframe = 0
        self.atksound = Attack_sound()
        self.dmg = 40

        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0

        self.PIXEL_PER_METER = (50.0 / 1.5)
        self.RUN_SPEED_KMPH = 15.0
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

    def update(self, frame_time):
        global timer, monster, paladin
        distance = self.RUN_SPEED_PPS * frame_time
        if timer > 6:
            timer = 0
            self.frame += 1
        if self.action == 1:
            if self.dir == Rightdown:
                self.x += distance
                self.y -= distance
            elif self.dir == Down:
                self.y -= distance
            elif self.dir == Leftdown:
                self.x -= distance
                self.y -= distance
            elif self.dir == Left:
                self.x -= distance
            elif self.dir == Leftup:
                self.x -= distance
                self.y += distance
            elif self.dir == Up:
                self.y += distance
            elif self.dir == Rightup:
                self.x += distance
                self.y += distance
            elif self.dir == Right:
                self.x += distance

    def attack(self):
        global monster
        self.atksound.sound.play(1)
        for i in range(100):
            distance = 40
            if self.dir == 0:#우하
                if self.x-3 < monster[i].x < self.x+distance:
                    if self.y-distance < monster[i].y < self.y+3:
                        monster[i].damaged()
            elif self.dir == 1:#하
                if self.x-(distance*0.75) < monster[i].x < self.x+(distance*0.75):
                    if self.y-(distance*1.25) < monster[i].y < self.y+3:
                        monster[i].damaged()
            elif self.dir == 2:#좌하
                if self.x-distance < monster[i].x < self.x+3:
                    if self.y-distance < monster[i].y < self.y+3:
                        monster[i].damaged()
            elif self.dir == 3:#좌
                if self.x-(distance*1.25) < monster[i].x < self.x+3:
                    if self.y-(distance*0.75) < monster[i].y < self.y+(distance*0.75):
                        monster[i].damaged()
            elif self.dir == 4:#좌상
                if self.x-distance < monster[i].x < self.x+3:
                    if self.y-3 < monster[i].y < self.y+distance:
                        monster[i].damaged()
            elif self.dir == 5:#상
                if self.x-(distance*0.75) < monster[i].x < self.x+(distance*0.75):
                    if self.y-3 < monster[i].y < self.y+(distance*1.25):
                        monster[i].damaged()
            elif self.dir == 6:#우상
                if self.x-3 < monster[i].x < self.x+distance:
                    if self.y-3 < monster[i].y < self.y+distance:
                        monster[i].damaged()
            elif self.dir == 7:#우
                if self.x-3 < monster[i].x < self.x+(distance*1.25):
                    if self.y-(distance*0.75) < monster[i].y < self.y+(distance*0.75):
                        monster[i].damaged()

    def draw(self):
        if self.action == 1:
            self.image.clip_draw(self.frame % 4 * 50, self.dir * 50, 50, 50, 400, 300)
        elif self.action == 0:
            self.image.clip_draw(0, self.dir * 50, 50, 50, 400, 300)
        self.ui.draw(400, 25)
        self.blood.clip_draw(0, 0, int(self.hp / self.maxhp * 100), 14, 412, 25)
        if self.atk:
            self.atkframe += 1
            self.effectimg.clip_draw(0, self.dir*50, 50, 50, 400, 300)
            if self.atkframe > 3:
                self.atk = False
                self.atkframe = 0


class Monster:
    def __init__(self):
        self.x, self.y = 100, 100
        self.image = load_image('Resource\Monster\Bug.png')
        self.frame = 0
        self.state = 0#0:주인공미발견, 1:주인공발견
        self.dir = 0
        self.attack = 0
        self.damage = 5
        self.die = False
        self.dmgsound = Monster_dmgsound()
        self.hp = 100

        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0

        self.PIXEL_PER_METER = (50.0 / 1.5)
        self.RUN_SPEED_KMPH = 10.0
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)
        self.spawn()
    def update(self, frame_time):
        global paladin
        distance = self.RUN_SPEED_PPS * frame_time
        if self.die:
            pass
        else:
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
                if paladin.x+10 < self.x:
                    self.x -= distance
                    self.left = 1
                    self.right = 0
                elif paladin.x-10 > self.x:
                    self.x += distance
                    self.left = 0
                    self.right = 1
                else:
                    self.left = 0
                    self.right = 0
                if paladin.y+10 < self.y:
                    self.y -= distance
                    self.up = 0
                    self.down = 1
                elif paladin.y-10 > self.y:
                    self.y += distance
                    self.up = 1
                    self.down = 0
                else:
                    self.up = 0
                    self.down = 0
            else:
                pass

    def draw(self):
        global paladin
        if self.state == 1:
            self.image.clip_draw((self.frame + 2) * 50, self.dir * 50, 50, 50, 400-(paladin.x - self.x), 300-(paladin.y - self.y))
        else:
            self.image.clip_draw(self.frame * 50, self.dir * 50, 50, 50, 400-(paladin.x - self.x), 300-(paladin.y - self.y))

    def damaged(self):
        global paladin, killstack, difficulty
        self.dmgsound.sound.play(1)
        self.hp -= paladin.dmg
        if self.hp < 1:
            self.spawn()
            killstack += 1
            paladin.exp += 20 + (difficulty * 5)
        pass

    def spawn(self):
        global wall
        self.x, self.y = random.randrange(600, 2600), random.randrange(450, 2750)
        self.hp = 100 + (difficulty * 20)
        self.dir = random.randrange(0, 8)
        Bx = int(self.x / 32)
        By = int(self.y / 32)
        while int(wall.tilestate[By][Bx]) > int('50'):
            if int(wall.tilestate[By][Bx]) < int('50'):
                break
            self.x, self.y = random.randrange(600, 2600), random.randrange(450, 2750)
            Bx = int(self.x / 32)
            By = int(self.y / 32)
        pass