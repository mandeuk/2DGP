import game_framework
import title_state
from pico2d import *

name = "LoseState"
image = None

def enter():
    global image
    image = load_image('Resource/Title/lose_title.png')

def exit():
    global image
    del(image)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(title_state)

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def update():
    pass


def pause():
    pass


def resume():
    pass