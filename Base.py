from Core import *
from RendererCore import *
import Renderer
from Environments import FBEnvironment

class MdlBase(Model):
    __slots__=["img_src",
               "img_size",
               "sprite",
               "game_object"]
    def __init__(self):
        self.img_src = "assets/base.png"
        self.game_object = None
        self.__setup()

    def __setup(self):
        self.img_size = Vector2(336, 112)
        self.sprite = Sprite(self.img_src, self.img_size, Vector2())

    def load(self, game_object):
        self.game_object = game_object
        self.img_size = self.img_size
        self.sprite.load()

    def unload(self):
        self.__setup()

    def render(self):
        Renderer.render_relative_sprite(self.sprite, self.game_object.transform)

class Base(GameObject2):
    __slots__=["model", "__size", "manager"]
    def __init__(self, manager, transform=Transform2(), priority=0, model=MdlBase()):
        super().__init__(transform=transform, priority=priority)
        self.model = model
        self.__size = self.model.img_size.mul_comp(self.transform.scale)
        self.__size.y += self.transform.position.y
        self.manager = manager

    def start(self):
        self.model.load(self)
        self.__size = self.model.img_size.mul_comp(self.transform.scale)
        self.__size.y += self.transform.position.y

    def stop(self):
        self.model.unload()
        self.__size = Vector2()

    def update(self):
        self.transform.position.x -= FBEnvironment.move_speed * get_engine().delta_time
        if self.transform.position.x < -self.get_width() + self.manager.pos_x:
            self.transform.position.x = self.manager.get_next_posx()
            self.manager.push_back()

    def get_width(self):
        return self.__size.x

    def get_height(self):
        return self.__size.y

    def render(self):
        self.model.render()

class BaseManager(GameObject2):
    __slots__=["bases", "fb_scene", "base_scale", "y_pos", "pos_x"]
    def __init__(self, fb_scene, base_scale=Vector2(1, 1), transform=Transform2(), priority=1, y_pos=0):
        super().__init__(transform, priority=priority)
        self.y_pos = y_pos
        self.fb_scene = fb_scene
        self.base_scale = base_scale
        self.bases = []
        base = Base(self, Transform2(Vector2(0, 0), self.base_scale), self.priority, MdlBase())
        self.bases.append(base)
        self.fb_scene.add_render_object(base)
        width = get_engine().WIDTH * FBEnvironment.render_part
        self.pos_x = get_engine().WIDTH - width
        count = int(width/base.get_width())
        for i in range(1, count+2):
            basea = Base(self, Transform2(Vector2(base.get_width()*i + self.pos_x, y_pos), self.base_scale), self.priority, MdlBase())
            self.bases.append(basea)
            self.fb_scene.add_render_object(basea)

    def setup(self):
        for i, base in enumerate(self.bases):
            base.transform.position = Vector2(base.get_width()*i + self.pos_x, self.y_pos)

    def start(self):
        self.setup()

    def push_back(self):
        """ pushes the first base of the bases to the end """
        self.bases.append(self.bases.pop(0))

    def get_next_posx(self):
        return round(self.bases[-1].transform.position.x) + self.bases[0].get_width()

    def get_height(self):
        return self.bases[0].get_height()