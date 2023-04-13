from Core import *
from UICore import *
from Environments import get_colors, get_fonts
import graphics

FONT_SIZE = 42
FONT_COLOR = Color(240, 240, 240)

class MMUI(GameObject2):
    __slots__=["btn_play",
               "btn_quit",
               "manager",
               "lbl_title",
               "lbl_title2"]
    def __init__(self, manager, transform=Transform2(), priority=256):
        super().__init__(transform=transform, priority=priority)
        self.manager = manager
        self.lbl_title = UILabel(RectTransform(Vector2(0, 0.85), Vector2(1, 1), Vector2(1, 0.15)), 0, "Flappy-gen", UILabelModel(get_colors("light"), AxisAlignType.CENTER, AxisAlignType.CENTER, get_fonts("title")))
        self.lbl_title2 = UILabel(RectTransform(Vector2(0.1, 0.75), Vector2(1, 1), Vector2(0.8, 0.1)), 0, "Neuro évolution de Flappy Bird", UILabelModel(get_colors("light"), AxisAlignType.CENTER, AxisAlignType.CENTER, get_fonts("title")))
        self.btn_quit = UIButton(RectTransform(Vector2(0.35, 0.075), Vector2(1, 1), Vector2(0.3, 0.1)), 0, "Quit", UIButtonModel(Vector2(0.15, 0.08), get_colors("tone_0"), get_colors("tone_0"), FillMode.OUTLINE, 0.003, get_fonts("button")))
        self.btn_play = UIButton(RectTransform(Vector2(0.35, 0.55), Vector2(1, 1), Vector2(0.3, 0.1)), 0, "Play", UIButtonModel(Vector2(0.15, 0.08), get_colors("tone_3"), get_colors("lightest"), FillMode.FILL, 0, get_fonts("button")))
        self.btn_quit.function_set.on_select = self.manager.quit
        self.btn_play.function_set.on_select = self.manager.play
        self.manager.mm_scene.add_ui_object(self.btn_play)
        self.manager.mm_scene.add_ui_object(self.lbl_title)
        self.manager.mm_scene.add_ui_object(self.btn_quit)
        self.manager.mm_scene.add_ui_object(self.lbl_title2)