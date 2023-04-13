from Core import *

class FBEnvironment:
    gravity = -9.21 * 200
    move_speed = 1.4 * 100 
    min_velocity = gravity * 20
    jump_delay = 0.17
    y_score_mult = 1
    render_part = 0.6 # portion de la fenetre ou le jeu est rendered, le reste (UI) est rendered a gauche
    
    @staticmethod
    def set_move_speed(new_speed):
        FBEnvironment.move_speed = new_speed

#### Constantes pour l'affichage UI ####

__SWEDISH_COLOR_PALETTE = { # Les couleurs ont étés obtenues ici : https://flatuicolors.com/
    "lightest": Color(250, 250, 250),
    "light": Color(210, 218, 226),
    "darkest": Color(30, 39, 46),
    "tone_0": Color(255, 63, 52),
    "tone_1": Color(15, 188, 249),
    "tone_2": Color(75, 207, 250),
    "tone_3": Color(5, 196, 107),
    "darker": Color(72, 84, 96),
    "midtone": Color(128, 142, 155),
    "tone_4": Color(245, 59, 87)
}

__FONTS_1 = {
    "title": "arialblack",
    "normal": "bahnschrift",
    "button": "arialblack"
}

__FONTS = __FONTS_1
__COLORS = __SWEDISH_COLOR_PALETTE

def get_colors(key):
    return __COLORS[key]

def get_fonts(key):
    return __FONTS[key]