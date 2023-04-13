### Engine logic and Pipeline attributing
import sys
import configparser

sys.path.append("./Extensions")

config = configparser.ConfigParser()
config.read("SnakeEngine.ini")
engine = config["Engine"]["Engine"].lower()
engine_pipeline = config["Engine"]["EnginePipeline"].lower()

if engine == "universal" or engine == "default":
    sys.path.append("./Engine/Universal")

if engine_pipeline == "base" or engine_pipeline == "default":
    sys.path.append("./Pipelines/BaseEnginePipeline")
elif engine_pipeline == "graphics":
    sys.path.append("./Pipelines/GraphicsEnginePipeline")
elif engine_pipeline == "pygame":
    pass
elif engine_pipeline == "opengl":
    sys.path.append("./Pipelines/OpenGLEnginePipeline")

### End Engine logic and Pipeline attributing

from Core import *
import SnakeEngineHandler as Handler
import threading

class Scene:
    """ The container for game objects used by the engine to render and update objects """
    __slots__=("game_objects",
               "render_objects",
               "ui_objects",
               "uio_selected",
               "_started",
               "__game_inactive",
               "__render_inactive",
               "__ui_inactive",
               "__ui_bounding_boxes")
    def __init__(self):
        self.game_objects = []
        self.render_objects = []
        self.ui_objects = []
        self.__game_inactive = []
        self.__render_inactive = []
        self.__ui_inactive = []
        self.uio_selected = None

    def _insert_gobject_by_priority(self, game_object, list_go):
        """ Adds the object at the same level as other objects with the same priority, if already in the list doesn't read it """
        if game_object in list_go:
            return
        if not list_go:
            list_go.append(game_object)
        else:
            for i, ro in enumerate(list_go):
                if ro.priority >= game_object.priority:
                    list_go.insert(i, game_object)
                    break
                if i+1 == len(list_go):
                    list_go.append(game_object)
                    break

    def add_game_object(self, game_object):
        """ Adds a game object that will not have its render method called """
        if game_object in self.game_objects:
            return
        self.game_objects.append(game_object)
        if get_engine()._awoken:
            game_object.awake()
        if get_engine()._started:
            game_object.start()

    def add_render_object(self, game_object):
        """ Adds a game object to the engine, + to be rendered """
        self.add_game_object(game_object)
        self._insert_gobject_by_priority(game_object, self.render_objects)

    def add_ui_object(self, game_object):
        """ Adds a game object to the engine that is rendered, and is part of the UI """
        self._insert_gobject_by_priority(game_object, self.ui_objects)
        if get_engine()._awoken:
            game_object.awake()
        if get_engine()._started:
            game_object.start()
    
    def set_render_priority(self, game_object, priority):
        """ Sets the rendering priority of a game_object to priority and updates its position for rendering to be rendered at the correct moment """
        game_object.priority = priority
        self.remove_game_object(game_object)
        self.add_render_object(game_object)

    def set_ui_priority(self, game_object, priority):
        """ Sets the priority at which the UI object will be rendered and selected on click """
        game_object.priority = priority
        self.remove_game_object(game_object)
        self.add_ui_object(game_object)

    def remove_game_object(self, game_object):
        """ Removes a game object and all its rendering aliases from the scene and stops it """
        game_object.stop()
        if game_object in self.game_objects:
            self.game_objects.remove(game_object)
        if game_object in self.render_objects:
            self.render_objects.remove(game_object)
        if game_object in self.ui_objects:
            self.ui_objects.remove(game_object)

    def disable_object_rendering(self, game_object):
        """ Stops the rendering of a certain object, to enable the rendering again, call the method add_render_object(<your_game_object>) """
        if game_object not in self.render_objects:
            return
        self.render_objects.remove(game_object)

    def __set_active_game_object(self, game_object):
        """ Adds a game object that will not have its render method called """
        if game_object in self.game_objects:
            return
        self.game_objects.append(game_object)

    def __set_active_render_object(self, game_object):
        """ Adds a game object to the engine, + to be rendered """
        self.__set_active_game_object(game_object)
        self._insert_gobject_by_priority(game_object, self.render_objects)

    def __set_active_ui_object(self, game_object):
        self._insert_gobject_by_priority(game_object, self.ui_objects)

    def set_active(self, game_object, active):
        """ When deactivating an object it doesn't get updated or rendered """
        if active:
            if game_object in self.__ui_inactive:
                self.__set_active_ui_object(game_object)
                self.__ui_inactive.remove(game_object)
            elif game_object in self.__render_inactive:
                self.__set_active_render_object(game_object)
                self.__render_inactive.remove(game_object)
            elif game_object in self.__game_inactive:
                self.__set_active_game_object(game_object)
                self.__game_inactive.remove(game_object)
        else:
            if game_object in self.ui_objects:
                self.__ui_inactive.append(game_object)
                self.remove_game_object(game_object)
            elif game_object in self.render_objects:
                self.__render_inactive.append(game_object)
                self.remove_game_object(game_object)
            elif game_object in self.game_objects:
                self.__game_inactive.append(game_object)
                self.remove_game_object(game_object)

    def _set_all_active(self):
        for game_object in self.__game_inactive + self.__render_inactive + self.__ui_inactive:
            self.set_active(game_object, True)

    def _load(self):
        for go in self.game_objects:
            go.awake()
        for uio in self.ui_objects:
            uio.awake()

    def _start(self):
        for go in self.game_objects:
            go.start()
        for uio in self.ui_objects:
            uio.start()
        self._started = True

    def _select_ui_object(self, ui_object):
        if self.uio_selected != None and self.uio_selected != ui_object:
            self.uio_selected.on_deselect()
        ui_object.on_select(Vector2(-1, -1))
        self.uio_selected = ui_object

    def _deselect_current_ui_object(self):
        if self.uio_selected != None:
            uio = self.uio_selected
            self.uio_selected = None
            uio.on_deselect()

    def _check_click_ui_objects(self):
        if get_engine().last_click_pos == None:
            return
        old_uio = None
        clicked = False
        for uio in reversed(self.ui_objects):
            if uio.is_clickable and uio.check_click(get_engine().last_click_pos):
                clicked = True
                uio.on_select(get_engine().last_click_pos)
                if uio.is_selectable:
                    uio.selected = True
                    old_uio = self.uio_selected
                    if uio != old_uio:
                        self.uio_selected = uio
                    else:
                        self.uio_selected = None
                else:
                    if self.uio_selected != None:
                        uio_selected = self.uio_selected
                        self.uio_selected = None
                        uio_selected.on_deselect()
                get_engine().last_click_pos = None
                break
        if not clicked:
            if self.uio_selected != None:
                self.uio_selected.on_deselect()
                self.uio_selected = None
        if old_uio != None:
            old_uio.on_deselect()
            
    def _update(self):
        for go in self.game_objects:
           go.update()
        self._check_click_ui_objects()
        if self.uio_selected != None:
            self.uio_selected.update()

    def _render(self):
        for ro in self.render_objects:
            ro.render()
        for uio in self.ui_objects:
            uio.render()

    def _unload(self):
        self._started = False
        for go in self.game_objects:
            go.stop()
        for uio in self.ui_objects:
            uio.stop()

class _Input:
    pass

class __SnakeEngine:
    """ Representation of the Engine """
    __slots__=("WIDTH", 
               "HEIGHT", 
               "CLEAR_COLOR", 
               "TITLE", 
               "VERSION", 
               "stopped", 
               "_started",
               "_awoken",
               "scene",
               "last_click_pos",
               "current_scene_index",
               "time_watch", 
               "view_port", 
               "main_camera",
               "__DEFAULT_SCENE",
               "do_multi_thread_rendering",
               "CRNT_THREAD",
               "delta_time",
               "render_delta_time",
               "real_delta_time",
               "time_scale",
               "WINDOW_SIZE",
               "input",
               "__FPS_R_CAP",
               "__do_fps_r_cap",
               "__render_delay",
               "__current_render_delay",
               "__FPS_CAP",
               "__do_fps_cap",
               "__update_delay",
               "__current_update_delay")
    def __init__(self, WIDTH=1200, HEIGHT=800, CLEAR_COLOR=Color(7, 13, 0), TITLE="Untitled", do_multi_thread_rendering=False, set_as_default_engine=True, do_fps_r_cap=False, FPS_R_CAP=64, do_fps_cap=False, FPS_CAP=600):
        """ Engine class /!\ WARNING DO NOT USE mutithread rendering AND do fps render cap AT THE SAME TIME """
        if set_as_default_engine:
            set_engine(self)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.CLEAR_COLOR = CLEAR_COLOR
        self.VERSION = "2.9.15.0"
        self.set_title(TITLE)
        self.stopped = False
        self.view_port = None
        if self.view_port == None:
            self.view_port = Rect(Vector2(0, 0), Vector2(WIDTH, HEIGHT))
        self._started = False
        self._awoken = False
        self.main_camera = None
        Handler.init()
        self.time_watch = Handler.TimeWatch()
        self.__DEFAULT_SCENE = Scene()
        self.scene = self.__DEFAULT_SCENE
        self.last_click_pos = None # Vector2 if clicked somewhere
        self.do_multi_thread_rendering = do_multi_thread_rendering
        self.CRNT_THREAD = None #Current thread for rendering
        self.render_delta_time = 0 #Delta time in the rendering thread
        self.real_delta_time = 0
        self.delta_time = 0
        self.time_scale = 1
        self.WINDOW_SIZE = Vector2(WIDTH, HEIGHT)
        # Due to the timers being precise to only the millisecond, the FPS caps will not be precise e.g.:
        #   imagine setting the cap to 700 FPS -> the delay between each frame would need to be 1 / 700 * 1000 ms, which means ~1.4286 ms :
        #   the engine will then need to wait for >= ~1.4286 between each updates so the max precision will be 2 ms beetwen each frame which is 500 FPS
        self.__FPS_R_CAP = FPS_R_CAP
        self.__do_fps_r_cap = do_fps_r_cap
        self.__render_delay = 1 / self.__FPS_R_CAP # Time in seconds to wait for each frame to be rendered
        self.__current_render_delay = 0
        self.__FPS_CAP = FPS_CAP
        self.__do_fps_cap = do_fps_cap
        self.__update_delay = 1 / self.__FPS_CAP
        self.__current_update_delay = 0

    def get_time(self):
        """ Returns the time in seconds since the start of the engine """
        return self.time_watch.read()

    def set_title(self, title):
        """ Sets the title of the engine """
        self.TITLE = "Snake Engine - " + self.VERSION + " : " + title
        Handler.set_title()

    def reload_scene(self):
        """ Reloads the current scene """
        scene = self.scene
        self.unload_scene()
        self.load_scene(scene)

    def load_scene(self, scene):
        """ Loads the scene, unloads the currently loaded one """
        if scene == self.scene or scene == self.__DEFAULT_SCENE:
            return
        if not (self.scene == self.__DEFAULT_SCENE):
            self.scene._unload()
        self.scene = scene
        if self._awoken:
            self.scene._load()
        if self._started:
            self.scene._start()

    def unload_scene(self):
        """ Unloads the current scene """
        self.scene._unload()
        self.scene = self.__DEFAULT_SCENE

    def _start(self):
        """ Starts the engine, /!\ use with caution """
        Handler.start()
        self._started = True
        self.scene._start()
        self.time_watch.start()

    def _update(self):
       """ Updates the engine taking the time elapsed since the last frame/update, /!\ use with caution """
       Handler.update()
       self.scene._update()

    def _render(self):
        """ Renders all the render objects of the engine and itself, /!\ use with caution """
        Handler.pre_render()
        self.scene._render()
        return Handler.render()

    def stop(self):
        """ Stops the engine """
        Handler.clean_up()
        self.stopped = True
        self._started = False
        self._awoken = False
        self.scene._unload()

    def __awake(self):
        self._awoken = True
        self.scene._load()
        
    def __f_render_thread(self):        
        r_old_time = 0
        r_new_time = 0
        temp_delta_time = 0
        delta_time = 0
        self.render_delta_time = 0
        while not self.stopped:
            r_new_time = self.time_watch.read()
            delta_time = r_new_time - r_old_time
            temp_delta_time += delta_time
            r_old_time = r_new_time
            if self.scene._started:
                if self.__do_fps_r_cap:
                    self.__current_render_delay -= delta_time
                    if self.__current_render_delay <= 0:
                        self.render_delta_time = temp_delta_time
                        temp_delta_time = 0
                        self.__current_render_delay = self.__render_delay
                        self._render()

    def run(self):
        """ Call this method to run the main loop, nothing shall be done after that method """
        self.__awake()
        self._start()
        #setting up vars
        old_time = 0
        new_time = 0
        delta_time = 0
        r_old_time = 0
        r_new_time = 0
        r_delta_time = 0
        udelta_time = 0
        if self.do_multi_thread_rendering:
            self.CRNT_THREAD = threading.Thread(target=self.__f_render_thread)
            self.CRNT_THREAD.start()
        #Main loop
        #self.stopped: break
        while True:
            new_time = self.time_watch.read()
            delta_time = new_time - old_time
            old_time = new_time
            if self.__do_fps_cap:
                self.__current_update_delay -= delta_time
                if self.__current_update_delay <= 0:
                    udelta_time = self.__update_delay - self.__current_update_delay
                    self.real_delta_time = udelta_time
                    self.delta_time = udelta_time * self.time_scale
                    self.__current_update_delay = self.__update_delay
                    self._update()
            else:
                self.real_delta_time = delta_time
                self.delta_time = delta_time * self.time_scale
                self._update()
            if self.stopped:
                break
            if self.do_multi_thread_rendering:
                continue
            elif self.__do_fps_r_cap:
                r_new_time = self.time_watch.read()
                r_delta_time = r_new_time - r_old_time
                r_old_time = r_new_time
                self.__current_render_delay -= r_delta_time
                if self.__current_render_delay <= 0:
                    self.render_delta_time = self.__render_delay - self.__current_render_delay
                    self.__current_render_delay = self.__render_delay
                    self._render()
            else:
                self.render_delta_time = delta_time
                self._render()

    #FPS R
    def get_FPS_R_CAP(self):
        return self.__FPS_R_CAP

    def get_do_fps_r_cap(self):
        return self.__do_fps_r_cap

    def set_do_fps_r_cap(self, active):
        self.__do_fps_r_cap = active

    def set_FPS_R_CAP(self, FPS_R_CAP=64):
        self.__FPS_R_CAP = FPS_R_CAP
        self.__render_delay = 1 / self.__FPS_R_CAP
        self.__current_render_delay = 0 # resetting for immediate change

    #FPS
    def get_FPS_CAP(self):
        return self.__FPS_CAP

    def get_do_fps_cap(self):
        return self.__do_fps_cap

    def set_do_fps_cap(self, active):
        self.__do_fps_cap = active

    def set_FPS_CAP(self, FPS_CAP=600):
        self.__FPS_CAP = FPS_CAP
        self.__update_delay = 1 / self.__FPS_CAP
        self.__current_update_delay = 0 # resetting for immediate change

SnakeEngine = __SnakeEngine

if engine_pipeline == "graphics":
    import SnakeEngineG
    SnakeEngine = SnakeEngineG._SnakeEngineG