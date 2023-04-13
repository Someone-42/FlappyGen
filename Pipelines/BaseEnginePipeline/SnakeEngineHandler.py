from Core import *
import Renderer

def set_title():
    """Changes the current Title of the engine, the window if attached to a window"""
    pass

def init():
    """Method called by the engine, /!\ Use is not recommended"""
    Renderer.init()

def start():
    """Method called by the engine, /!\ Use is not recommended"""
    Renderer.start()

def update():
    """Method called by the engine, /!\ Use is not recommended"""
    pass

def pre_render():
    """Method called by the engine, /!\ Use is not recommended"""
    Renderer.clear()

def render():
    """Method called by the engine, /!\ Use is not recommended"""
    return Renderer.render()

def stop():
    """Call this method when you want to stop the engine"""
    #add your actions there
    CURRENT_ENGINE.stopped = True

def clean_up():
    """Method called by the engine, /!\ Use is not recommended"""
    Renderer.clean_up()
    for timer in get_timers():
        stop_timer(timer)
    Renderer.close()
    
def create_timer(timer_name):
    """Creates a new timer timer_name, doesn't start it"""
    #Add your code here

def start_timer(timer_name):
    """Starts a timer timer_name, if it doesn't exist it creates it"""
    #Add your code here
    pass

def read_timer(timer_name):
    """Returns the current value of the timer timer_name in seconds"""
    #Add your code here
    return 0

def stop_timer(timer_name):
    """Stops the timer timer_name"""
    #Add your code here
    pass

def get_timers():
    """Returns a list of timers names"""
    #Add your code here
    return []
