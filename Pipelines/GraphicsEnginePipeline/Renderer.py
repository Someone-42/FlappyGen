from Core import *
from RendererCore import *
import graphics
import math

"""

HELP PANEL :
*1 : in screen coordinates/coords = when a Vector2 is set between Vector2(0, 0) and Vector2(1, 1) where Vector2(1, 1) => SnakeEngine.WINDOW_SIZE (it is representing window space) # This is mostly used for UI
*2 : in screen space = when a Vector2 is set between Vector2(0, 0) and Vector2(SnakeEngine.WIDTH, SnakeEngine.HEIGHT)

"""

def _Color_to_couleur(color):
    return graphics.couleur(color.r, color.g, color.b, color.a)

def _Vector2_to_point(vector2):
    return graphics.Point(int(vector2.x), int(vector2.y))

DEFAULT_FONT = "arial"

def init():
    graphics.affiche_auto_off()

def clear():
    graphics.remplir_fenetre(_Color_to_couleur(get_engine().CLEAR_COLOR))

def start():
    graphics.init_fenetre(get_engine().WIDTH, get_engine().HEIGHT, get_engine().TITLE)
    clear()

def pre_render():
    clear()

def render():
    graphics.affiche_tout()

def clean_up():
    clear()

def close():
    clean_up()

    
########################################################
#                      UI Getters                      #
########################################################

def get_text_size(text, font_size, font=DEFAULT_FONT):
    """ Return a vector 2 giving the width and the height of the text in screen coordinates *1 """
    return Vector2(
        graphics.largeur_texte(text, font_size, font), 
        graphics.hauteur_texte(text, font_size, font)).div_comp(get_engine().WINDOW_SIZE)

def get_optimal_font_size(text, size, font=DEFAULT_FONT):
    """ Returns the optimal font size (for a text and a size to ~fit in (in screen coords *1) """
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
    if fill_mode == FillMode.OUTLINE or fill_mode == FillMode.MESH:
        graphics.affiche_triangle(_Vector2_to_point(triangle.p1), _Vector2_to_point(triangle.p2), _Vector2_to_point(triangle.p3), _Color_to_couleur(triangle.color), width)
    if fill_mode == FillMode.FILL:
        graphics.affiche_triangle_plein(_Vector2_to_point(triangle.p1), _Vector2_to_point(triangle.p2), _Vector2_to_point(triangle.p3), _Color_to_couleur(triangle.color))
        
def render_trans_tri(triangle, transform, fill_mode=FillMode.FILL, width = 1):
    """ Renders a triangle to the screen in px coordinates relative to Screen Space and the transform given, width optional (Mesh and Outline) """
    angle_r = math.radians(transform.rotation)
    tri = Triangle2(
        triangle.p1.mul_comp(transform.scale).rotate(angle_r) + transform.position,
        triangle.p2.mul_comp(transform.scale).rotate(angle_r) + transform.position,
        triangle.p3.mul_comp(transform.scale).rotate(angle_r) + transform.position,
        triangle.color
    )
    render_tri(tri, fill_mode, width)

def render_relative_tri(triangle, transform, fill_mode=FillMode.FILL, width=1):
    """ Renders a triangle to the screen with coordinates relative to World Space with the game_object's transform, width optional (Mesh and Outline) """
    rel_t = transform.sum_up()
    angle_r = math.radians(rel_t.rotation)
    tri = Triangle2(
        (triangle.p1.mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale),
        (triangle.p2.mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale),
        (triangle.p3.mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale),
        triangle.color
    )
    render_tri(tri, fill_mode, width)

#End Triangles
########################################################
#Polygons

def render_poly(polygon, fill_mode=FillMode.FILL, width=1):
    #TO FIX
    if fill_mode == FillMode.FILL:
        for i in range(0, len(polygon.points), 1):
            graphics.affiche_triangle_plein(_Vector2_to_point(polygon.points[i]), _Vector2_to_point(polygon.points[i-1]), _Vector2_to_point(polygon.points[i-2]), _Color_to_couleur(polygon.color))
    elif fill_mode == FillMode.MESH:
        for i in range(0, len(polygon.points), 1):
            graphics.affiche_triangle(_Vector2_to_point(polygon.points[i]), _Vector2_to_point(polygon.points[i+1]), _Vector2_to_point(polygon.points[i+2]), _Color_to_couleur(polygon.color), width)
    elif fill_mode == FillMode.OUTLINE:
        for i in range(len(polygon.points)):
            graphics.affiche_ligne(_Vector2_to_point(polygon.points[i-1]), _Vector2_to_point(polygon.points[i]), _Color_to_couleur(polygon.color), width)

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
    if fill_mode == FillMode.FILL:
        graphics.affiche_rectangle_plein(rect.pos, rect.pos + rect.size, _Color_to_couleur(rect.color))
    if fill_mode == FillMode.MESH or fill_mode == FillMode.OUTLINE:
        graphics.affiche_rectangle(rect.pos, rect.pos + rect.size, _Color_to_couleur(rect.color), width)

def render_trans_rect(rect, transform, fill_mode=FillMode.FILL, width = 1):
    """ Renders a quad to the screen in px coordinates relative to Screen Space and the transform given, width optional (Mesh and Outline) """
    angle_r = math.radians(transform.rotation)
    p1 = rect.pos.mul_comp(transform.scale).rotate(angle_r) + transform.position
    p2 = (rect.pos + Vector2(rect.size.x)).mul_comp(transform.scale).rotate(angle_r) + transform.position
    p3 = (rect.pos + Vector2(0, rect.size.y)).mul_comp(transform.scale).rotate(angle_r) + transform.position
    p4 = (rect.pos + rect.size).mul_comp(transform.scale).rotate(angle_r) + transform.position
    if fill_mode == FillMode.FILL or fill_mode == FillMode.MESH:
        render_tri(Triangle2(p1, p2, p3, rect.color), fill_mode, width)
        render_tri(Triangle2(p4, p2, p3, rect.color), fill_mode, width)
    else:
        render_line(p1, p2, rect.color, width) # Bottom
        render_line(p1, p3, rect.color, width) # Left
        render_line(p2, p4, rect.color, width) # Right
        render_line(p3, p4, rect.color, width) # Top

def render_relative_rect(rect, transform, fill_mode=FillMode.FILL, width=1):
    """ Renders a quad to the screen with coordinates relative to World Space with the game_object's transform, width optional (Mesh and Outline) """
    rel_t = transform.sum_up()
    angle_r = math.radians(rel_t.rotation)
    p1 = (rect.pos.mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale)
    p2 = ((rect.pos + Vector2(rect.size.x)).mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale)
    p3 = ((rect.pos + Vector2(0, rect.size.y)).mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale)
    p4 = ((rect.pos + rect.size).mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale)
    if fill_mode == FillMode.FILL or fill_mode == FillMode.MESH:
        render_tri(Triangle2(p1, p2, p3, rect.color), fill_mode, width)
        render_tri(Triangle2(p4, p2, p3, rect.color), fill_mode, width)
    else:
        render_line(p1, p2, rect.color, width) # Bottom
        render_line(p1, p3, rect.color, width) # Left
        render_line(p2, p4, rect.color, width) # Right
        render_line(p3, p4, rect.color, width) # Top

#End Quads
########################################################
#Sprites

def render_sprite(sprite):
    """ Renders a Sprite to the screen, with the position relative to screen_space """
    sprite._set_sprite_size(sprite.get_size()) # updates the sprite size to make sure it is rendered correctly
    if sprite.partial:
        graphics.affiche_image(sprite.get_img_src(), _Vector2_to_point(sprite._r_pos), sprite._r_part.pos, sprite._r_part.size)
    else:
        graphics.affiche_image(sprite.get_img_src(), _Vector2_to_point(sprite._r_pos))

def render_trans_sprite(sprite, transform):
    """ Renders a Sprite to the screen, relative to screen space, doesn't support rotation """
    size = sprite.get_size().mul_comp(transform.scale)
    sprite._set_sprite_size(size)
    if sprite.partial:
        graphics.affiche_image(sprite.get_img_src(), _Vector2_to_point(sprite._r_pos+transform.position), sprite._r_part.pos, sprite._r_part.size)
    else:
        graphics.affiche_image(sprite.get_img_src(), _Vector2_to_point(sprite._r_pos+transform.position))

def render_relative_sprite(sprite, transform):
    """ Renders a Sprite to the screen, relative to world space, doesn't support rotation """
    rel_t = transform.sum_up()
    size = (sprite.get_size().mul_comp(rel_t.scale)).mul_comp(get_engine().main_camera.scale)
    pos = (sprite._r_pos + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale)
    sprite._set_sprite_size(size)
    if sprite.partial:    
        graphics.affiche_image(sprite.get_img_src(), _Vector2_to_point(pos), sprite._r_part.pos, sprite._r_part.size)
    else:
        graphics.affiche_image(sprite.get_img_src(), _Vector2_to_point(pos))

#End Sprites
########################################################
#Text

def render_text(text, font_size, font_color, pos, font=DEFAULT_FONT):
    """ Renders text to the screen, with the position relative to screen_space """
    graphics.affiche_texte(text, _Vector2_to_point(pos), _Color_to_couleur(font_color), font_size, font)

def render_trans_text(text, font_size, font_color, transform, pos, font=DEFAULT_FONT):
    """ Renders text to the screen, relative to screen space, doesn't support rotation """
    render_text(text, font_size * min(transform.scale.x, transform.scale.y), font_color, transform.position + pos, font)

def render_relative_text(text, font_size, font_color, transform, pos, font=DEFAULT_FONT):
    """ Renders text to the screen, relative to world space, doesn't support rotation """
    rel_t = transform.sum_up()
    rel_t.position -= get_engine().main_camera.position
    rel_t.scale = rel_t.scale.mul_comp(get_engine().main_camera.scale)
    render_trans_text(text, font_size, font_color, rel_t, pos.mul_comp(rel_t.scale), font)

#End Text
#########################################################
#Lines

def render_line(p1, p2, color=Color(), width=1):
    """ Renders a line to the screen in px coordinates relative to Screen Space, width optional """
    graphics.affiche_ligne(_Vector2_to_point(p1), _Vector2_to_point(p2), _Color_to_couleur(color), width)

def render_trans_line(p1, p2, transform, color=Color(), width = 1):
    """ Renders a line to the screen in px coordinates relative to Screen Space and the transform given, width optional """
    angle_r = math.radians(transform.rotation)
    p1 = p1.mul_comp(transform.scale).rotate(angle_r) + transform.position
    p2 = p2.mul_comp(transform.scale).rotate(angle_r) + transform.position
    render_line(p1, p2, color, width)

def render_relative_line(p1, p2, transform, color=Color(), width=1):
    """ Renders a line to the screen with coordinates relative to World Space with the game_object's transform, width optional """
    rel_t = transform.sum_up()
    angle_r = math.radians(rel_t.rotation)
    p1 = (p1.mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale)
    p2 = (p2.mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale)
    render_line(p1, p2, color, width)

#End Lines
##########################################################
#Circles

def render_circle(circle, fill_mode=FillMode.FILL, width=1):
    """ Renders a circle to the screen in px coordinates relative to Screen Space, width optional (Mesh and Outline) """
    if fill_mode == FillMode.OUTLINE or fill_mode == FillMode.MESH:
        graphics.affiche_cercle(_Vector2_to_point(circle.pos), int(circle.radius), _Color_to_couleur(circle.color), width)
    if fill_mode == FillMode.FILL:
        graphics.affiche_cercle_plein(_Vector2_to_point(circle.pos), int(circle.radius), _Color_to_couleur(circle.color))

def render_trans_circle(circle, transform, fill_mode=FillMode.FILL, width = 1):
    """ Renders a circle to the screen in px coordinates relative to Screen Space and the transform given, width optional (Mesh and Outline) """
    angle_r = math.radians(transform.rotation)
    crcl = Circle(
        circle.radius * transform.scale.min_comp(),
        circle.pos.mul_comp(transform.scale).rotate(angle_r) + transform.position,
        circle.color
    )
    render_circle(crcl, fill_mode, width)

def render_relative_circle(circle, transform, fill_mode=FillMode.FILL, width=1):
    """ Renders a circle to the screen with coordinates relative to World Space with the game_object's transform, width optional (Mesh and Outline) """
    rel_t = transform.sum_up()
    angle_r = math.radians(rel_t.rotation)
    crcl = Circle(
        circle.radius * rel_t.scale.min_comp(),
        (circle.pos.mul_comp(rel_t.scale).rotate(angle_r) + rel_t.position - get_engine().main_camera.position).mul_comp(get_engine().main_camera.scale),
        circle.color
    )
    render_circle(crcl, fill_mode, width)

#End Circles