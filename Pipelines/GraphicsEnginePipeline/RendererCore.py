from Core import *
import graphics
import enum

def _Color_to_couleur(color):
    return graphics.couleur(color.r, color.g, color.b, color.a)

def _Vector2_to_point(vector2):
    return graphics.Point(int(vector2.x), int(vector2.y))

_image_previous_sizes = dict()

class SpriteFitMode(enum.Enum):
    FIT=0
    FILL=1
    STRETCH=2

class Sprite:
    """ The sprite class may still have issues, and or cause them """
    __slots__=("__size", #Dimensions in pixels
               "__prev_size", #previous size for rendering
               "__img_src",
               "partial",
               "_r_part",
               "__position",
               "_r_pos") #Path to the image and extension
    def __init__(self, img_src, size, position=Vector2(), partial=False, part=Rect()):
        self.__size = size
        self.__img_src = img_src
        global _image_previous_sizes
        _image_previous_sizes[img_src] = size.copy()
        self.__position = position
        self.set_partial_part(partial, part)

    def set_size(self, size):
        global _image_previous_sizes
        if self.__size.x == size.x and self.__size.y == size.y:
            return
        self.__size = size
        _image_previous_sizes[self.__img_src] = size.copy()
        graphics.modifie_taille_image(self.get_img_src(), int(self.__size.x), int(self.__size.y))

    def _set_sprite_size(self, size):
        global _image_previous_sizes
        """ Modifies the size of the image in memory without modifying the Sprite.__size component """
        if _image_previous_sizes[self.__img_src].x == size.x and _image_previous_sizes[self.__img_src].y == size.y:
            return
        _image_previous_sizes[self.__img_src] = size.copy()
        graphics.modifie_taille_image(self.get_img_src(), int(size.x), int(size.y))

    def get_size(self):
        return self.__size.copy()

    def set_img_src(self, path):
        self.__img_src = path
        global _image_previous_sizes
        _image_previous_sizes[self.__img_src] = self.get_size() + Vector2(42, -42) # changing it to force an update
        self._set_sprite_size(self.get_size())

    def get_img_src(self):
        return self.__img_src
    
    def set_position(self, position):
        self.__position = position
        self._r_pos = self.__position
        if self.partial:
            self._r_pos += self._r_part.pos

    def get_position(self):
        return self.__position.copy()

    def load(self):
        """ Call this function only when the engine is starting """
        graphics.modifie_taille_image(self.get_img_src(), int(self.__size.x), int(self.__size.y))

    def set_partial_part(self, partial=True, part=Rect()):
        self.partial = partial
        self.set_part(part)

    def set_part(self, part):
        self._r_part = Rect(_Vector2_to_point(part.pos), _Vector2_to_point(part.pos + part.size))
        self._r_pos = self.__position + part.pos

    def get_part(self):
        return self._r_part.copy()

    def set_to_fit_in_box(self, bounding_box=Rect(), sprite_fit_mode=SpriteFitMode.FIT):
        """
        Modifies the attributes of the sprite to make it fit (corresponding to the sprite_fit_mode) in the defined bounding box (changes positionning, scale, partial rendering, etc...)
        Returns a Rect() corresponding to the space in which the sprite will be rendered in Screen Space (or pixel space)
        """
        bounding_box_ret = bounding_box.copy()
        self.set_position(bounding_box.pos + Vector2.scaler(0.5))
        self.set_partial_part(False)
        if sprite_fit_mode == SpriteFitMode.STRETCH:
            self.set_size(bounding_box.size + Vector2.scaler(0.5))
        elif sprite_fit_mode == SpriteFitMode.FIT:
            scale = (bounding_box.size.div_comp(self.get_size())).min_comp()
            self.set_size(self.get_size() * scale)
            self.set_position(self.get_position() + (bounding_box.size - self.get_size()) / 2 + Vector2.scaler(0.5))
            bounding_box_ret.pos = self.get_position().copy()
            bounding_box_ret.size = self.get_size().copy()
        elif sprite_fit_mode == SpriteFitMode.FILL:
            scale = (bounding_box.size.div_comp(self.get_size())).max_comp()
            self.set_size(self.get_size() * scale)
            pos = (bounding_box.size - self.get_size()) / 2 #+ Vector2.scaler(0.5)
            self.set_position(self.get_position() + pos)
            self.set_partial_part(True, Rect(pos.abs_comp(), bounding_box.size.copy()))
        return bounding_box_ret