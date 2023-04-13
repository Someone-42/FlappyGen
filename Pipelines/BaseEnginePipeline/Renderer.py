from Core import *

"""

HELP PANEL :
*1 : in screen coordinates/coords = when a Vector2 is set between Vector2(0, 0) and Vector2(1, 1) where Vector2(1, 1) => SnakeEngine.WINDOW_SIZE # This is mostly used for UI
*2 : in screen space = when a Vector2 is set between Vector2(0, 0) and Vector2(SnakeEngine.WIDTH, SnakeEngine.HEIGHT)

"""

DEFAULT_FONT = None

def init():
    pass

def start():
    pass

def clear():
    pass

def render():
    return None

def clean_up():
    clear()

def close():
    pass
    
########################################################
#                      UI Getters                      #
########################################################
def get_text_size(text, font_size, font=DEFAULT_FONT):
    """ Return a vector 2 giving the width and the height of the text"""
    # Add your code here
    return Vector2()

def get_optimal_font_size(text, size, font=DEFAULT_FONT):
    """ Returns the optimal font size for a text and a size to ~fit in (in screen coords *1) """
    txt_size = get_text_size(text, 42, font)
    v_ratio = txt_size / 42
    v_opt = size.div_comp(v_ratio)
    return int(min(v_opt.x, v_opt.y))

########################################################
#                 Primitives Rendering                 #
########################################################

#Triangles

def render_tri(triangle, fill_mode=FillMode.FILL, width=1):
    """ Renders a triangle to the screen in px coordinates relative to Screen Space, width optional (Mesh and Outline) """
    #Add your code here
    pass
    
def render_trans_tri(triangle, transform, fill_mode=FillMode.FILL, width = 1):
    """ Renders a triangle to the screen in px coordinates relative to Screen Space and the transform given, width optional (Mesh and Outline) """
    #Add your code here
    pass

def render_relative_tri(triangle, transform, fill_mode=FillMode.FILL, width=1):
    """ Renders a triangle to the screen with coordinates relative to World Space with the game_object's transform, width optional (Mesh and Outline) """
    #Add your code here
    pass

#End Triangles
########################################################
#Polygons

def render_poly(polygon, fill_mode=FillMode.FILL, width=1):
    """ Renders a polygon with its array of points, the coordinates are evaluated in screen space in px, width optional"""
    #Add your code here
    pass
    
def render_trans_poly(polygon, transform, fill_mode=FillMode.FILL, width=1):
    """ Renders a polygon to the screen in px coordinates relative to Screen Space and the transform given, width optional (Mesh and Outline) """
    #Add your code here
    pass

def render_relative_poly(polygon, transform, fill_mode=FillMode.FILL, width=1):
    """ Renders a polygon to the screen in px coordinates relative to World Space and the game object's transform given, width optional (Mesh and Outline) """
    #Add your code here
    pass

#End Polygons
########################################################
#Rects
def render_rect(rect, fill_mode=FillMode.FILL, width=1):
    """ Renders a quad to the screen in px coordinates relative to Screen Space, width optional (Mesh and Outline) """
    #Add your code here
    pass
        
def render_trans_rect(rect, transform, fill_mode=FillMode.FILL, width = 1):
    """ Renders a quad to the screen in px coordinates relative to Screen Space and the transform given, width optional (Mesh and Outline) """
    #Add your code here
    pass

def render_relative_rect(rect, transform, fill_mode=FillMode.FILL, width=1):
    """ Renders a quad to the screen with coordinates relative to World Space with the game_object's transform, width optional (Mesh and Outline) """
    #Add your code here
    pass

#End Quads
########################################################
#Sprites

def render_sprite(sprite):
    """ Renders a Sprite to the screen, with the position relative to screen_space """
    #Add your code here
    pass

def render_trans_sprite(sprite, transform):
    """ Renders a Sprite to the screen, relative to screen space, doesn't support rotation """
    #Add your code here
    pass

def render_relative_sprite(sprite, transform):
    """ Renders a Sprite to the screen, relative to world space, doesn't support rotation """
    #Add your code here
    pass

#End Sprites
########################################################
#Text

def render_text(text, font_size, font_color, pos, font=DEFAULT_FONT):
    """ Renders text to the screen, with the position relative to screen_space """
    #Add your code here
    pass

def render_trans_text(text, font_size, font_color, transform, font=DEFAULT_FONT):
    """ Renders text to the screen, relative to screen space, doesn't support rotation """
    #Add your code here
    pass

def render_relative_text(text, font_size, font_color, transform, font=DEFAULT_FONT):
    """ Renders text to the screen, relative to world space, doesn't support rotation """
    #Add your code here
    pass

#End Text
########################################################
#Lines

def render_line(p1, p2, color=Color(), width=1):
    """ Renders a line to the screen in px coordinates relative to Screen Space, width optional """
    #Add your code here
    pass

def render_trans_line(p1, p2, transform, color=Color(), width = 1):
    """ Renders a line to the screen in px coordinates relative to Screen Space and the transform given, width optional """
    #Add your code here
    pass

def render_relative_line(p1, p2, transform, color=Color(), width=1):
    """ Renders a line to the screen with coordinates relative to World Space with the game_object's transform, width optional """
    #Add your code here
    pass

#End Lines
#########################################################
#Circles

def render_circle(circle, fill_mode=FillMode.FILL, width=1):
    """ Renders a circle to the screen in px coordinates relative to Screen Space, width optional (Mesh and Outline) """
    #Add your code here
    pass
    
def render_trans_circle(circle, transform, fill_mode=FillMode.FILL, width = 1):
    """ Renders a circle to the screen in px coordinates relative to Screen Space and the transform given, width optional (Mesh and Outline) """
    #Add your code here
    pass

def render_relative_circle(circle, transform, fill_mode=FillMode.FILL, width=1):
    """ Renders a circle to the screen with coordinates relative to World Space with the game_object's transform, width optional (Mesh and Outline) """
    #Add your code here
    pass

#End Circles