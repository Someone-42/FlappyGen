from Core import *
import Renderer
import graphics
import time

def set_title():
    pass

def init():
    """Method called by the engine, /!\ Use is not recommended"""
    Renderer.init()

def start():
    """Method called by the engine, /!\ Use is not recommended"""
    Renderer.start()

def update():
    """Method called by the engine, /!\ Use is not recommended"""
    click = graphics.last_clic()
    if click == None:
        get_engine().last_click_pos = None
        return
    get_engine().last_click_pos = Vector2(click.x, click.y)

def pre_render():
    """Method called by the engine, /!\ Use is not recommended"""
    Renderer.pre_render()

def render():
    """Method called by the engine, /!\ Use is not recommended"""
    Renderer.render()


def stop():
    """Call this method when you want to stop the engine"""
    #add your actions there
    get_engine().stopped = True

def clean_up():
    """Method called by the engine, /!\ Use is not recommended"""
    Renderer.clean_up()
    Renderer.close()

# TODO : Fix timers/timer functions

class TimeWatch():
    "A stopwatch that allows to measure time in seconds easely"
    __slots__=("__start_time",
               "__running",
               "__total_time")

    def __init__(self):
        self.__start_time = 0
        self.__total_time = 0
        self.__running = False

    def stop(self):
        "Stops the TimeWatch"
        if not self.__running:
            return
        self.__total_time = time.perf_counter() - self.__start_time
        self.__running = False

    def start(self):
        "Starts the TimeWatch"
        if self.__running:
            return
        self.__start_time = time.perf_counter()
        self.__running = True

    def reset(self):
        "Resets the total time to 0"
        self.__start_time = time.perf_counter()
        self.__total_time = 0

    def read(self):
        "Returns the current time on the stopwatch in seconds"
        if not self.__running:
            return self.__total_time
        self.__total_time = time.perf_counter() - self.__start_time
        return self.__total_time