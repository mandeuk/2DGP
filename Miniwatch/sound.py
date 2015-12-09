from pico2d import *

class Sound:
    def __init__(self):
        self.bgm = load_music('Resource/Music/Maintheme.ogg')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        pass

class Attack_sound:
    def __init__(self):
        #self.sound = load_wav('Resource/Music/Paladin_attack.wav')
        pass
