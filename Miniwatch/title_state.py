import game_framework
import main_state
from pico2d import *

from sound import Sound

name = "TitleState"
image = None
music = None
button = None
mouse_x = 0
mouse_y = 0


class Button:
    def __init__(self):
        self.image = load_image('Resource\Title\mainbutton.png')
        self.clicksound = load_wav('Resource/Music/buttonclick.wav')
        self.clicksound.set_volume(127)
        self.start = False
        self.exit = False

    def update(self):
        global mouse_x, mouse_y
        if mouse_x < 450 and mouse_x > 350 and mouse_y > (600-233) and mouse_y < (600-207):
            self.start = True
        elif mouse_x < 450 and mouse_x > 350 and mouse_y > (600-193) and mouse_y < (600-167):
            self.exit = True
        else:
            self.start = False
            self.exit = False

    def draw(self):
        if self.start:
            self.image.clip_draw(0, 26*2, 100, 26, 400, 220)
        else:
            self.image.clip_draw(0, 26*3, 100, 26, 400, 220)
        if self.exit:
            self.image.clip_draw(0, 26*0, 100, 26, 400, 180)
        else:
            self.image.clip_draw(0, 26*1, 100, 26, 400, 180)


def enter():
    global image, music, button
    image = load_image('Resource\Title\Miniwatch_Title.png')
    button = Button()
    if music == None:
        music = Sound()
    else:
        music.bgm.set_volume(64)


def exit():
    global image, button, music
    del(image)
    del(button)
    music = None


def handle_events():
    global mouse_x, mouse_y, button
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mouse_x = event.x
            mouse_y = event.y
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_state(main_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            if button.start:
                button.clicksound.play(1)
                game_framework.change_state(main_state)
            elif button.exit:
                button.clicksound.play(1)
                game_framework.quit()


def draw():
    clear_canvas()
    image.draw(400, 300)
    button.draw()
    update_canvas()


def update():
    button.update()
    pass


def pause():
    pass


def resume():
    pass
