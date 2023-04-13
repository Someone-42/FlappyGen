import math
from enum import Enum

__ENGINE = None # Acts as a static reference of the engine

def get_engine():
    """ Returns the current instance of the engine running """
    return __ENGINE

def set_engine(engine):
    """ Sets the current instance of the engine running """
    global __ENGINE
    __ENGINE = engine
        
def clamp(value, min_value, max_value):
    """ Returns 'value' between 'min_value' and 'max_value'"""
    return min(max(min_value, value), max_value)

def degrees_to_radians(degrees):
    """ /!\ Deprecated method (will be removed) /!\ Takes a value 'degrees' in degrees and returns it converted to radians """
    return math.pi / 180 * degrees

def radians_to_degrees(radians):
    """ /!\ Deprecated method (will be removed) /!\ Takes a value 'radians' in radians and returns it converted to degrees """
    return 180 / math.pi * radians

def copy_2D_list(l):
    """ Copies the 2d list l (very fast (600+ times faster than copy.deepcopy)) """
    s = len(l)
    return [l[i][:] for i in range(s)]

class FillMode(Enum):
    """ FillMode is an Enum telling the renderer how to render the shapes OUTLINE will only draw the oultine of the shape, MESH will draw the Primitives used, and fill will draw the shape filled in"""
    OUTLINE=0
    MESH=1
    FILL=2

class Vector2:
    """Representation of a 2D vector"""
    __slots__=("x", "y")
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def magnitude(self):
        """Returns the length of the vector"""
        return math.sqrt((self.x*self.x) + (self.y*self.y))

    def squared_magnitude(self):
        """Returns the squared length of the vector, faster to compute"""
        return (self.x*self.x) + (self.y*self.y)

    def normalize(self):
        """Normalizes the vector to have its length equal to 1"""
        magn = self.magnitude()
        if magn == 0:
            magn = 1
        return Vector2(self.x / magn, self.y / magn)

    def __len__(self):
        return self.magnitude()

    def __abs__(self):
        return self.magnitude()
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self
    
    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def __str__(self):
        """Returns the Vector2 in a easier way to read string form"""
        return "x:"+str(self.x)+", y:"+str(self.y)

    def copy(self):
        """ Returns a copy of itself """
        return Vector2(self.x, self.y)

    def rotate(self, angle_radians):
        """ Rotates vectors using rotation matrices """
        return Vector2((math.cos(angle_radians) * self.x) - (self.y * math.sin(angle_radians)),
                       (math.sin(angle_radians) * self.x) + (self.y * math.cos(angle_radians)))

    def mul_comp(self, vector2):
        """ Multiplies each component of the vectors individually """
        return Vector2(self.x * vector2.x, self.y * vector2.y)
    
    def div_comp(self, vector2):
        """ Divides each component of the vectors individually """
        return Vector2(self.x / vector2.x, self.y / vector2.y)

    def min_comp(self):
        """ Returns the smallest component of the vector """
        return min(self.x, self.y)
    
    def max_comp(self):
        """ Returns the biggest component of the vector """
        return max(self.x, self.y)

    def flip_comp(self):
        """ Returns a flipped around version of the vector by switching its components """
        return Vector2(self.y, self.x)

    def sort_comp(self):
        """ Returns a new vector where x < y """
        return Vector2(self.min_comp(), self.max_comp())

    @staticmethod
    def scaler(n):
        """ Returns a vector with n as components : Vector2(n, n)"""
        return Vector2(1, 1) * n

    def abs_comp(self):
        """ Returns a vector with the absolute value of each comp """
        return Vector2(abs(self.x), abs(self.y))

    def squared_distance(self, point):
        """ Returns the squared distance to point : faster method because no calculation of the sqrt is needed """
        return (point.x - self.x) ** 2 + (point.y - self.y) ** 2

    def distance(self, point):
        """ Returns the distance to point"""
        return math.sqrt(self.squared_distance(point))

class Transform:
    """ Transform is a holder for the position, rotation, scale, and the parent game_object of a game_object"""
    __slots__=("position", "scale", "rotation", "parent")
    def __init__(self, position, scale, rotation, parent_game_object=None):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.parent = parent_game_object

    def __add__(self, other):
        return Transform(
            self.position + other.position,
            self.scale.mul_comp(other.scale),
            self.rotation + other.rotation,
            None
        )

class Transform2(Transform):
    """ A transform holding informations for 2D environment """
    __slots__=()
    def __init__(self, position=Vector2(), scale=Vector2(1, 1), rotation=0, parent_game_object=None):
        super().__init__(position, scale, rotation, parent_game_object)

    def sum_up(self):
        """ Gives an absolute transform wich has the position of itself and all it's parents added, same for position and rotation, has no parents"""
        ret_trans = Transform(self.position.copy(), self.scale.copy(), self.rotation, None)
        ret_parent = self.parent
        while not ret_parent == None:
            ret_trans = ret_trans + ret_parent.transform
            ret_parent = ret_parent.transform.parent
        return ret_trans

class Color:
    """ Simple color struct with, r=Red g=Green b=Blue a=Alpha"""
    __slots__=("r", "g" ,"b", "a")
    def __init__(self, r=128, g=128, b=128, a=255):
        self.r = 1 * int(clamp(r, 0, 255))
        self.g = int(clamp(g, 0, 255))
        self.b = int(clamp(b, 0, 255))
        self.a = int(clamp(a, 0, 255))

    def clamp_to_rgba_uint8(self):
        """ Clamps all the value to unsigned int 8bits (from 0 to 255) """
        self = Color.sttc_clamp_to_rgba_uint8(self)

    @staticmethod
    def sttc_clamp_to_rgba_uint8(color):
        """ Returns a Color() object with all the values clamped to unsigned int 8bits (from 0 to 255) """
        return Color(color.r, color.g, color.b, color.a)

    def __mul__(self, other):
        col = self.copy()
        col.r *= other
        col.g *= other
        col.b *= other
        return Color.sttc_clamp_to_rgba_uint8(col)

    def copy(self):
        """ Returns a copy of itself """
        return Color(self.r, self.g, self.b, self.a)

class Color01:
    """ Simple color struct with, r=Red g=Green b=Blue a=Alpha ranging from 0 to 1 (using floats), 
        Used with low level API like OpenGL, DirectX, etc... in fragment type shaders to do easier and faster maths/alpha blending/etc...,
        (faster than Color)""" # More operator overloading/functionalities will come with the OpenGL Renderer
    __slots__=("r", "g" ,"b", "a")
    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def clamp_to_rgba_ufloat_01(self):
        """ Clamps all the value to unsigned floats (ranging from 0 to 1) """
        self = Color01.sttc_clamp_to_rgba_uint8(self)

    @staticmethod
    def sttc_clamp_to_rgba_ufloat_01(color):
        """ Returns a Color01() object with all the values clamped to unsigned floats (ranging from 0 to 1) """
        return Color01(clamp(color.r, 0.0, 1.0), clamp(color.g, 0.0, 1.0), clamp(color.b, 0.0, 1.0), clamp(color.a, 0.0, 1.0))

    def __mul__(self, other):
        col = self.copy()
        col.r *= other
        col.g *= other
        col.b *= other
        return Color01.sttc_clamp_to_rgba_ufloat_01(col)
    
    def copy(self):
        """ Returns a copy of itself """
        return Color01.sttc_clamp_to_rgba_ufloat_01(self)

    def copy_fast():
        """ Returns a copy of the color without clamping all the values """
        return Color01(self.r, self.g, self.b, self.a)

class Rect:
    """ Simple rect struct, with the position and size """
    __slots__=("pos", "size")
    def __init__(self, pos=Vector2(), size=Vector2()):
        self.pos = pos
        self.size = size

    def copy(self):
        """ Returns a copy of itself """
        return Rect(self.pos.copy(), self.size.copy())

class GameObject:
    """ A GameObject is an entity with a transform, a reference to the engine it's in, and a priority over others (priority only for rendering)"""
    __slots__=("transform", "priority")
    def __init__(self, transform, priority=0):
        self.transform = transform
        self.priority = priority

    def awake(self):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def stop(self):
        pass

class GameObject2(GameObject):
    """ A GameObject made for 2D environments """
    __slots__=()
    def __init__(self, transform=Transform2(), priority=0):
        super().__init__(transform, priority)

class Primitive:
    """ Shape base for rendering """
    __slots__=("color")
    def __init__(self, color = Color()):
        self.color = color

class Triangle2(Primitive):
    """ 2D Triangle primitive """
    __slots__=("p1", "p2", "p3")
    def __init__(self, p1=Vector2(), p2=Vector2(), p3=Vector2(), color=Color()):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        super().__init__(color)

class Rectangle2(Primitive):
    """ 2D Rectangle primitive """
    __slots__=("pos", "size")
    def __init__(self, position=Vector2(), size=Vector2(), color=Color()):
        super().__init__(color)
        self.pos = position
        self.size = size

class Polygon2(Primitive):
    """ 2D Polygon primitive """
    __slots__=("points")
    def __init__(self, points=[], color=Color()):
        self.points = points
        super().__init__(color)
 
class Circle(Primitive):
    """ 2D Circle primitive """
    __slots__=("pos",
               "radius")
    def __init__(self, radius=42, pos=Vector2(0, 0), color=Color()):
        super().__init__(color=color)
        self.radius = radius
        self.pos = pos

class Model:
    """ 2D model, containing information for rendering of a specific object """
    __slots__=()

    def render(self):
        pass

def SS_to_SC(vector2):
    """ Takes a vector2 in ScreenSpace *2 and returns a vector2 in ScreenCoordinates *1 """
    return vector2.div_comp(get_engine().WINDOW_SIZE)

def SC_to_SS(vector2):
    """ Takes a vector2 in ScreenCoordinates *1 and returns a vector2 in ScreenSpace *2 """
    return vector2.mul_comp(get_engine().WINDOW_SIZE)

class TempMemory:
    """ Class to store temporarly vars, you might only store 1 var per object (in developpement to prevent this issue) """
    __slots__=("senders",
               "vars")
    def __init__(self):
        self.senders = []
        self.vars = {}

    def _get_id(self, sender):
        id = repr(sender)
        id = id.strip("<>")
        id_l = id.split(' ')
        id_l[0] = id_l[0].split('.')[1]
        id = id_l[0] + ':' + id_l[-1]
        return id

    def store_var(self, sender, var):
        self.senders.append(sender)
        self.vars[self._get_id(sender)] = var

    def get_var(self, sender):
        try:
            ret_var = self.vars[self._get_id(sender)]
            del self.vars[self._get_id(sender)]
        except ValueError as error:
            raise ValueError("ERROR : Couldn't access a variable that was never stored in TempMemoryBuffer")
        return ret_var

__TEMP_MEMORY = TempMemory()

def get_temp_memory():
    return __TEMP_MEMORY