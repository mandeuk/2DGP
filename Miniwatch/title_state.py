import game_framework
import main_state
from pico2d import *

from sound import Sound


name = "TitleState"
image = None
<<<<<<< HEAD
music = None

=======
#bgm = load_music('Resource/Music/Maintheme.mp3')
#bgm.set_volume(64)
#bgm.repeat_play()
>>>>>>> origin/master
def enter():
    global image, music
    image = load_image('Resource\Title\Miniwatch_Title.png')
    if music == None:
        music = Sound()


def exit():
    global image
    del(image)
<<<<<<< HEAD
    music.bgm.set_volume(0)
=======
    #del(bgm)
>>>>>>> origin/master


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
