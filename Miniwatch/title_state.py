import game_framework
import main_state
from pico2d import *


name = "TitleState"
image = None
#bgm = load_music('Resource/Music/Maintheme.mp3')
#bgm.set_volume(64)
#bgm.repeat_play()
def enter():
    global image
    image = load_image('Resource\Title\Miniwatch_Title.png')


def exit():
    global image
    del(image)
    #del(bgm)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

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






