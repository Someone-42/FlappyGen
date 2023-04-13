from Core import *
from RendererCore import *
from UICore import *
import Renderer
from statistics import mean
from Environments import *
from FsManager import get_save_files

class FBUI(GameObject2):
    __slots__=("game_manager",
               "slider_speed",
               "slider_scale",
               "btn_quit",
               "btn_save",
               "btn_restart",
               "rect_ui",
               "font_pos",
               "btn_load",
               "btn_options",
               "info_labels",
               "info_labels_base_text",
               "info_labels_group_layout",
               "separation_lines",
               "separation_lines_color",
               "options_ui_click_blocker",
               "options_label",
               "options_back_button",
               "load_ui_click_blocker",
               "load_saves_scroll_view",
               "load_menu_label",
               "load_back_button",
               "load_menu_load_button",
               "load_cancel_button",
               "save_item_selected",
               "load_menu_item_label",
               "base_load_menu_item_label_texts")
    def __init__(self, game_manager, transform=Transform2(), priority=16):
        super().__init__(transform=transform, priority=priority)
        self.game_manager = game_manager
        width = get_engine().WIDTH - get_engine().WIDTH * FBEnvironment.render_part
        ui_scale_x = 1 - FBEnvironment.render_part
        self.separation_lines_color = get_colors("midtone").copy()
        self.rect_ui = Rectangle2(Vector2(0, 0), Vector2(width, get_engine().HEIGHT), get_colors("darkest"))
        self.separation_lines = (Vector2(0, get_engine().HEIGHT * 0.18), Vector2(width-1, get_engine().HEIGHT * 0.18), 
                                 Vector2(0, get_engine().HEIGHT * 0.67), Vector2(width-1, get_engine().HEIGHT * 0.67))
        self.btn_quit = UIButton(RectTransform(Vector2(0.325 * ui_scale_x, 0.0525), Vector2(1, 1), Vector2(0.35 * ui_scale_x, 0.08)), 
                                10, "Leave", UIButtonModel(Vector2(0.15, 0.1), get_colors("tone_0"), get_colors("tone_0"),
                                                        FillMode.OUTLINE, 0.002, get_fonts("button")))
        self.btn_save = UIButton(RectTransform(Vector2(0.575 * ui_scale_x, 0.225), Vector2(1, 1), Vector2(0.3 * ui_scale_x, 0.075)), 
                                5, "Save", UIButtonModel(Vector2(0, 0.15), get_colors("tone_3"), get_colors("tone_3"),
                                                        FillMode.OUTLINE, 0.002, get_fonts("button")))
        self.btn_options = UIButton(RectTransform(Vector2(0.125 * ui_scale_x, 0.225), Vector2(1, 1), Vector2(0.3 * ui_scale_x, 0.075)), 
                                5, "Options", UIButtonModel(Vector2(0, 0.15), get_colors("tone_1"), get_colors("tone_1"), 
                                                        FillMode.OUTLINE, 0.002, get_fonts("button")))
        self.btn_load = UIButton(RectTransform(Vector2(0.575 * ui_scale_x, 0.35), Vector2(1, 1), Vector2(0.3 * ui_scale_x, 0.075)), 
                                5, "Load", UIButtonModel(Vector2(0, 0.15), get_colors("tone_3"), get_colors("lightest"),
                                                        FillMode.FILL, 0.002, get_fonts("button")))
        self.btn_restart = UIButton(RectTransform(Vector2(0.125 * ui_scale_x, 0.35), Vector2(1, 1), Vector2(0.3 * ui_scale_x, 0.075)), 
                                5, "Restart", UIButtonModel(Vector2(0, 0.15), get_colors("tone_1"), get_colors("lightest"), 
                                                        FillMode.FILL, 0.002, get_fonts("button")))
        self.slider_scale = UISlider(RectTransform(Vector2(0.125 * ui_scale_x, 0.5), Vector2(1, 1), Vector2(0.75 * ui_scale_x, 0.014)), Vector2(0, 8), 1, UISliderModel(get_colors("darker"), UIKnobRoundModel(1.1, get_colors("tone_4"))), 4, True)
        self.slider_speed = UISlider(RectTransform(Vector2(0.125 * ui_scale_x, 0.58), Vector2(1, 1), Vector2(0.75 * ui_scale_x, 0.014)), Vector2(100, 1000), 140, UISliderModel(get_colors("darker"), UIKnobRoundModel(1.1, get_colors("tone_4"))), 4, True)
        
        self.info_labels_base_text = (
            "Score : ",
            "Birds left : ",
            "Generation : ",
            "FPS render : ",
            "FPS updates : "
        )

        self.info_labels = (
            UILabel(RectTransform(), 8, self.info_labels_base_text[0], UILabelModel(get_colors("light"), AxisAlignType.LEFT, AxisAlignType.CENTER, get_fonts("normal"))),
            UILabel(RectTransform(), 8, self.info_labels_base_text[1], UILabelModel(get_colors("light"), AxisAlignType.LEFT, AxisAlignType.CENTER, get_fonts("normal"))),
            UILabel(RectTransform(), 8, self.info_labels_base_text[2], UILabelModel(get_colors("light"), AxisAlignType.LEFT, AxisAlignType.CENTER, get_fonts("normal"))),
            UILabel(RectTransform(), 8, self.info_labels_base_text[3], UILabelModel(get_colors("light"), AxisAlignType.LEFT, AxisAlignType.CENTER, get_fonts("normal"))),
            UILabel(RectTransform(), 8, self.info_labels_base_text[4], UILabelModel(get_colors("light"), AxisAlignType.LEFT, AxisAlignType.CENTER, get_fonts("normal")))
        )
        game_manager.fb_scene.add_ui_object(self.info_labels[0])
        game_manager.fb_scene.add_ui_object(self.info_labels[1])
        game_manager.fb_scene.add_ui_object(self.info_labels[2])
        game_manager.fb_scene.add_ui_object(self.info_labels[3])
        game_manager.fb_scene.add_ui_object(self.info_labels[4])
        # size of elements must not be zero
        self.info_labels_group_layout = UIObjectsGroupLayout(RectTransform(Vector2(0.05 * ui_scale_x, 0.69), Vector2(1, 1), Vector2(ui_scale_x * 0.9, 1 - 0.7)), self.info_labels, Vector2(0, 0.02), True, False, False)

        self.options_ui_click_blocker = UIRect(RectTransform(Vector2(0, 0), Vector2(1, 1), Vector2(1, 1)), 128, True, UIRectModel(False))
        self.options_label = UILabel(RectTransform(Vector2(0.05, 0.5), Vector2(1, 1), Vector2(0.9, 0.2)), 130, "The options menu is not available yet", UILabelModel(get_colors("tone_0"), AxisAlignType.CENTER, AxisAlignType.CENTER, get_fonts("normal")))
        self.options_back_button = UIButton(RectTransform(Vector2(0.4, 0.075), Vector2(1, 1), Vector2(0.2, 0.08)), 
                                            132, "Back", UIButtonModel(Vector2(0, 0.15), get_colors("tone_1"), get_colors("lightest"), 
                                                        FillMode.FILL, 0.002, get_fonts("button")))

        self.load_ui_click_blocker = UIRect(RectTransform(Vector2(0, 0), Vector2(1, 1), Vector2(1, 1)), 128, True, UIRectModel(True, get_colors("darkest")))
        self.load_saves_scroll_view = UIItemScrollView(self.save_item_clicked, [], RectTransform(Vector2(0, 0), Vector2(1, 1), Vector2(0.6, 1)), 132, 
                                                       UIItemScrollViewModel(True, get_colors("darkest"), Vector2(0.1, 0.1), 0.03, 0.06, Vector2(0.05, 0.01), 
                                                                             Vector2(0.1, 0.05), get_colors("tone_1"), 0.04, get_colors("light"), get_colors("lightest"), get_fonts("button")), 
                                                       UISliderModel(get_colors("darker"), UIKnobRoundModel(1.1, get_colors("tone_4"))))
        self.load_menu_label = UILabel(RectTransform(Vector2(0.65, 0.9), Vector2(1, 1), Vector2(0.3, 0.1)), 140, "Load menu", UILabelModel(get_colors("tone_3"), AxisAlignType.CENTER, AxisAlignType.CENTER, get_fonts("title")))
        self.load_back_button = UIButton(RectTransform(Vector2(0.675, 0.05), Vector2(1, 1), Vector2(0.25, 0.08)), 
                                            132, "Back", UIButtonModel(Vector2(0, 0.15), get_colors("tone_0"), get_colors("tone_0"), 
                                                        FillMode.OUTLINE, 0.002, get_fonts("button")))
        self.load_menu_load_button = UIButton(RectTransform(Vector2(0.675, 0.6), Vector2(1, 1), Vector2(0.25, 0.08)), 
                                                    132, "Load", UIButtonModel(Vector2(0, 0.15), get_colors("tone_3"), get_colors("lightest"), 
                                                                FillMode.FILL, 0.002, get_fonts("button")))
        self.load_cancel_button = UIButton(RectTransform(Vector2(0.675, 0.35), Vector2(1, 1), Vector2(0.25, 0.08)), 
                                                    132, "Cancel", UIButtonModel(Vector2(0, 0.15), get_colors("tone_4"), get_colors("lightest"), 
                                                                FillMode.FILL, 0.002, get_fonts("button")))
        self.base_load_menu_item_label_texts = ("<No item currently selected>",
                                                "Current item: ")
        self.load_menu_item_label = UILabel(RectTransform(Vector2(0.65, 0.75), Vector2(1, 1), Vector2(0.3, 0.1)), 140, self.base_load_menu_item_label_texts[0], UILabelModel(get_colors("light"), AxisAlignType.CENTER, AxisAlignType.CENTER, get_fonts("normal")))
        self.save_item_selected = None

        self.btn_quit.function_set.on_select = self.game_manager.quit
        self.btn_save.function_set.on_select = self.game_manager.save
        self.btn_restart.function_set.on_select = self.game_manager.restart_game
        self.btn_load.function_set.on_select = self.open_load_menu
        self.btn_options.function_set.on_select = self.open_options_menu
        self.load_back_button.function_set.on_select = self.close_load_menu

        self.slider_scale.function_set.on_select = self.game_manager.change_scale
        self.slider_speed.function_set.on_select = self.game_manager.change_speed

        game_manager.fb_scene.add_ui_object(self.slider_scale)
        game_manager.fb_scene.add_ui_object(self.slider_speed)
        game_manager.fb_scene.add_ui_object(self.btn_quit)
        game_manager.fb_scene.add_ui_object(self.btn_save)
        game_manager.fb_scene.add_ui_object(self.btn_options)
        game_manager.fb_scene.add_ui_object(self.btn_load)
        game_manager.fb_scene.add_ui_object(self.btn_restart)
        
        #Menus et trucs ui speciaux
        self.options_back_button.function_set.on_select = self.close_options_menu

        self.load_cancel_button.function_set.on_select = self.cancel_loading_clicked
        self.load_menu_load_button.function_set.on_select = self.load_item_clicked

        game_manager.fb_scene.add_ui_object(self.options_ui_click_blocker)
        game_manager.fb_scene.add_ui_object(self.options_label)
        game_manager.fb_scene.add_ui_object(self.options_back_button)
        game_manager.fb_scene.add_ui_object(self.load_ui_click_blocker)
        game_manager.fb_scene.add_ui_object(self.load_saves_scroll_view)
        game_manager.fb_scene.add_ui_object(self.load_menu_label)
        game_manager.fb_scene.add_ui_object(self.load_back_button)
        game_manager.fb_scene.add_ui_object(self.load_cancel_button)
        game_manager.fb_scene.add_ui_object(self.load_menu_load_button)
        game_manager.fb_scene.add_ui_object(self.load_menu_item_label)

    def update_load_item_selected_label(self):
        if self.save_item_selected == None:
            self.load_menu_item_label.text = self.base_load_menu_item_label_texts[0]
            self.load_menu_item_label.model.color = get_colors("light")
        else:
            self.load_menu_item_label.text = self.base_load_menu_item_label_texts[1] + self.save_item_selected.text
            self.load_menu_item_label.model.color = get_colors("tone_3")
        self.load_menu_item_label.recalculate()

    def open_options_menu(self, btn, click):
        self.game_manager.pause_game()
        self.game_manager.fb_scene.set_active(self.options_ui_click_blocker, True)
        self.game_manager.fb_scene.set_active(self.options_label, True)
        self.game_manager.fb_scene.set_active(self.options_back_button, True)

    def close_options_menu(self, btn, click):
        self.game_manager.resume_game()
        self.game_manager.fb_scene.set_active(self.options_ui_click_blocker, False)
        self.game_manager.fb_scene.set_active(self.options_label, False)
        self.game_manager.fb_scene.set_active(self.options_back_button, False)

    def open_load_menu(self, btn, click):
        self.save_item_selected = None
        self.update_load_item_selected_label()
        self.game_manager.pause_game()
        self.load_saves_scroll_view.elements = self.items_from_save_file_name(get_save_files())
        self.load_saves_scroll_view.recalculate()
        self.game_manager.fb_scene.set_active(self.load_ui_click_blocker, True)
        self.game_manager.fb_scene.set_active(self.load_saves_scroll_view, True)
        self.game_manager.fb_scene.set_active(self.load_menu_label, True)
        self.game_manager.fb_scene.set_active(self.load_back_button, True)
        self.game_manager.fb_scene.set_active(self.load_cancel_button, True)
        self.game_manager.fb_scene.set_active(self.load_menu_load_button, True)
        self.game_manager.fb_scene.set_active(self.load_menu_item_label, True)
        
    def close_load_menu(self, btn, click):
        self.game_manager.resume_game()
        self.game_manager.fb_scene.set_active(self.load_ui_click_blocker, False)
        self.game_manager.fb_scene.set_active(self.load_saves_scroll_view, False)
        self.game_manager.fb_scene.set_active(self.load_menu_label, False)
        self.game_manager.fb_scene.set_active(self.load_back_button, False)
        self.game_manager.fb_scene.set_active(self.load_cancel_button, False)
        self.game_manager.fb_scene.set_active(self.load_menu_load_button, False)
        self.game_manager.fb_scene.set_active(self.load_menu_item_label, False)
    
    def items_from_save_file_name(self, save_files):
        items = []
        for save_file in save_files:
            name_without_extension = save_file.split('.')[0]
            items.append(UIItem(save_file, name_without_extension, name_without_extension))
        return items

    def save_item_clicked(self, item):
        """ Called when the user in the load menu selects a save """
        self.save_item_selected = item
        self.update_load_item_selected_label()

    def cancel_loading_clicked(self, btn, click):
        self.save_item_selected = None
        self.update_load_item_selected_label()

    def load_item_clicked(self, btn, click):
        self.close_load_menu(btn, click)
        self.game_manager.load(self.save_item_selected.value)

    def awake(self):
        self.game_manager.fb_ui = self

    def update_bird_count(self):
        self.info_labels[1].text = self.info_labels_base_text[1] + str(len(self.game_manager.birds))

    def start(self):
        self.options_ui_click_blocker.recalculate()
        self.options_label.recalculate()
        self.options_back_button.recalculate()
        self.load_ui_click_blocker.recalculate()
        self.load_saves_scroll_view.recalculate()
        self.load_menu_label.recalculate()
        self.load_back_button.recalculate()
        self.load_cancel_button.recalculate()
        self.load_menu_item_label.recalculate()
        self.load_menu_load_button.recalculate()
        self.game_manager.fb_scene.set_active(self.load_ui_click_blocker, False)
        self.game_manager.fb_scene.set_active(self.load_menu_label, False)
        self.game_manager.fb_scene.set_active(self.load_back_button, False)
        self.game_manager.fb_scene.set_active(self.load_saves_scroll_view, False)
        self.game_manager.fb_scene.set_active(self.options_label, False)
        self.game_manager.fb_scene.set_active(self.options_back_button, False)
        self.game_manager.fb_scene.set_active(self.options_ui_click_blocker, False)
        self.game_manager.fb_scene.set_active(self.load_cancel_button, False)
        self.game_manager.fb_scene.set_active(self.load_menu_load_button, False)
        self.game_manager.fb_scene.set_active(self.load_menu_item_label, False)
        self.info_labels_group_layout.recalculate()

    def slider_test(self, slider, click):
        print(str(slider.value))
        
    def update(self):
        if get_engine().real_delta_time:
            self.info_labels[4].text = self.info_labels_base_text[4] + str(int(1 / get_engine().real_delta_time))

    def render(self):
        if get_engine().render_delta_time:
            self.info_labels[3].text = self.info_labels_base_text[3] + str(int(1 / get_engine().render_delta_time))

        Renderer.render_rect(self.rect_ui)
        Renderer.render_line(self.separation_lines[0], self.separation_lines[1], self.separation_lines_color, 4)
        Renderer.render_line(self.separation_lines[2], self.separation_lines[3], self.separation_lines_color, 4)