from Core import *
from RendererCore import *
import Renderer
import Environments

class MdlBackground(Model):
    """ Model graphique pour le rendering du Background de FlappyBird """
    __slots__=["game_object",
               "image_name",
               "image_size",
               "__sprites"]
    def __init__(self):
        self.image_name = "assets/background-night.png"
        self.image_size = Vector2(288, 512)
        self.__sprites = []
        self.game_object = None
        height_ratio = get_engine().HEIGHT/self.image_size.y
        self.image_size = Vector2(self.image_size.x*height_ratio, height_ratio*self.image_size.y)
        width = get_engine().WIDTH * Environments.FBEnvironment.render_part
        count = int(width/self.image_size.x)+1
        print(str(count))
        for i in range(count):
            self.__sprites.append(Sprite(self.image_name, self.image_size, Vector2(self.image_size.x*i+(i*-1) + (get_engine().WIDTH - width), 0)))
        
    def load(self, game_object):
        self.game_object = game_object
        for sprite in self.__sprites:
            sprite.load()

    def render(self):
        for spr in self.__sprites:
            Renderer.render_sprite(spr)

class Background(GameObject2):
    __slots__=["model"]
    def __init__(self, model, priority=0):
        self.model = model
        super().__init__(Transform2(), priority)

    def start(self):
        super().start()
        self.model.load(self)

    def render(self):
        self.model.render()
