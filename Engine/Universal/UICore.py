from Core import *
from RendererCore import *
import Renderer
import enum

""" 

Every parameter for UIModels are in screen cordinates, refer to the Renderer panel for more info

"""

# The whole UI System might need some rework........................................

### Base ###

class AxisAlignType(enum.IntEnum):
    LEFT=-1
    TOP=1
    RIGHT=1
    BOTTOM=-1
    CENTER=0

class UIFunctionSet:

    @staticmethod
    def on_start(ui_object):
        """ A static method that can be set as another by doing : ui_obj.on_start = your_method_start | this method will be called on the start before set_style """
        pass
    
    @staticmethod
    def on_stop(ui_object):
        """ A static method that can be set as another by doing : ui_obj.on_stop = your_method_stop | this method will be called on the stop """
        pass
    
    @staticmethod
    def on_update(ui_object):
        """ A static method that can be set as another by doing : ui_obj.on_update = your_method_update | this method will be called on the update if selected """
        pass
    
    @staticmethod
    def on_render(ui_object):
        """ A static method that can be set as another by doing : ui_obj.on_render = your_method_render | this method will be called on the rendering """
        pass
    
    @staticmethod
    def set_style(ui_object):
        """ A static method can be set as method by doing : ui_obj.set_style = your_method_setting_style | this method will be called on the start """
        pass
    
    @staticmethod
    def on_select(ui_object, click):
        """ A static method that can be set as another by doing : ui_obj.on_select_called = your_method_on_select | this method will be called on the selection of the ui_object """
        pass
    
    @staticmethod
    def on_deselect(ui_object):
        """ A static method that can be set as another by doing : ui_obj.on_deselect_called = your_method_on_deselect | this method will be called on the deselection of the ui_object """
        pass

class RectTransform:
    __slots__=("real_position",
               "real_size",
               "position",
               "scale",
               "size",
               "ui_object")
    def __init__(self, position=Vector2(0, 0), scale=Vector2(1, 1), size=Vector2(0.5, 0.5)):
        """ TODO : DESCRIPTION + PARAMS """
        self.position = position
        self.scale = scale
        self.size = size
        #Set when starting
        self.real_position = None
        self.real_size = None
        self.ui_object = None
    
    def recalculate(self):
        """ Recalculates the transform's parameters (call when changing position, etc...) """
        self.real_position = SC_to_SS(self.position)
        self.real_size = SC_to_SS(self.size.mul_comp(self.scale))

    def awake(self, ui_object):
        self.ui_object = ui_object

    def copy(self):
        """ Returns a copy of the object, real_position and real_size are not copied -> has to be recalculated to access them """
        return RectTransform(self.position.copy(), self.scale.copy(), self.size.copy())

### End Base ###
################
### Models ###

class UIModel(Model):
    __slots__=("ui_object")
    def __init__(self):
        self.ui_object = None

    def awake(self, ui_object):
        self.ui_object = ui_object

    def start(self):
        pass
     
    def recalculate(self):
        pass
    
class UIButtonModel(UIModel):
    __slots__=("margin", # Margin is a portion of the ui_object's size
               "font",
               "color",
               "font_color",
               "fill_mode",
               "width",
               "_font_size",
               "_button_rect",
               "_real_text_pos",
               "_final_width")
    def __init__(self, margin=Vector2(0.2, 0.1), color=Color(100, 100, 100), font_color=Color(255, 255, 255), fill_mode=FillMode.FILL, width=0.005, font=Renderer.DEFAULT_FONT):
        super().__init__()
        self.font = font
        self.fill_mode = fill_mode
        self.color = color
        self.font_color = font_color
        self._font_size = None
        self._button_rect = None
        self._real_text_pos = None
        self.margin = margin
        self.width = width
        self._final_width = None

    def recalculate(self):
        """ Recalculates the button's parameters for rendering (call when changing text/position, etc...) """
        margin = self.ui_object.rect_transform.size.mul_comp(self.ui_object.rect_transform.scale).mul_comp(self.margin)
        self._font_size = Renderer.get_optimal_font_size(self.ui_object.text, self.ui_object.rect_transform.size.mul_comp(self.ui_object.rect_transform.scale) - (margin * 2).mul_comp(self.ui_object.rect_transform.scale), self.font)
        text_rect_size = Renderer.get_text_size(self.ui_object.text, self._font_size, self.font)
        final_margin = (self.ui_object.rect_transform.size.mul_comp(self.ui_object.rect_transform.scale) - text_rect_size) / 2
        self._button_rect = Rectangle2(self.ui_object.rect_transform.real_position, self.ui_object.rect_transform.real_size, self.color)
        self._real_text_pos = self.ui_object.rect_transform.real_position + SC_to_SS(final_margin)
        self._final_width = int(get_engine().WINDOW_SIZE.min_comp() * self.width)
        self.ui_object._bounding_box.pos = self.ui_object.rect_transform.real_position.copy()
        self.ui_object._bounding_box.size = self.ui_object.rect_transform.real_size.copy()

    def render(self):
        Renderer.render_rect(self._button_rect, self.fill_mode, self._final_width)
        Renderer.render_text(self.ui_object.text, self._font_size, self.font_color, self._real_text_pos, self.font)

class UIButtonSpriteModel(UIModel):
    __slots__=("margin", # Margin is a portion of the ui_object's size
               "font",
               "font_color",
               "sprite_fit_mode",
               "sprite",
               "do_render_text",
               "_font_size",
               "_real_text_pos")
    def __init__(self, sprite, margin=Vector2(0.2, 0.1), do_render_text=False, font_color=Color(255, 255, 255), sprite_fit_mode=SpriteFitMode.FIT, font=Renderer.DEFAULT_FONT):
        super().__init__()
        self.do_render_text = do_render_text
        self.font = font
        self.font_color = font_color
        self._font_size = None
        self._real_text_pos = None
        self.margin = margin
        self.sprite_fit_mode = sprite_fit_mode
        self.sprite = sprite

    def start(self):
        self.sprite.load()

    def recalculate(self):
        """ Recalculates the button's parameters for rendering (call when changing text/position, etc...) """
        self.ui_object._bounding_box = self.sprite.set_to_fit_in_box(
            Rect(self.ui_object.rect_transform.real_position.copy(), self.ui_object.rect_transform.real_size.copy()), self.sprite_fit_mode)
        sc_bb = Rect(SS_to_SC(self.ui_object._bounding_box.pos), SS_to_SC(self.ui_object._bounding_box.size)) # Screen coordinates bounding box
        margin = sc_bb.size.mul_comp(self.margin)
        self._font_size = Renderer.get_optimal_font_size(self.ui_object.text, sc_bb.size - (margin * 2).mul_comp(self.ui_object.rect_transform.scale), self.font)
        text_rect_size = Renderer.get_text_size(self.ui_object.text, self._font_size, self.font)
        final_margin = (sc_bb.size - text_rect_size) / 2
        self._real_text_pos = self.ui_object._bounding_box.pos + SC_to_SS(final_margin)
        
    def render(self):
        Renderer.render_sprite(self.sprite)
        if self.do_render_text:
            Renderer.render_text(self.ui_object.text, self._font_size, self.font_color, self._real_text_pos, self.font)

class UIKnobRoundModel(UIModel):
    __slots__=("color",
               "radius",
               "fill_mode",
               "width",
               "_circle")
    def __init__(self, radius=0.8, color=Color(128, 128, 128), fill_mode=FillMode.FILL, width=0.02):
        """
        Round knob model for the slider model
        @param: the real radius of the knob is equals to (if horizontal) ui_object.rect_transform.real_size.y * radius
        """
        super().__init__()
        self.radius = radius
        self.color = color
        self._circle = None
        self.fill_mode = fill_mode
        self.width = width

    def awake(self, ui_object):
        super().awake(ui_object)

    def recalculate(self):
        if self.ui_object.is_horizontal:
            self._circle = Circle(self.radius * self.ui_object.rect_transform.real_size.y, 
                                  Vector2((self.ui_object.value - self.ui_object.min_max_value.x) / (self.ui_object.min_max_value.y - self.ui_object.min_max_value.x) * self.ui_object.rect_transform.real_size.x, self.ui_object.rect_transform.real_size.y / 2) +
                                  self.ui_object.rect_transform.real_position, self.color)
        else:
            self._circle = Circle(self.radius * self.ui_object.rect_transform.real_size.x, 
                                  Vector2(self.ui_object.rect_transform.real_size.x / 2, (self.ui_object.value - self.ui_object.min_max_value.x) / (self.ui_object.min_max_value.y - self.ui_object.min_max_value.x) * self.ui_object.rect_transform.real_size.y) +
                                    self.ui_object.rect_transform.real_position, self.color)

    def render(self):
        Renderer.render_circle(self._circle, self.fill_mode, self.width)

    def check_click(self, click):
        return self._circle.pos.squared_distance(click) < self._circle.radius * self._circle.radius 

class UISliderModel(UIModel):
    __slots__=("knob_model",
               "color",
               "_rect_render")
    def __init__(self, color=Color(42, 42, 42), knob_model=UIKnobRoundModel()):
        super().__init__()
        self.knob_model = knob_model
        self.color = color
        self._rect_render = None

    def recalculate(self):
        self._rect_render = Rectangle2(self.ui_object.rect_transform.real_position, self.ui_object.rect_transform.real_size, self.color)
        self.knob_model.recalculate()
        
    def awake(self, ui_object):
        super().awake(ui_object)
        self.knob_model.awake(ui_object)

    def start(self):
        super().start()
        self.knob_model.start()
    
    def render(self):
        Renderer.render_rect(self._rect_render)
        self.knob_model.render()

class UILabelModel(UIModel):
    __slots__=("color",
               "font",
               "xalignement",
               "yalignement",
               "_font_size",
               "_real_text_pos")
    def __init__(self, color=Color(240, 240, 240), xalignment=AxisAlignType.CENTER, yalignment=AxisAlignType.CENTER, font=Renderer.DEFAULT_FONT):
        super().__init__()
        self.color = color
        self.font = font
        self.xalignement = xalignment
        self.yalignement = yalignment
        self._font_size = None
        self._real_text_pos = Vector2(0, 0)

    def recalculate(self):
        self._font_size = Renderer.get_optimal_font_size(self.ui_object.text, self.ui_object.rect_transform.size.mul_comp(self.ui_object.rect_transform.scale), self.font)
        txt_size = Renderer.get_text_size(self.ui_object.text, self._font_size, self.font)
        final_margin = SC_to_SS((self.ui_object.rect_transform.size.mul_comp(self.ui_object.rect_transform.scale) - txt_size) / 2)
        real_pos = SC_to_SS(self.ui_object.rect_transform.position)
        if self.xalignement == AxisAlignType.CENTER:
            self._real_text_pos.x = final_margin.x * 1 + real_pos.x
        if self.xalignement == AxisAlignType.LEFT:
            self._real_text_pos.x = real_pos.x
        if self.xalignement == AxisAlignType.RIGHT:
            self._real_text_pos.x = final_margin.x * 2 + real_pos.x
        if self.yalignement == AxisAlignType.CENTER:
            self._real_text_pos.y = final_margin.y * 1 + real_pos.y
        if self.yalignement == AxisAlignType.BOTTOM:
            self._real_text_pos.y = real_pos.y
        if self.yalignement == AxisAlignType.TOP:
            self._real_text_pos.y = final_margin.y * 2 + real_pos.y

    def render(self):
        Renderer.render_text(self.ui_object.text, self._font_size, self.color, self._real_text_pos, self.font)

class UIToggleButtonModel(UIModel):
    __slots__=("__alignment",
               "do_render_text",
               "knob_margin",
               "knob_color",
               "toggled_color",
               "color",
               "_r_rect",
               "_label",
               "_ext_end_circles",
               "_r_value_circle",
               "_r_value_circle_pos",
               "label_model",
               "label_margin")
    def __init__(self, do_render_text=True, alignment=AxisAlignType.RIGHT, knob_margin=4, color=Color(60, 60, 60), toggled_color=Color(60, 100, 220), knob_color=Color(230, 230, 230), label_model=UILabelModel(), label_margin=Vector2(0.1, 0.05)): # CENTER alignment won't work, and will use RIGHT by default
        super().__init__()
        self.do_render_text = do_render_text
        if alignment == AxisAlignType.CENTER:
            alignment = AxisAlignType.RIGHT
        self.__alignment = int(alignment)
        self.label_model = label_model
        self.knob_margin = knob_margin
        self.knob_color = knob_color
        self.toggled_color = toggled_color
        self.color = color
        self._label = None
        self._r_rect = None
        self._ext_end_circles = None
        self._r_value_circle = None
        self._r_value_circle_pos = None
        self.label_margin = label_margin

    def awake(self, ui_object):
        super().awake(ui_object)
        self.label_model.awake(ui_object)

    def start(self):
        super().start()
        self.label_model.start()

    def set_alignment(self, new_alignment):
        if new_alignment == AxisAlignType.CENTER:
            new_alignment = AxisAlignType.RIGHT
        self.__alignment = int(new_alignment)

    def get_alignment(self):
        return self.__alignment

    def label_recalculate(self, label_bounding_box):
        self.label_model._font_size = Renderer.get_optimal_font_size(self.ui_object.text, label_bounding_box.size, self.label_model.font)
        txt_size = Renderer.get_text_size(self.ui_object.text, self.label_model._font_size, self.label_model.font)
        final_margin = SC_to_SS((label_bounding_box.size - txt_size) / 2)
        real_pos = label_bounding_box.pos
        if self.label_model.xalignement == AxisAlignType.CENTER:
            self.label_model._real_text_pos.x = final_margin.x * 1 + real_pos.x
        if self.label_model.xalignement == AxisAlignType.LEFT:
            self.label_model._real_text_pos.x = real_pos.x
        if self.label_model.xalignement == AxisAlignType.RIGHT:
            self.label_model._real_text_pos.x = final_margin.x * 2 + real_pos.x
        if self.label_model.yalignement == AxisAlignType.CENTER:
            self.label_model._real_text_pos.y = final_margin.y * 1 + real_pos.y
        if self.label_model.yalignement == AxisAlignType.BOTTOM:
            self.label_model._real_text_pos.y = real_pos.y
        if self.label_model.yalignement == AxisAlignType.TOP:
            self.label_model._real_text_pos.y = final_margin.y * 2 + real_pos.y

    def recalculate(self):
        sorted = self.ui_object.rect_transform.real_size.sort_comp()
        min_size = sorted.x
        ar = min_size / self.ui_object.rect_transform.real_size.max_comp()
        if ar > 0.5:
            min_size = sorted.y / 2

        dir_normal = (self.ui_object.rect_transform.real_size - Vector2(1, 1) * sorted.x).normalize()
        alignment_v_mul_normal = dir_normal * ((int(self.__alignment) + 1) / 2)
        bounding_box_size = (Vector2(1, 1) + dir_normal) * min_size
        axis_offset = dir_normal.flip_comp() * ((sorted.x - min_size) / 2)
        radius = min_size / 2 + 0.5

        self.ui_object._bounding_box = Rect(self.ui_object.rect_transform.real_position + axis_offset + alignment_v_mul_normal.mul_comp(self.ui_object.rect_transform.real_size - bounding_box_size), bounding_box_size)
        
        self._r_rect = Rectangle2(self.ui_object._bounding_box.pos + dir_normal * radius, (Vector2(2, 2)) * radius, Color(60, 60, 60))
        self._ext_end_circles = (
            Circle(radius, self.ui_object._bounding_box.pos + Vector2(1, 1) * radius, Color(60, 60, 60)),
            Circle(radius, self.ui_object._bounding_box.pos + (Vector2(1, 1) + dir_normal * 2) * radius, Color(60, 60, 60))
        )
        self._r_value_circle_pos = (
            self.ui_object._bounding_box.pos + Vector2(1, 1) * radius + dir_normal * 1,
            self.ui_object._bounding_box.pos + (Vector2(1, 1) + dir_normal * 2) * radius - dir_normal * 1
        )
        self._r_value_circle = Circle(radius - self.knob_margin * min_size, Vector2(-1, -1), self.knob_color)

        #label_bounding_box pos is in SS and size is in SC
        label_bounding_box = Rect(self.ui_object.rect_transform.real_position + (((dir_normal * -1) + alignment_v_mul_normal) * -1).mul_comp(bounding_box_size) + self.label_margin.mul_comp(self.ui_object.rect_transform.real_size), SS_to_SC(self.ui_object.rect_transform.real_size - self.ui_object._bounding_box.size.mul_comp(dir_normal) - self.label_margin.mul_comp(self.ui_object.rect_transform.real_size) * 2))

        self.label_recalculate(label_bounding_box)
        self.toggle_changed() # updating depending on the values

    def get_toggled_color(self):
        if self.ui_object.toggled:
            return self.toggled_color
        else:
            return self.color

    def get_toggled_circle_pos(self):
        if self.ui_object.toggled:
            return self._r_value_circle_pos[1]
        else:
            return self._r_value_circle_pos[0]

    def toggle_changed(self):
        color = self.get_toggled_color()
        self._r_value_circle.pos = self.get_toggled_circle_pos()
        self._r_rect.color = color
        self._ext_end_circles[0].color = color
        self._ext_end_circles[1].color = color

    def render(self):
        Renderer.render_rect(self._r_rect, FillMode.FILL)
        Renderer.render_circle(self._ext_end_circles[0])
        Renderer.render_circle(self._ext_end_circles[1])
        Renderer.render_circle(self._r_value_circle)
        if self.do_render_text:
            self.label_model.render()

class UIItemScrollViewModel(UIModel):
    __slots__=("color",
               "margin",
               "text_scalex",
               "font",
               "font_color",
               "slider_scalex",
               "item_size",
               "item_color",
               "item_font_color",
               "item_margin",
               "item_spacing",
               "render_index_number",
               "_rect_render",
               "_font_size",
               "_item_rects",
               "_item_labels",
               "_index_labels")
    def __init__(self, render_index_number=True, color=Color(70, 70, 70), margin=Vector2(0.05, 0.075), slider_scalex=0.04, text_scalex=0.06, item_size=Vector2(0.14, 0.06), item_margin=Vector2(0.01, 0.01), item_color=Color(100, 100, 100), item_spacing=0.04, font_color=Color(240, 240, 240), item_font_color=Color(240, 240, 240), font=Renderer.DEFAULT_FONT):
        super().__init__()
        self.color = color
        self.margin = margin
        self.font = font
        self.font_color = font_color
        self.slider_scalex = slider_scalex
        self.font_color = font_color
        self.item_font_color = item_font_color
        self.item_size = item_size
        self.render_index_number = render_index_number
        self.item_spacing = item_spacing
        self.item_color = item_color
        self.text_scalex = text_scalex
        self.item_margin = item_margin
        self._rect_render = None
        self._font_size = None
        self._item_labels = []
        self._index_labels = []

    def recalculate(self):
        # Getting Scaled_size and calculated_margin
        scaled_size = self.ui_object.rect_transform.size.mul_comp(self.ui_object.rect_transform.scale)
        calculated_margin = scaled_size.mul_comp(self.margin)
        item_spacing = scaled_size.y * self.item_spacing
        # Base rect
        self._rect_render = Rectangle2(self.ui_object.rect_transform.real_position, self.ui_object.rect_transform.real_size, self.color)
        # Scroll bar
        scroll_bar_size = Vector2(scaled_size.x * self.slider_scalex, self.ui_object.rect_transform.size.y - (calculated_margin.y * 2))
        self.ui_object._scroll_bar.rect_transform = RectTransform(Vector2(scaled_size.x - calculated_margin.x * 0.5 - scroll_bar_size.x, calculated_margin.y) + self.ui_object.rect_transform.position, self.ui_object.rect_transform.scale.copy(), scroll_bar_size)
        self.ui_object._scroll_bar.rect_transform.recalculate()
        self.ui_object._scroll_bar.model.recalculate()
        # Getting fit_in_size and scaled_size
        fit_in_size = Vector2(0, 0)
        if self.render_index_number:
            fit_in_size = scaled_size - Vector2(calculated_margin.x * 2 + self.ui_object._scroll_bar.rect_transform.size.x + self.text_scalex * scaled_size.x, calculated_margin.y * 2)
        else:
            fit_in_size = scaled_size - Vector2(calculated_margin.x * 2 + self.ui_object._scroll_bar.rect_transform.size.x, calculated_margin.y * 2)
        # Getting items scale
        item_scale = Vector2(1, 1) * fit_in_size.div_comp(self.item_size).min_comp()
        # Getting item count to render and total item count
        item_count = len(self.ui_object.elements)
        item_fit_in_count = int(fit_in_size.y / (self.item_size.y * item_scale.y + item_spacing))
        if item_fit_in_count > item_count:
            item_fit_in_count = item_count
        # Getting which item to render from the slider's value
        item_render_index = int((self.ui_object._scroll_bar.min_max_value.y - self.ui_object._scroll_bar.value) * (item_count - item_fit_in_count + 1))
        self.ui_object._r_render_index = item_render_index
        # Setting rectangles to render
        self.ui_object._r_item_rects = []
        self._item_labels = []
        final_item_size = self.item_size.mul_comp(item_scale)
        calculated_item_margin = final_item_size.mul_comp(self.item_margin)
        current_pos = Vector2(calculated_margin.x, scaled_size.y - calculated_margin.y - final_item_size.y) + self.ui_object.rect_transform.position
        if self.render_index_number:
            current_pos.x += self.text_scalex * scaled_size.x
            self._index_labels = []
        final_item_layout_margin = 0
        final_index_text_size = Vector2(self.text_scalex * scaled_size.x, final_item_size.y)
        if item_fit_in_count != 1:
            final_item_spacin = (item_fit_in_count * item_spacing) / (item_fit_in_count - 1)
        for i in range(item_render_index, item_render_index + item_fit_in_count):
            self.ui_object._r_item_rects.append(Rectangle2(SC_to_SS(current_pos.copy()), SC_to_SS(final_item_size.copy()), self.item_color))
            self._item_labels.append(self.LabelStruct(current_pos + calculated_item_margin, final_item_size - calculated_item_margin * 2, self.ui_object.elements[i].text, self.font))
            if self.render_index_number:
                self._index_labels.append(self.LabelStruct(current_pos - Vector2(final_index_text_size.x + calculated_margin.x * 0.5, 0), final_index_text_size, str(i), self.font))
            current_pos -= Vector2(0, item_spacing + final_item_size.y)
        self._rect_render = Rectangle2(self.ui_object.rect_transform.real_position, self.ui_object.rect_transform.real_size, self.color)
        self.ui_object._bounding_box = Rect(self._rect_render.pos.copy(), self._rect_render.size.copy())

    def render(self):
        Renderer.render_rect(self._rect_render)
        for i, label in enumerate(self._item_labels):
            Renderer.render_rect(self.ui_object._r_item_rects[i])
            Renderer.render_text(label.text, label._font_size, self.font_color, label._r_position, self.font)
            if self.render_index_number:
                index_label = self._index_labels[i]
                Renderer.render_text(index_label.text, index_label._font_size, self.font_color, index_label._r_position, self.font)

    class LabelStruct:
        __slots__=("text",
                   "_r_position",
                   "_font_size",
                   "_real_text_size",
                   "font")
        def __init__(self, position, size, text, font):
            self.text = text
            self._font_size = Renderer.get_optimal_font_size(self.text, size, font)
            text_size = Renderer.get_text_size(self.text, self._font_size, font)
            position += (size - text_size) / 2
            self._r_position = SC_to_SS(position)

class UIRectModel(UIModel):
    __slots__=("_r_rect",
               "do_render",
               "color",
               "fill_mode",
               "width")
    def __init__(self, do_render=True, color=Color(), fill_mode=FillMode.FILL, width=0.005):
        super().__init__()
        self._r_rect = None
        self.do_render = do_render
        self.color = color
        self.fill_mode = fill_mode
        self.width = width

    def recalculate(self):
        self._r_rect = Rectangle2(self.ui_object.rect_transform.real_position, self.ui_object.rect_transform.real_size, self.color)
        self.ui_object._bounding_box = Rect(self.ui_object.rect_transform.real_position.copy(), self.ui_object.rect_transform.real_size.copy())

    def render(self):
        if self.do_render:
            Renderer.render_rect(self._r_rect, self.fill_mode, self.width)

class UIRectSpriteModel(UIModel):
    __slots__=("do_render",
               "sprite",
               "sprite_fit_mode")
    def __init__(self, sprite, do_render=True, sprite_fit_mode=SpriteFitMode.FIT):
        super().__init__()
        self.do_render = do_render
        self.sprite = sprite
        self.sprite_fit_mode = sprite_fit_mode

    def start(self):
        super().start()
        self.sprite.load()

    def recalculate(self):
        self.ui_object._bounding_box = self.sprite.set_to_fit_in_box(Rect(self.ui_object.rect_transform.real_position.copy(), self.ui_object.rect_transform.real_size.copy()), self.sprite_fit_mode)

    def render(self):
        if self.do_render:
            Renderer.render_sprite(self.sprite)

class UIDropdownModel(UIModel):
    __slots__=("_r_dropdown_rect",
               "item_background_color",
               "item_font_color",
               "margin",
               "color",
               "arrow_color",
               "selected_color",
               "font_color",
               "font",
               "fill_mode",
               "width",
               "arrow_width",
               "arrow_margin",
               "_r_width",
               "_r_arrow_lines",
               "_r_arrow_width",
               "_r_current_item_text_pos",
               "_r_current_item_font_size",
               "_r_item_font_size")
    def __init__(self, margin=Vector2(0.06, 0.09), arrow_margin=0.25, color=Color(75, 75, 75), selected_color=Color(90, 90, 90), arrow_color=Color(), item_background_color=Color(50, 50, 50), font_color=Color(240, 240, 240), item_font_color=Color(225, 225, 225), arrow_width=0.1, font=Renderer.DEFAULT_FONT, fill_mode=FillMode.FILL, width=0.1):
        super().__init__()
        self._r_dropdown_rect = None
        self.color = color
        self.fill_mode = fill_mode
        self.width = width
        self.item_background_color = item_background_color
        self._r_width = None
        self.selected_color = selected_color
        self.margin = margin
        self.arrow_width = arrow_width
        self.arrow_color = arrow_color
        self._r_arrow_lines = None
        self._r_arrow_width = None
        self._r_current_item_text_pos = None
        self._r_current_item_font_size = None
        self._r_item_font_size = None
        self.font = font
        self.font_color = font_color
        self.arrow_margin = arrow_margin
        self.item_font_color = item_font_color

    def recalculate(self):
        super().recalculate()
        size = Vector2.scaler(self.ui_object.rect_transform.real_size.y)
        arrow_box_pos = self.ui_object.rect_transform.real_position + self.ui_object.rect_transform.real_size - size
        margin = self.ui_object.rect_transform.real_size.mul_comp(self.margin)
        arrow_margin = size * self.arrow_margin
        normal_x = Vector2(1, 0)
        normal_y = Vector2(0, 1)
        self._r_arrow_lines = (
            (
                (arrow_box_pos + arrow_margin.mul_comp(normal_y) + normal_x.mul_comp(size / 2), arrow_box_pos + Vector2(arrow_margin.x, -arrow_margin.y) + normal_y.mul_comp(size)),
                (arrow_box_pos + arrow_margin.mul_comp(normal_y) + normal_x.mul_comp(size / 2), arrow_box_pos + size - arrow_margin)
            ),
            (
                (arrow_box_pos - arrow_margin.mul_comp(normal_y) + normal_x.mul_comp(size / 2) + normal_y.mul_comp(size), arrow_box_pos + Vector2(-arrow_margin.x, arrow_margin.y) + normal_x.mul_comp(size)),
                (arrow_box_pos - arrow_margin.mul_comp(normal_y) + normal_x.mul_comp(size / 2) + normal_y.mul_comp(size), arrow_box_pos + arrow_margin)
            ),
            (arrow_box_pos + size.mul_comp(normal_y) - arrow_margin.mul_comp(Vector2(0, 1)) - Vector2(1, 0) * self.arrow_width, arrow_box_pos + arrow_margin.mul_comp(Vector2(0, 1)) - Vector2(1, 0) * self.arrow_width)
        )

        self.current_item_changed()
        self._r_dropdown_rect = Rectangle2(self.ui_object.rect_transform.real_position.copy(), self.ui_object.rect_transform.real_size.copy(), self.color)
        self._r_width = int(self.width * self.ui_object.rect_transform.real_size.min_comp())
        self._r_arrow_width = int(self.arrow_width * size.x)
        self.ui_object._bounding_box = Rect(self.ui_object.rect_transform.real_position.copy(), self.ui_object.rect_transform.real_size.copy())

    def current_item_changed(self):
        arrow_box_size = Vector2.scaler(self.ui_object.rect_transform.real_size.y)
        margin = self.ui_object.rect_transform.real_size.mul_comp(self.margin)
        fit_in_size = SS_to_SC(self.ui_object.rect_transform.real_size - margin * 2 - arrow_box_size.mul_comp(Vector2(1, 0)))
        self._r_current_item_font_size = Renderer.get_optimal_font_size(self.ui_object.get_current_item().text, fit_in_size, self.font)
        final_text_size = SC_to_SS(Renderer.get_text_size(self.ui_object.get_current_item().text, self._r_current_item_font_size, self.font))
        final_margin = (self.ui_object.rect_transform.real_size - arrow_box_size.mul_comp(Vector2(1, 0)) - final_text_size) / 2
        self._r_current_item_text_pos = self.ui_object.rect_transform.real_position + final_margin

    def on_select(self):
        self._r_dropdown_rect.color = self.selected_color

    def on_deselect(self):
        self._r_dropdown_rect.color = self.color

    def render(self):
        Renderer.render_rect(self._r_dropdown_rect, self.fill_mode, self._r_width)
        if self.ui_object.selected:
            Renderer.render_line(self._r_arrow_lines[1][0][0], self._r_arrow_lines[1][0][1], self.arrow_color, self._r_arrow_width)
            Renderer.render_line(self._r_arrow_lines[1][1][0], self._r_arrow_lines[1][1][1], self.arrow_color, self._r_arrow_width)
        else:
            Renderer.render_line(self._r_arrow_lines[0][0][0], self._r_arrow_lines[0][0][1], self.arrow_color, self._r_arrow_width)
            Renderer.render_line(self._r_arrow_lines[0][1][0], self._r_arrow_lines[0][1][1], self.arrow_color, self._r_arrow_width)
        Renderer.render_line(self._r_arrow_lines[2][0], self._r_arrow_lines[2][1], self.arrow_color, int(self._r_arrow_width * 0.8))
        Renderer.render_text(self.ui_object.get_current_item().text, self._r_current_item_font_size, self.font_color, self._r_current_item_text_pos, self.font)

### End Models###
################
### Core ###

class UIObject:
    __slots__=("is_selectable", # If we click on the object and it is selectable the object is going to enter a certain state till we click somewhere else
               "selected", # if we are in that state
               "is_clickable", # If the engine checks if the click is in the object
               "rect_transform",
               "priority",
               "model", # The model of the object for rendering
               "function_set")
    def __init__(self, is_selectable=True, rect_transform=RectTransform(), priority=0, model=UIModel()):
        self.rect_transform = rect_transform
        self.priority = priority
        self.selected = False
        self.is_selectable = is_selectable
        self.model = model
        self.function_set = UIFunctionSet()
        self.is_clickable=True

    def awake(self):
        self.rect_transform.awake(self)
        self.model.awake(self)

    def start(self):
        """ Need to be called by child classes """
        self.selected = False
        self.model.start()
        self.recalculate()
        self.function_set.on_start(self)
        self.function_set.set_style(self)

    def update(self):
        """ Called only if selected """
        self.function_set.on_update(self)

    def render(self):
        self.function_set.on_render(self)
        self.model.render()

    def check_click(self, click):
        """ Returns true if the click is in the boundaries of the object """
        return False

    def on_select(self, click):
        self.function_set.on_select(self, click)

    def on_deselect(self):
        self.function_set.on_deselect(self)
        self.selected = False

    def stop(self):
        self.function_set.on_stop(self)

    def recalculate(self):
        self.rect_transform.recalculate()
        self.model.recalculate()

class UIButton(UIObject):
    __slots__=("text",
               "_bounding_box")
    def __init__(self, rect_transform=RectTransform(), priority=0, text="Button", model=UIButtonModel()):
        super().__init__(is_selectable=False, rect_transform=rect_transform, priority=priority, model=model)
        self.text = text
        self._bounding_box = Rect()

    def check_click(self, click):
        return click.x > self._bounding_box.pos.x and click.x < self._bounding_box.pos.x + self._bounding_box.size.x and click.y > self._bounding_box.pos.y and click.y < self._bounding_box.pos.y + self._bounding_box.size.y

class UISlider(UIObject):
    __slots__=("value",
               "min_max_value",
               "modifiable",
               "is_horizontal")
    def __init__(self, rect_transform=RectTransform(), min_max_value = Vector2(0, 1), value = 0, model=UISliderModel(), priority=0, is_horizontal=True):
        super().__init__(is_selectable=False, rect_transform=rect_transform, priority=priority, model=model)
        self.min_max_value = min_max_value
        self.value = value
        self.is_horizontal = is_horizontal

    def check_click(self, click):
        return self.model.knob_model.check_click(click) or (click.x > self.rect_transform.real_position.x and click.x < self.rect_transform.real_position.x + self.rect_transform.real_size.x and click.y > self.rect_transform.real_position.y and click.y < self.rect_transform.real_position.y + self.rect_transform.real_size.y)

    def on_select(self, click):
        if not (click.x > self.rect_transform.real_position.x and click.x < self.rect_transform.real_position.x + self.rect_transform.real_size.x and click.y > self.rect_transform.real_position.y and click.y < self.rect_transform.real_position.y + self.rect_transform.real_size.y):
            return
        if self.is_horizontal:
            self.value = ((click.x - self.rect_transform.real_position.x) /  self.rect_transform.real_size.x * (self.min_max_value.y - self.min_max_value.x)) + self.min_max_value.x
        else:
            self.value = ((click.y - self.rect_transform.real_position.y) /  self.rect_transform.real_size.y * (self.min_max_value.y - self.min_max_value.x)) + self.min_max_value.x
        self.model.recalculate()
        super().on_select(click)

class UILabel(UIObject):
    __slots__=("text")
    def __init__(self, rect_transform=RectTransform(), priority=0, text="Label", model=UILabelModel()):
        super().__init__(is_selectable=False, rect_transform=rect_transform, priority=priority, model=model)
        self.is_clickable = False
        self.text = text

class UIToggleButton(UIObject):
    __slots__=("text",
               "toggled",
               "_bounding_box")
    def __init__(self, rect_transform=RectTransform(), toggled=True, priority=0, text="Toggle", model=UIToggleButtonModel()):
        super().__init__(is_selectable=False, rect_transform=rect_transform, priority=priority, model=model)
        self.text = text
        self._bounding_box = Rect()
        self.toggled = toggled
    
    def check_click(self, click):
        return click.x > self._bounding_box.pos.x and click.x < self._bounding_box.pos.x + self._bounding_box.size.x and click.y > self._bounding_box.pos.y and click.y < self._bounding_box.pos.y + self._bounding_box.size.y

    def on_select(self, click):
        self.toggled = not self.toggled
        self.model.toggle_changed()
        super().on_select(click)

class UIObjectsGroupLayout:
    __slots__=("elements",
               "rect_transform",
               "do_vertical_stacking",
               "spacing",
               "do_center_objects",
               "keep_aspect_ratio")
    def __init__(self, rect_transform=RectTransform(), elements=[], spacing=Vector2(0.005, 0.05), do_vertical_stacking=True, do_center_objects=True, keep_aspect_ratio=True):
        self.elements = elements
        self.rect_transform = rect_transform
        self.do_vertical_stacking = do_vertical_stacking
        self.spacing = spacing
        self.do_center_objects = do_center_objects
        self.keep_aspect_ratio = keep_aspect_ratio

    def _get_total_elements_size(self):
        """ Returns the full size horizontally and vertically for all the elements added together """
        size = Vector2()
        for element in self.elements:
            size += element.rect_transform.size
        return size

    def _get_max_size_from_individual_elements(self):
        """ Returns the maximum size by testing each element in each direction """
        max_size = Vector2()
        for element in self.elements:
            max_size.x = max(element.rect_transform.size.x, max_size.x)
            max_size.y = max(element.rect_transform.size.y, max_size.y)
        return max_size

    def recalculate(self):
        """ Recalculates all the positions and sizes for the elements : Needs to be called when adding new elements or removing them || or when changing the layout """
        # TODO: method could be more compact
        total_size = self._get_total_elements_size()
        max_size = self._get_max_size_from_individual_elements()
        spacing = self.spacing.mul_comp(self.rect_transform.size.mul_comp(self.rect_transform.scale))
        fit_in_size = self.rect_transform.size.mul_comp(self.rect_transform.scale) - (spacing * (len(self.elements) - 1))
        scale = Vector2(1, 1)
        v_10 = Vector2(1, 0)
        v_01 = Vector2(0, 1)
        if self.keep_aspect_ratio:
            offset = Vector2(0, 0)
            if self.do_vertical_stacking:
                n_scale = min(fit_in_size.x / max_size.x, fit_in_size.y / total_size.y)
                scale *= n_scale
                current_pos = self.rect_transform.position.copy()
                for element in reversed(self.elements): # reversed to have the last element at the bottom
                    element.rect_transform.scale = scale
                    if self.do_center_objects:
                        offset = ((self.rect_transform.size - element.rect_transform.size.mul_comp(element.rect_transform.scale)) / 2).mul_comp(v_10)
                    element.rect_transform.position = current_pos + offset
                    element.recalculate()
                    current_pos += (spacing + element.rect_transform.size.mul_comp(element.rect_transform.scale)).mul_comp(v_01)
            else:
                n_scale = min(fit_in_size.x / total_size.x, fit_in_size.y / max_size.y)
                scale *= n_scale
                current_pos = self.rect_transform.position.copy()
                for element in self.elements:
                    element.rect_transform.scale = scale
                    if self.do_center_objects:
                        offset = ((self.rect_transform.size - element.rect_transform.size.mul_comp(element.rect_transform.scale)) / 2).mul_comp(v_01)
                    element.rect_transform.position = current_pos + offset
                    element.rect_transform.recalculate()
                    element.model.recalculate()
                    current_pos += (spacing + element.rect_transform.size.mul_comp(element.rect_transform.scale)).mul_comp(v_10)
        else:
            item_count = len(self.elements)
            if self.do_vertical_stacking:
                size_y = fit_in_size.y / item_count
                current_pos = self.rect_transform.position.copy()
                for element in reversed(self.elements):
                    element.rect_transform.scale = Vector2(self.rect_transform.size.x * self.rect_transform.scale.x, size_y).div_comp(element.rect_transform.size)
                    element.rect_transform.position = current_pos.copy()
                    element.recalculate()
                    current_pos += (spacing + element.rect_transform.size.mul_comp(element.rect_transform.scale)).mul_comp(v_01)
            else:            
                item_count = len(self.elements)
                size_x = fit_in_size.x / item_count
                current_pos = self.rect_transform.position.copy()
                for element in reversed(self.elements):
                    element.rect_transform.scale = Vector2(size_x, self.rect_transform.size.y * self.rect_transform.scale.y).div_comp(element.rect_transform.size)
                    element.rect_transform.position = current_pos.copy()
                    element.recalculate()
                    current_pos += (spacing + element.rect_transform.size.mul_comp(element.rect_transform.scale)).mul_comp(v_10)

class UIItem:
    __slots__=("id",
               "value",
               "text")
    def __init__(self, value, id, text="item"):
        self.id = id
        self.value = value
        self.text = text

class UIItemScrollView(UIObject):
    __slots__=("_scroll_bar",
               "is_vertical",
               "elements",
               "_r_item_rects",
               "_r_render_index",
               "call_function",
               "_bounding_box")
    def __init__(self, call_function, elements=[], rect_transform=RectTransform(), priority=0, model=UIItemScrollViewModel(), slider_model=UISliderModel(Color(42, 42, 42), UIKnobRoundModel())):
        """
        @param: call_function is the function that is gonna be called when an item is clicked
        """
        super().__init__(is_selectable=False, rect_transform=rect_transform, priority=priority, model=model)
        self.elements = elements
        self._r_item_rects = []
        self._r_render_index = None
        self.call_function = call_function
        self._scroll_bar = UISlider(RectTransform(), Vector2(0, 1), 1, slider_model, self.priority, False)
        self._scroll_bar.function_set.on_select = self.on_changed_value
        self._bounding_box = Rect()

    def check_click(self, click):
        return click.x > self._bounding_box.pos.x and click.x < self._bounding_box.pos.x + self._bounding_box.size.x and click.y > self._bounding_box.pos.y and click.y < self._bounding_box.pos.y + self._bounding_box.size.y

    def on_select(self, click):
        if self._scroll_bar.check_click(click):
            self._scroll_bar.on_select(click)
            super().on_select(click)
        else:
            super().on_select(click)
            for i, item_rect in enumerate(self._r_item_rects):
                if click.x > item_rect.pos.x and click.x < item_rect.pos.x + item_rect.size.x and click.y > item_rect.pos.y and click.y < item_rect.pos.y + item_rect.size.y:
                    self.call_function(self.elements[self._r_render_index + i])
        
    def recalculate(self):
        super().recalculate()
        self._scroll_bar.recalculate()

    def awake(self):
        self._scroll_bar.awake()
        super().awake()

    def start(self):
        self._scroll_bar.start()
        super().start()

    def render(self):
        super().render()
        self._scroll_bar.render()

    def on_changed_value(self, slider, click):
        self.model.recalculate()

class UIRect(UIObject):
    __slots__=("block_clicks",
               "_bounding_box")
    def __init__(self, rect_transform=RectTransform(), priority=0, block_clicks=True, model=UIRectModel()):
        super().__init__(is_selectable=False, rect_transform=rect_transform, priority=priority, model=model)
        self.block_clicks = block_clicks

    def check_click(self, click):
        if not self.block_clicks:
            return False
        return click.x > self._bounding_box.pos.x and click.x < self._bounding_box.pos.x + self._bounding_box.size.x and click.y > self._bounding_box.pos.y and click.y < self._bounding_box.pos.y + self._bounding_box.size.y

class UIDropdown(UIObject):
    # Selection and deselection is held really poorly + an upgrade to have the model manage everything in the rendering and not use a UIItemScrollView would be great addition
    # TODO: Refactor, make cleaner code, for instance the mess can cause plenty of errors
    #  + A refactor of the UI selection system could be good, like clicking on some part of an object deselects/stays selected, depending on certain stuff
    __slots__=("callback_function",
               "_bounding_box",
               "_ui_item_scroll_view",
               "__ui_scroll_view_on_select_fired",
               "__list_items",
               "__current_item",
               "__scene")
    def __init__(self, scene, callback_function, rect_transform=RectTransform(), priority=0, list_items=(UIItem(None, "default_item", "No item selected"),UIItem(42, "default_item2", "another item")), item_index=0, model=UIDropdownModel(), slider_model=UISliderModel(Color(42, 42, 42), UIKnobRoundModel(0.8, Color(140, 140, 140)))):
        super().__init__(is_selectable=True, rect_transform=rect_transform, priority=priority, model=model)
        self._bounding_box = Rect()
        pos = Vector2(self.rect_transform.position.x, clamp(self.rect_transform.position.y - self.rect_transform.size.y * 6, 0, self.rect_transform.position.y - self.rect_transform.size.y * 1.5))
        self._ui_item_scroll_view = UIItemScrollView(self.clicked_on_item, [], RectTransform(pos, self.rect_transform.scale.copy(), Vector2(self.rect_transform.size.x, self.rect_transform.position.y - pos.y)),
                                                     self.priority, UIItemScrollViewModel(False, self.model.item_background_color, self.model.margin.mul_comp(Vector2(2, 0)), 0.07, 0, self.rect_transform.size - Vector2(1, 0) * self.rect_transform.size.y, item_color=self.model.item_background_color, item_spacing=0, font_color=self.model.item_font_color), slider_model)
        self.set_list_items(list_items, item_index)
        self.__scene = scene
        scene.add_ui_object(self._ui_item_scroll_view)
        self._ui_item_scroll_view.function_set.on_start = self.ui_scroll_view_start_call_back
        self._ui_item_scroll_view.function_set.on_select = self.ui_scroll_view_on_select_callback
        self.__ui_scroll_view_on_select_fired = False
        self.callback_function = callback_function

    def clicked_on_item(self, item):
        self.set_current_item_by_id(item.id)
        self.__ui_scroll_view_on_select_fired = False
        self.__scene.deselect_current_ui_object()
        self.callback_function(self, item)

    def set_list_items(self, list_items=(UIItem(None, "default_item", "No items"),), item_index=0):
        assert list_items, "list_items cannot be empty"
        self.__list_items = list_items
        item_index = clamp(item_index, -len(list_items), len(list_items) - 1)
        self.__current_item = self.__list_items[item_index]
        self.update_ui_scroll_view_elements()

    def update_ui_scroll_view_elements(self):
        self._ui_item_scroll_view.elements = list(self.__list_items)
        self._ui_item_scroll_view.elements.remove(self.__current_item)

    def get_list_items(self):
        return self.__list_items

    def set_current_item_by_index(self, index):
        index = clamp(index, -len(self.__list_items), len(self.__list_items) - 1)
        self.__current_item = self.__list_items[index]
        self.model.current_item_changed()
        self.update_ui_scroll_view_elements()
        self._ui_item_scroll_view.recalculate()

    def set_current_item_by_id(self, id):
        for item in self.__list_items:
            if item.id == id:
                self.__current_item = item
                self.model.current_item_changed()
                self.update_ui_scroll_view_elements()
                self._ui_item_scroll_view.recalculate()
                return
        raise Exception("The id does not match with any item of list_items")

    def get_current_item(self):
        return self.__current_item

    def check_click(self, click):
        return (click.x > self._bounding_box.pos.x and click.x < self._bounding_box.pos.x + self._bounding_box.size.x and click.y > self._bounding_box.pos.y and click.y < self._bounding_box.pos.y + self._bounding_box.size.y)

    def ui_scroll_view_start_call_back(self, ui_scroll_view):
        self.__scene.set_active(self._ui_item_scroll_view, False)
      
    def ui_scroll_view_on_select_callback(self, ui_scroll_view, click):
        self.__ui_scroll_view_on_select_fired = True

    def on_select(self, click):
        self.model.on_select()
        self.__scene.set_active(self._ui_item_scroll_view, True)
        super().on_select(click)

    def on_deselect(self):
        # Check to see which item has been selected
        if self.__ui_scroll_view_on_select_fired:
            self.__scene.select_ui_object(self)
            self.__ui_scroll_view_on_select_fired = False
        else:
            self.__scene.set_active(self._ui_item_scroll_view, False)
            self.model.on_deselect()
            super().on_deselect()

### End Core ###