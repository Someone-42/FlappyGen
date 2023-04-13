from Core import *
import graphics

class CameraMover(GameObject2):
    __slots__=["speed"]
    def __init__(self, speed=100, transform=Transform2(), priority=0):
        super().__init__(transform, priority=priority)
        self.speed = speed

    def update(self):
        movement = Vector2(0, 0)
        del_speed = self.speed * get_engine().real_delta_time
        if graphics.touche_enfoncee("K_a"):
            movement.x -= del_speed
        if graphics.touche_enfoncee("K_w"):
            movement.y += del_speed
        if graphics.touche_enfoncee("K_s"):
            movement.y -= del_speed
        if graphics.touche_enfoncee("K_d"):
            movement.x += del_speed
        get_engine().main_camera.position += movement
        if not get_engine().real_delta_time:
            return
        print(1/get_engine().real_delta_time)