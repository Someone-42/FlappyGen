from Core import *
from Birds import *
from Genetics import generate_new_brains
from FsManager import save_birds, load_birds
from Environments import *


class FBManager(GameObject2):
    """ Game Manager for Flappy bird """
    __slots__ = ["pipe_manager",
                 "birds",
                 "base_manager",
                 "dead_birds",
                 "fb_scene",
                 "next_pipe",
                 "score",
                 "generation",
                 "in_pipe",
                 "dead_human_birds",
                 "mm_scene",
                 "is_loading",
                 "fb_ui",
                 "total_birds",
                 "pos_x",
                 "width_r",
                 "_game_paused"]

    def __init__(self, fb_scene, mm_scene, pipe_manager, base_manager, transform=Transform2(), priority=0, total_birds=50):
        super().__init__(transform=transform, priority=priority)
        self.pipe_manager = pipe_manager
        self.base_manager = base_manager
        self.birds = []
        self.dead_birds = []
        self.dead_human_birds = []
        self.fb_scene = fb_scene
        self.mm_scene = mm_scene
        self.next_pipe = None
        self.score = 0
        self.generation = -1
        self.in_pipe = False
        self.is_loading = False
        self.fb_ui = None
        self.total_birds = total_birds
        width = get_engine().WIDTH * FBEnvironment.render_part
        self.width_r = width
        self.pos_x = get_engine().WIDTH - width
        self._game_paused = False

    def awake(self):
        if self.is_loading == True:
            return

        self.generation += 1
        self.pipe_manager.game_manager = self
        if not self.generation == 0:
            self.birds = []
            brains = generate_new_brains(self.dead_birds, self.score)
            for i, bird in enumerate(self.dead_birds):
                bird.brain = brains[i]
                self.birds.append(bird)
            self.dead_birds = []
            for bird in self.dead_human_birds:
                self.birds.append(bird)
            self.dead_human_birds = []
        else:
            self.generate_birds(self.total_birds)
        for bird in self.birds:
            self.fb_scene.add_render_object(bird)
        get_engine().CLEAR_COLOR = Color(100, 210, 255)

    def start(self):
        self.score = 0
        self.fb_ui.info_labels[0].text = self.fb_ui.info_labels_base_text[0] + str(self.score)
        self.fb_ui.info_labels[2].text = self.fb_ui.info_labels_base_text[2] + str(self.generation)
        self.fb_ui.update_bird_count()

    def generate_birds(self, number):
        for _ in range(number):
            self.birds.append(Bird(self, 80, False, Transform2(
                Vector2(self.pos_x + self.width_r / 4, 0), Vector2(1.5, 1.5)), MdlBird(), 10))
        #self.birds.append(Bird(self, 80, True, Transform2(Vector2(self.pos_x + self.width_r / 4, 0), Vector2(1.5, 1.5)), MdlBird(), 10))

    def get_min_height(self):
        """ Returns the minimum height at which the pipes can generate """
        return self.base_manager.get_height()

    def kill_birds(self):
        for bird in self.birds:
            self.dead_birds.append(bird)
        self.birds = []

    def stop(self):
        self.kill_birds()

    def kill(self, bird):
        if self.is_loading == True:
            return

        self.fb_scene.disable_object_rendering(bird)
        self.birds.remove(bird)
        bird.dead = True
        if bird.behave == bird.behave_human:
            self.dead_human_birds.append(bird)
        else:
            self.dead_birds.append(bird)
        self.fb_ui.update_bird_count()

    def get_non_human_birds(self, bird_list):
        """ Retourne une liste contenant tous les oiseaux non-humains depuis bird_list """
        list_r = bird_list[:]
        for bird in bird_list:
            if bird.behave == bird.behave_human:
                list_r.remove(bird)
        return list_r

    def update(self):
        if self.is_loading == True:
            return

        if len(self.birds) == 0:
            get_engine().reload_scene()
        pipe = self.pipe_manager.get_closest_pipe()
        if pipe != self.next_pipe and self.next_pipe != None:
            self.score += 1
            self.fb_ui.info_labels[0].text = self.fb_ui.info_labels_base_text[0] + str(self.score)
        self.next_pipe = pipe
        self.in_pipe = (self.birds[0].get_width() + self.birds[0].transform.position.x > pipe.transform.position.x) and (self.birds[0].transform.position.x < pipe.transform.position.x + pipe.get_width())

    def quit(self, btn, click):
        """ Called when the player wants to exit the game """
        get_engine().load_scene(self.mm_scene)

    def save(self, btn, click):
        """ Called when the player wants to save the game """
        birds_to_save = self.get_non_human_birds(self.dead_birds + self.birds)
        save_birds(birds_to_save, self.generation)

    def remove_birds(self):
        self.kill_birds()
        for bird in self.dead_birds + self.dead_human_birds:
            self.fb_scene.remove_game_object(bird)
        self.dead_birds = []
        self.dead_human_birds = []

    def load(self, file_name):
        """ Called when the player wants to load saved brains into the birds """
        loaded_birds = load_birds(file_name)
        self.generation = loaded_birds["generation_number"]
        self.remove_birds()
        self.generate_birds(len(loaded_birds["brains"]))
        for i, bird in enumerate(self.birds):
            bird.brain = loaded_birds["brains"][i]
        get_engine().reload_scene()
        
    def pause_game(self):
        self._game_paused = True
        get_temp_memory().store_var(self, get_engine().time_scale) # Stockage de time_scale temporairement pour la reprendre quand le jeu est repris
        get_engine().time_scale = 0

    def resume_game(self):
        self._game_paused = False
        get_engine().time_scale = get_temp_memory().get_var(self)

    def restart_game(self, btn, click):
        """ Called when the player clics on the restart button """
        self.remove_birds()
        self.generate_birds(self.total_birds)
        self.generation = -1
        get_engine().reload_scene()

    def change_speed(self, slider, click):
        """ Changes the speed at which the world moves """
        FBEnvironment.set_move_speed(slider.value)

    def change_scale(self, slider, click):
        """ Called when the player changes the scale via the slider """
        get_engine().time_scale = slider.value


class MMManager(GameObject2):
    __slots__ = ["fb_scene",
                 "mm_scene"]

    def __init__(self, mm_scene, fb_scene, transform=Transform2(), priority=0):
        super().__init__(transform=transform, priority=priority)
        self.fb_scene = fb_scene
        self.mm_scene = mm_scene

    def awake(self):
        get_engine().CLEAR_COLOR = get_colors("darkest")

    def play(self, btn, click):
        get_engine().load_scene(self.fb_scene)

    def quit(self, btn, click):
        get_engine().stop()
