import dearpygui.dearpygui as dpg
from window1 import *
from math import *


# with dpg.window(label="Select com port", width=150) as base_state:
#     dpg.add_input_float()


# with (dpg.window(label="Base window", pos=(0, 0))):
#     create_statement = dpg.add_button(
#         label="Add exp", callback=create_state)
# тестовая кнопка по добавлению новых окон.
dpg.bind_theme(light_theme)
dpg.create_viewport(title="Custom Title", clear_color=(255, 255, 255))
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
