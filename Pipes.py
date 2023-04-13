import Renderer
from RendererCore import *
from Core import *
from Environments import FBEnvironment
import math
import random


PIPE_TEXTURES_UP = ["assets/pipe-green.png",
                    "assets/pipe-red.png"]
PIPE_TEXTURES_DOWN = ["assets/pipe-green-downside.png",
                      "assets/pipe-red-downside.png"]

class MdlPipe(Model):
    __slots__=["img_src_up",
               "img_src_down",
               "img_size",
               "sprite1",
               "sprite2",
               "game_object"]
    def __init__(self):
        rand = random.randint(0, 1)
        self.img_src_down = PIPE_TEXTURES_UP[rand]
        self.img_src_up = PIPE_TEXTURES_DOWN[rand]
        self.game_object = None
        self.__setup()

    def __setup(self):
        self.img_size = Vector2(52, 320) # originally 52 by 320
        #self.img_size = Vector2(12, 100)

    def load(self, game_object):
        self.game_object = game_object
        self.img_size = self.img_size
        self.sprite1 = Sprite(self.img_src_up, self.img_size, Vector2(0, game_object.gap/2))
        self.sprite2 = Sprite(self.img_src_down, self.img_size, Vector2(0, (-game_object.gap / 2) - (self.img_size.y * game_object.transform.scale.y)))
        self.sprite1.set_size(self.img_size)
        self.sprite2.set_size(self.img_size)
        self.sprite1.load()
        self.sprite2.load()

    def unload(self):
        self.__setup()

    def render(self):
        Renderer.render_relative_sprite(self.sprite1, self.game_object.transform)
        Renderer.render_relative_sprite(self.sprite2, self.game_object.transform)

class Pipe(GameObject2):
    __slots__=["model", "__width", "manager", "gap"]
    def __init__(self, manager, gap=100, transform=Transform2(), priority=4, model=MdlPipe()):
        super().__init__( transform=transform, priority=priority)
        self.model = model
        self.gap = gap
        self.manager = manager
        self.__width = self.model.img_size.x * self.transform.scale.x

    def start(self):
        self.model.load(self)
        self.__width = self.model.img_size.x * self.transform.scale.x

    def stop(self):
        self.model.unload()
        self.__width = 0

    def update(self):
        self.transform.position.x -= FBEnvironment.move_speed * get_engine().delta_time
        if self.transform.position.x < -self.get_width() + self.manager.pos_x:
            self.manager.push_back(self)

    def get_width(self):
        return self.__width

    def render(self):
        self.model.render()

class PipesManager(GameObject2):
    __slots__=["pipes",
               "fb_scene", 
               "pipe_scale", 
               "min_height",
               "gap",
               "space_beetwen_pipes",
               "game_manager",
               "__max_dist_pipe",
               "pos_x"]
    def __init__(self, fb_scene, pipes_nbr=4, gap=175, space_beetwen_pipes=400, pipe_scale=Vector2(1, 1), transform=Transform2(), priority=8):
        super().__init__(transform, priority=priority)
        self.fb_scene = fb_scene
        self.pipe_scale = pipe_scale
        self.pipes = []
        self.gap = gap
        self.space_beetwen_pipes = space_beetwen_pipes
        self.min_height = 0
        self.game_manager = None
        width = get_engine().WIDTH * FBEnvironment.render_part
        self.pos_x = get_engine().WIDTH - width
        for i in range(pipes_nbr):
            pipe = Pipe(self, self.gap, Transform2(Vector2(), self.pipe_scale.copy()), self.priority, MdlPipe())
            self.pipes.append(pipe)
            self.fb_scene.add_render_object(pipe)

    def get_random_height(self, pipe):
        return (random.random() * (get_engine().HEIGHT - pipe.gap - self.min_height)) + self.min_height + (pipe.gap / 2)

    def get_min_max_height(self, pipe):
        return Vector2(self.min_height + (pipe.gap / 2), get_engine().HEIGHT - pipe.gap)

    def get_max_dist_pipe(self):
        return self.__max_dist_pipe

    def setup(self):
        for i, pipe in enumerate(self.pipes):
            pipe.transform.position = Vector2((i * self.space_beetwen_pipes) + self.space_beetwen_pipes + (get_engine().WIDTH / 2) + self.pos_x, self.get_random_height(pipe))

    def start(self):
        self.min_height = self.game_manager.get_min_height()
        self.__max_dist_pipe = self.space_beetwen_pipes + (get_engine().WIDTH / 2)
        self.setup()

    def get_closest_pipe(self):
        for pipe in self.pipes:
            if pipe.transform.position.x + pipe.get_width() > self.pos_x:
                return pipe

    def push_back(self, pipe):
        """ pushes the first base of the bases to the end """
        self.pipes[0].transform.position.x = self.pipes[-1].transform.position.x + self.space_beetwen_pipes
        self.pipes[0].transform.position.y = self.get_random_height(self.pipes[0])
        self.pipes.append(self.pipes.pop(0))