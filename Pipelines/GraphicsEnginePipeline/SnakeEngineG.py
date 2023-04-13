from SnakeEngine2 import *
import SnakeEngineHandler as Handler

class _SnakeEngineG(SnakeEngine):
    __slots__=("G_VERSION")

    def __init__(self, WIDTH=1200, HEIGHT=800, CLEAR_COLOR=Color(7, 13, 0), TITLE='Untitled', do_multi_thread_rendering=False, set_as_default_engine=True, do_fps_r_cap=False, FPS_R_CAP=64, do_fps_cap=False, FPS_CAP=600):
        self.G_VERSION = "6.4.2"
        # The graphics RendererCore is in preview, sprite rendering may be bugged or cause bugs
        super().__init__(WIDTH=WIDTH, HEIGHT=HEIGHT, CLEAR_COLOR=CLEAR_COLOR, TITLE=TITLE, do_multi_thread_rendering=do_multi_thread_rendering, set_as_default_engine=set_as_default_engine, do_fps_r_cap=do_fps_r_cap, FPS_R_CAP=FPS_R_CAP, do_fps_cap=do_fps_cap, FPS_CAP=FPS_CAP)
        self.main_camera = Transform2()

    def set_title(self, title):
        self.TITLE = "Snake Engine "+self.VERSION+" - Gfx "+self.G_VERSION + " : " + title
        Handler.set_title()