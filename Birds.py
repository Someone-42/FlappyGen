import Renderer
from Core import *
from RendererCore import *
from Environments import FBEnvironment
import graphics
import math
import random
from NeuralNetwork import *
from Matrix import *

BIRD_TEXTURES = ["assets/redbird-midflap.png",
                 "assets/yellowbird-midflap.png", 
                 "assets/bluebird-midflap.png"
                ]

class MdlBird(Model):
    __slots__ = ["img_src",
                 "img_size",
                 "sprite",
                 "game_object",
                 "rect"]

    def __init__(self):
        self.img_src = BIRD_TEXTURES[random.randint(0, len(BIRD_TEXTURES) - 1)]
        self.game_object = None
        self.__setup()

    def __setup(self):
        self.img_size = Vector2(int(34), int(24))
        self.sprite = Sprite(self.img_src, self.img_size, Vector2())
        self.rect = Rectangle2(Vector2(), self.img_size)

    def load(self, game_object):
        self.game_object = game_object
        self.rect.color = self.game_object.get_color()
        self.img_size = self.img_size
        self.sprite.load()

    def unload(self):
        self.__setup()

    def render(self):
        Renderer.render_relative_sprite(
            self.sprite, self.game_object.transform)
        Renderer.render_relative_rect(
            self.rect, self.game_object.transform, fill_mode=FillMode.OUTLINE, width=6)


class Bird(GameObject2):
    __slots__ = ["model",
                 "jump_height", 
                 "y_velocity",
                 "last_jump_time",
                 "__size",
                 "manager",
                 "brain",
                 "behave",
                 "score",
                 "dead"]

    def __init__(self, manager, jump_height=80, human_player=False, transform=Transform2(), model=MdlBird(), priority=10):
        self.jump_height = jump_height
        self.y_velocity = 0
        self.last_jump_time = 0
        self.model = model
        self.score = 0
        self.__size = Vector2()
        self.manager = manager
        self.brain = NeuralNetwork(4, 1)
        self.behave = self.behave_AI
        self.dead = False
        if human_player:
            self.behave = self.behave_human
            #self.model.img_src = BIRD_TEXTURES[0]
        super().__init__(transform, priority)

    def start(self):
        self.y_velocity = 0
        self.score = 0
        self.transform.position.y = get_engine().HEIGHT/2
        self.__size = self.model.img_size.mul_comp(self.transform.scale)
        self.model.load(self)
        self.dead = False

    def jump(self):
        if get_engine().get_time() - self.last_jump_time <= FBEnvironment.jump_delay:
            return
        self.last_jump_time = get_engine().get_time()
        self.y_velocity = math.sqrt(
            self.jump_height * -2 * FBEnvironment.gravity)

    def behave_human(self):
        if graphics.touche_enfoncee("K_SPACE"):
            self.jump()

    def check_collision(self):
        # En dessous
        if self.transform.position.y < self.manager.base_manager.get_height():
            self.manager.kill(self)
            return

        # Au dessus
        if self.transform.position.y > get_engine().HEIGHT:
            self.manager.kill(self)
            return

        if not self.manager.in_pipe:
            return

        y_bottom_bird = self.transform.position.y
        y_bottom_pipe = self.manager.next_pipe.transform.position.y - \
            (self.manager.next_pipe.gap / 2)

        bird_in_bottom = y_bottom_bird < y_bottom_pipe

        y_top_bird = self.transform.position.y + self.get_size_y()
        y_top_pipe = self.manager.next_pipe.transform.position.y + \
            (self.manager.next_pipe.gap / 2)

        bird_in_top = y_top_bird > y_top_pipe

        if bird_in_bottom or bird_in_top:

            bird_pos_y = self.transform.position.y + (self.get_size_y() // 2)
            pipe_pos_y = self.manager.next_pipe.transform.position.y

            dist_bird_pipe = abs(bird_pos_y - pipe_pos_y)

            max_dist = abs(
                self.manager.base_manager.get_height() - get_engine().HEIGHT)

            dist_bird_pipe = toRange(dist_bird_pipe, 0, max_dist, 100, 0)

            self.score += dist_bird_pipe
            self.manager.kill(self)

    def behave_AI(self):
        if self.manager.next_pipe == None:
            return

        # Distance au prochain Pipe
        a = toRange(abs(self.transform.position.x - self.manager.next_pipe.transform.position.x),
                    0, self.manager.pipe_manager.get_max_dist_pipe(), 0, 1)
        # Hauteur du Pipe
        b = toRange(self.manager.next_pipe.transform.position.y, self.manager.pipe_manager.get_min_max_height(
            self.manager.next_pipe).x, self.manager.pipe_manager.get_min_max_height(self.manager.next_pipe).y, 0, 1)
        # Position en Y
        c = toRange(self.transform.position.y,
                    self.manager.base_manager.get_height(), get_engine().HEIGHT, 0, 1)
        # Velocité en Y
        d = toRange(self.y_velocity, FBEnvironment.min_velocity,
                    math.sqrt(-2*FBEnvironment.gravity*self.jump_height), 0, 1)
        inputs = Matrix.from_array_light([
            [a],
            [b],
            [c],
            [d],
        ])

        if self.brain.predict(inputs).data[0][0] >= 1:
            self.jump()

    def update(self):
        if self.dead:
            return
        if self.y_velocity < FBEnvironment.min_velocity:
            self.y_velocity = FBEnvironment.min_velocity
        self.behave()
        self.y_velocity += FBEnvironment.gravity * get_engine().delta_time
        self.transform.position.y += self.y_velocity * get_engine().delta_time
        self.check_collision()
        self.score += get_engine().delta_time * 100

    def get_color(self):
        # On récupère les composants de la couleur via les poids du cerveau
        r = sum(self.brain.poids_input_output.data[0][:2])
        g = sum(self.brain.poids_input_output.data[0][2:])
        b = self.brain.biais_output.data[0][0]

        # On convertit les valeurs que l'on pense être entre -10 et 10
        # dans dans des valeurs de 0 à 255
        def converter(c):
            return int(toRange(c, -5, 5, 0, 255))
        r = converter(r)
        g = converter(g)
        b = converter(b)

        # print(r, g, b)

        return Color(r, g, b)

    def render(self):
        self.model.render()

    def stop(self):
        self.model.unload()

    def get_width(self):
        """ Returns the width of the bird (x size of the sprite) """
        return self.__size.x

    def get_size_y(self):
        """ Returns the size.y of the bird (y size of the sprite) """
        return self.__size.y