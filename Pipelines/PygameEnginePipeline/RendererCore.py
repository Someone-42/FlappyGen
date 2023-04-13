from Core import *

class SpriteFitMode(enum.Enum):
    FIT=0
    FILL=1
    STRETCH=2

class Sprite(Primitive):
    __slots__=["__size", #Dimensions in pixels
               "__img_src",
               "partial",
               "part",
               "__position"] #Path to the image and extension
    def __init__(self, img_src, size, position=Vector2(), partial=False, part=Rect()):
        super().__init__(Color(0, 0, 0))
        self.set_img_src(img_src)
        self.set_size(size)
        self.__position = position
        self.partial = partial
        self.part = part

    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size

    def set_img_src(self, path):
        self.__img_src = path

    def get_img_src(self):
        return self.__img_src

    def set_partial_part(self, partial=True, part=Rect()):
        self.partial = partial
        self.part = part

    def set_position(self, position):
        self.__position = position

    def get_position(self):
        return self.__position.copy()

    def set_part(self, part):
        self.part = part

    def get_part(self):
        return self.part.copy()

    def set_to_fit_in_box(self, bounding_box=Rect(), sprite_fit_mode=SpriteFitMode.FIT):
        """
        Modifies the attributes of the sprite to make it fit (corresponding to the sprite_fit_mode) in the defined bounding box (changes positionning, scale, partial rendering, etc...)
        Returns a Rect() corresponding to the space in which the sprite will be rendered in Screen Space (or pixel space)
        """
        #Add code here
        pass