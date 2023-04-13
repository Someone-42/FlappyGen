from Core import *
from UICore import *
import enum

#
#   Extension MoreUIModels:
#       This extension supplies a small variety of UIModels to enhance the UI when creating an app or a game
#
#   Version : 1.3
#

class UIButtonOperatorSignModel(UIModel):
    class Operator(enum.Enum):
        MINUS_SIGN=-1
        PLUS_SIGN=1
        #todo: divide and multiply

    __slots__=("operator_sign",
               "margin", # Margin is a portion of the ui_object's size
               "color",
               "sign_color",
               "sign_width",
               "fill_mode",
               "width",
               "_button_rect",
               "_final_width",
               "_r_lines",
               "_r_sign_width",
               "outline",
               "_outline_rect",
               "outline_width",
               "_r_outline_width")
    def __init__(self, operator_sign=Operator.MINUS_SIGN, margin=0.15, color=Color(60, 60, 60), sign_color=Color(240, 240, 240), sign_width=0.15, outline=True, outline_width=0.085, fill_mode=FillMode.FILL, width=0.005):
        super().__init__()
        self.fill_mode = fill_mode
        self.color = color
        self.sign_color = sign_color
        self.sign_width = sign_width
        self._button_rect = None
        self.margin = margin
        self.width = width
        self._final_width = None
        self._r_lines = None
        self.operator_sign = operator_sign
        self._r_sign_width = None
        self.outline = outline
        self._outline_rect = None
        self.outline_width = outline_width
        self._r_outline_width = None

    def recalculate(self):
        """ Recalculates the button's parameters for rendering (call when changing text/position, etc...) """
        size = self.ui_object.rect_transform.real_size.min_comp()
        margin = size * self.margin
        normal = (self.ui_object.rect_transform.real_size - Vector2.scaler(size)).normalize()
        pos = normal * (self.ui_object.rect_transform.real_size.max_comp() - size) / 2 + self.ui_object.rect_transform.real_position
        normal = Vector2(1, 0)
        self._button_rect = Rectangle2(pos, Vector2.scaler(size), self.color)
        self._outline_rect = Rectangle2(pos, Vector2.scaler(size), self.sign_color)
        self._final_width = int(get_engine().WINDOW_SIZE.min_comp() * self.width)
        self._r_sign_width = int(size * self.sign_width)
        self._r_outline_width = int(size * self.outline_width)
        self.ui_object._bounding_box.pos = pos.copy()
        self.ui_object._bounding_box.size = Vector2.scaler(size)
        if self.operator_sign == self.Operator.MINUS_SIGN:
            self._r_lines = (
                (pos + normal * margin + normal.flip_comp() * size / 2, pos + normal * size - normal * margin + normal.flip_comp() * size / 2),
            )
        if self.operator_sign == self.Operator.PLUS_SIGN:
            self._r_lines = (
                (pos + normal * margin + normal.flip_comp() * size / 2, pos + normal * size - normal * margin + normal.flip_comp() * size / 2),
                (pos + normal.flip_comp() * margin + normal * size / 2, pos + normal.flip_comp() * size - normal.flip_comp() * margin + normal * size / 2)
            )

    def render(self):
        Renderer.render_rect(self._button_rect, self.fill_mode, self._final_width)
        for line in self._r_lines:
            Renderer.render_line(line[0], line[1], self.sign_color, self._r_sign_width)
        if self.outline:
            Renderer.render_rect(self._outline_rect, FillMode.OUTLINE, self._r_outline_width)

class UIButtonArrowModel(UIModel):
    class Direction(enum.Enum):
        UP=2
        RIGHT=1
        LEFT=-1
        DOWN=-2

    __slots__=("direction",
               "margin", # Margin is a portion of the ui_object's size
               "color",
               "arrow_color",
               "arrow_width",
               "fill_mode",
               "width",
               "_button_rect",
               "_final_width",
               "_r_lines",
               "_r_arrow_width",
               "outline",
               "_outline_rect",
               "outline_width",
               "_r_outline_width")
    def __init__(self, direction=Direction.RIGHT, margin=0.2, color=Color(60, 60, 60), arrow_color=Color(240, 240, 240), arrow_width=0.15, outline=True, outline_width=0.085, fill_mode=FillMode.FILL, width=0.005):
        super().__init__()
        self.fill_mode = fill_mode
        self.color = color
        self.arrow_color = arrow_color
        self.arrow_width = arrow_width
        self._button_rect = None
        self.margin = margin
        self.width = width
        self._final_width = None
        self._r_lines = None
        self.direction = direction
        self._r_arrow_width = None
        self.outline = outline
        self._outline_rect = None
        self.outline_width = outline_width
        self._r_outline_width = None

    def recalculate(self):
        """ Recalculates the button's parameters for rendering (call when changing text/position, etc...) """
        size = self.ui_object.rect_transform.real_size.min_comp()
        margin = size * self.margin
        normal = (self.ui_object.rect_transform.real_size - Vector2.scaler(size)).normalize()
        pos = normal * (self.ui_object.rect_transform.real_size.max_comp() - size) / 2 + self.ui_object.rect_transform.real_position
        normal = Vector2(1, 0)
        self._button_rect = Rectangle2(pos, Vector2.scaler(size), self.color)
        self._outline_rect = Rectangle2(pos, Vector2.scaler(size), self.arrow_color)
        self._final_width = int(get_engine().WINDOW_SIZE.min_comp() * self.width)
        self._r_arrow_width = int(size * self.arrow_width)
        self._r_outline_width = int(size * self.outline_width)
        self.ui_object._bounding_box.pos = pos.copy()
        self.ui_object._bounding_box.size = Vector2.scaler(size)
        if self.direction == self.Direction.RIGHT:
            self._r_lines = (
                (pos + Vector2.scaler(margin), pos - normal * margin + Vector2(size, size / 2)),
                (pos + Vector2(margin, -margin) + normal.flip_comp() * size, pos - normal * margin + Vector2(size, size / 2))
            )
        if self.direction == self.Direction.LEFT:
            self._r_lines = (
                (pos + normal * (size - margin) + normal.flip_comp() * margin, pos + Vector2(margin, size / 2)),
                (pos + normal * (size - margin) + normal.flip_comp() * -margin + normal.flip_comp() * size, pos + Vector2(margin, size / 2))
            )
        if self.direction == self.Direction.UP:
            self._r_lines = (
                (pos + Vector2.scaler(margin), pos + Vector2(size / 2, size - margin)),
                (pos + Vector2(size - margin, margin), pos + Vector2(size / 2, size - margin))
            )
        if self.direction == self.Direction.DOWN:
            self._r_lines = (
                (pos + Vector2(margin, size - margin), pos + Vector2(size / 2, margin)),
                (pos + Vector2(size - margin, size - margin), pos + Vector2(size / 2, margin))
            )

    def render(self):
        Renderer.render_rect(self._button_rect, self.fill_mode, self._final_width)
        for line in self._r_lines:
            Renderer.render_line(line[0], line[1], self.arrow_color, self._r_arrow_width)
        if self.outline:
            Renderer.render_rect(self._outline_rect, FillMode.OUTLINE, self._r_outline_width)

class UIToggleButtonPauseModel(UIModel):
    __slots__=("direction",
               "margin", # Margin is a portion of the ui_object's size
               "color",
               "foreground_color",
               "foreground_width",
               "fill_mode",
               "width",
               "_button_rect",
               "_final_width",
               "_r_lines",
               "_r_pause_triangle",
               "_r_foreground_width",
               "outline",
               "_outline_rect",
               "paused_fill",
               "outline_width",
               "_r_outline_width",
               "paused_width",
               "_r_paused_width")
    def __init__(self, margin=0.25, color=Color(60, 60, 60), foreground_color=Color(240, 240, 240), outline=True, outline_width=0.085, foreground_width=0.2, paused_fill=FillMode.FILL, paused_width=0.1, fill_mode=FillMode.FILL, width=0.005):
        super().__init__()
        self.fill_mode = fill_mode
        self.color = color
        self.foreground_color = foreground_color
        self.foreground_width = foreground_width
        self._button_rect = None
        self.margin = margin
        self.width = width
        self._final_width = None
        self._r_lines = None
        self._r_foreground_width = None
        self.outline = outline
        self.outline_width = outline_width
        self._outline_rect = None
        self.paused_fill = paused_fill
        self._r_pause_triangle = None
        self._r_outline_width = None
        self.paused_width = paused_width
        self._r_paused_width = None

    def recalculate(self):
        """ Recalculates the button's parameters for rendering (call when changing text/position, etc...) """
        size = self.ui_object.rect_transform.real_size.min_comp()
        margin = size * self.margin
        normal = (self.ui_object.rect_transform.real_size - Vector2.scaler(size)).normalize()
        pos = normal * (self.ui_object.rect_transform.real_size.max_comp() - size) / 2 + self.ui_object.rect_transform.real_position
        normal = Vector2(1, 0)
        self._button_rect = Rectangle2(pos, Vector2.scaler(size), self.color)
        self._outline_rect = Rectangle2(pos, Vector2.scaler(size), self.foreground_color)
        self._final_width = int(get_engine().WINDOW_SIZE.min_comp() * self.width)
        self._r_foreground_width = int(size * self.foreground_width)
        self._r_outline_width = int(size * self.outline_width)
        self._r_paused_width = int(size * self.paused_width)
        self.ui_object._bounding_box.pos = pos.copy()
        self.ui_object._bounding_box.size = Vector2.scaler(size)
        self.toggle_changed()
        self._r_pause_triangle = Triangle2(pos + normal * (margin + self._r_paused_width / 2) + normal.flip_comp() * margin,
                                           pos + normal * (margin + self._r_paused_width / 2) + normal.flip_comp() * (size - margin),
                                           pos + normal * (size - margin) + normal.flip_comp() * (size / 2),
                                           self.foreground_color)
        self._r_lines = (
            (pos + normal * (size / 3) + normal.flip_comp() * margin, pos + normal * (size / 3) + normal.flip_comp() * (size - margin)),
            (pos + normal * (size / 3) * 2 + normal.flip_comp() * margin, pos + normal * (size / 3) * 2 + normal.flip_comp() * (size - margin))
        )

    def toggle_changed(self):
        pass

    def render(self):
        Renderer.render_rect(self._button_rect, self.fill_mode, self._final_width)
        if self.ui_object.toggled:
            Renderer.render_tri(self._r_pause_triangle, self.paused_fill, self._r_paused_width)
        else:
            Renderer.render_line(self._r_lines[0][0], self._r_lines[0][1], self.foreground_color, self._r_foreground_width)
            Renderer.render_line(self._r_lines[1][0], self._r_lines[1][1], self.foreground_color, self._r_foreground_width)
        if self.outline:
            Renderer.render_rect(self._outline_rect, FillMode.OUTLINE, self._r_outline_width)
