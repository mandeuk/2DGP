from pico2d import *


class Sound:
    def __init__(self):
        self.bgm = load_music('Resource/Music/Maintheme.ogg')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        pass


class BGM_ingame:
    def __init__(self):
        self.bgm1 = load_music('Resource/Music/At_The_Gates.ogg')
        self.bgm2 = load_music('Resource/Music/Further_in.ogg')
        self.bgm3 = load_music('Resource/Music/Heroes_Never_Die.ogg')
        self.bgm4 = load_music('Resource/Music/Pens_and_Swords.ogg')
        self.bgm1.set_volume(45)
        self.bgm2.set_volume(45)
        self.bgm3.set_volume(45)
        self.bgm4.set_volume(45)
        pass


class Attack_sound:
    def __init__(self):
        self.sound = load_wav('Resource/Music/paladinattack.wav')
        self.sound.set_volume(127)
        pass


class Monster_dmgsound:
    def __init__(self):
        self.sound = load_wav('Resource/Music/monsterdamage.wav')
        self.sound.set_volume(127)
        pass