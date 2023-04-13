from SnakeEngine2 import *
from Core import *
from Background import Background, MdlBackground
from Tester import *
from Base import BaseManager
from Birds import *
from Pipes import *
from GameManagers import *
from FlappyBirdUI import *
from MainMenuUI import MMUI

# Aspect ratio recommandé : 9/8, resolution native : W900 H800

# Creation de l'engine
engine = SnakeEngine(WIDTH=1000, HEIGHT=750, TITLE="Flappy-gen (FlappyBird Neuroevolution)", 
                      CLEAR_COLOR=Color(0, 0, 0), do_fps_r_cap=True, FPS_R_CAP=24, do_fps_cap=False, do_multi_thread_rendering=False)

# Creation des scènes
fb_scene = Scene() # FlappyBirdScene
mm_scene = Scene() # MainMenuScene : Menu principal

## Creation des game_objects ##
#cam_mover = CameraMover(500) # ---Debug---

#Main Menu
mm_manager = MMManager(mm_scene=mm_scene, fb_scene=fb_scene)
mm_ui = MMUI(manager=mm_manager)

#Flappy bird
background = Background(model=MdlBackground(), priority=0)
base_manager = BaseManager(fb_scene, base_scale=Vector2(1.5, 1.5), priority=4, y_pos=0)
pipe_manager = PipesManager(fb_scene, pipes_nbr=2, gap=150, space_beetwen_pipes=442, pipe_scale=Vector2(1.5, 1.5), transform=Transform2(Vector2(), Vector2(1, 1)), priority=2)
fb_manager = FBManager(fb_scene, mm_scene, pipe_manager, base_manager, total_birds=42)
fb_UI = FBUI(fb_manager)

## Ajouts des game_objects a la scène ##

#Main Menu
#mm_scene.add_game_object(cam_mover) # ---Debug---
mm_scene.add_game_object(mm_manager)
mm_scene.add_render_object(mm_ui)

#Flappy bird
fb_scene.add_render_object(background)
fb_scene.add_game_object(base_manager)
fb_scene.add_game_object(pipe_manager)
fb_scene.add_game_object(fb_manager)
fb_scene.add_render_object(fb_UI)
#fb_scene.add_game_object(cam_mover) # ---Debug---

# Lancement de l'engine
engine.load_scene(mm_scene)
engine.run()