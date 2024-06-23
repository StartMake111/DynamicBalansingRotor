import dearpygui.dearpygui as dpg
import numpy as np
from com_port1 import ArduinoUNO, PORT, samplingRate, TachometerSimulationPlot
from pyfirmata2 import Arduino
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import threading
import time
import func
import dearpygui_ext.themes as dpg_ext

dpg.create_context()
light_theme = dpg_ext.create_theme_imgui_light()
with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(
            dpg.mvThemeCol_FrameBg, (255, 255, 255), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_style(
            dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
        )

    with dpg.theme_component(dpg.mvInputInt):
        dpg.add_theme_color(
            dpg.mvThemeCol_FrameBg, (140, 255, 23), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_style(
            dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
        )


def callBack1(data):
    PanningPlot1.addData(data)
    PanningPlot1.update()


def callBack2(data):
    PanningPlot2.addData(data)
    PanningPlot2.update()


def connect():
    print("Connecting")
    start_tachometer_simulation()
    dpg.configure_item("Button", label="Connecting..")
    board = Arduino(PORT, baudrate=115200, debug=True)
    dpg.configure_item("COM", default_value=f"{board}")
    board.samplingOn(1000 // samplingRate)
    board.analog[0].register_callback(callBack1)
    board.analog[1].register_callback(callBack2)
    board.analog[0].enable_reporting()
    board.analog[1].enable_reporting()
    dpg.configure_item("Button", label="Connected", enabled=False)
    print("Connected")


def start_tachometer_simulation():
    global tachometer_thread
    PanningPlot3.stop_simulation()  # остановить текущую симуляцию, если она идет
    tachometer_thread = threading.Thread(
        target=PanningPlot3.start_simulation, args=(0.1,)
    )
    tachometer_thread.start()


with dpg.theme() as window_theme1:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(
            dpg.mvThemeCol_WindowBg, (247, 247, 247, 255), category=dpg.mvThemeCat_Core
        )

with dpg.window(
    label="Main window",
    pos=(150,),
    autosize=True,
    tag="mainplots",
) as win:
    PanningPlot1 = ArduinoUNO("First", "main_window")
    PanningPlot2 = ArduinoUNO("Second", "main_window")
    PanningPlot3 = TachometerSimulationPlot("Tachometer", "main_window", rpm=60)

# dpg.bind_theme("Firtst", global_theme)

l = serial.tools.list_ports.comports()
comports = []
for d in l:
    if d.device:
        if ("USB" in d.description) or (not d.description):
            devname = str(d.device)
            comports.append(devname)
comports.sort()
try:
    port = comports[0]
except Exception as e:
    port = []
    pass

save = []


def takesnap():
    x, y = func.draw_vector_with_phase(
        func.find_phase(PanningPlot1.data, PanningPlot3.data)
    )
    dpg.draw_arrow(
        parent="left",
        p2=[200.0, 200.0],
        p1=[200 + x * 20, 200 + y * 20],
        tag="first1",
        color=(0, 0, 255),
    )
    a = np.array([200.0, 200.0]), np.array([200 + x * 20, 200 + y * 20])
    x, y = func.draw_vector_with_phase(
        func.find_phase(PanningPlot2.data, PanningPlot3.data)
    )
    dpg.draw_arrow(
        parent="right",
        p2=[200.0, 200.0],
        p1=[200 + x * 20, 200 + y * 20],
        tag="second1",
        color=(0, 0, 255),
    )
    save = [
        a,
        [np.array([200.0, 200.0]), np.array([200 + x * 20, 200 + y * 20])],
    ]


def takesnap1():
    x, y = func.draw_vector_with_phase(
        func.find_phase(PanningPlot1.data, PanningPlot3.data)
    )
    dpg.draw_arrow(
        parent="left",
        p1=[200.0, 200.0],
        p2=[200 + x * 20, 200 + y * 20],
        tag="first2",
        color=(255, 0, 0),
    )
    a = np.array([200.0, 200.0], [200 + x * 20, 200 + y * 20])
    x, y = func.draw_vector_with_phase(
        func.find_phase(PanningPlot2.data, PanningPlot3.data)
    )
    dpg.draw_arrow(
        parent="right",
        p1=[200.0, 200.0],
        p2=[200 + x * 20, 200 + y * 20],
        tag="first2",
        color=(255, 0, 0),
    )
    b = np.array([200.0, 200.0], [200 + x * 20, 200 + y * 20])
    c = a - save[0]
    # dpg.draw_arrow(parent="left", c[0],c[1])


def takesnap2():
    x, y = func.draw_vector_with_phase(
        func.find_phase(PanningPlot1.data, PanningPlot3.data)
    )
    dpg.draw_arrow(
        parent="left",
        p1=[200.0, 200.0],
        p2=[200 + x * 20, 200 + y * 20],
        tag="first3",
        color=(0, 255, 0),
    )
    x, y = func.draw_vector_with_phase(
        func.find_phase(PanningPlot2.data, PanningPlot3.data)
    )
    dpg.draw_arrow(
        parent="right",
        p1=[200.0, 200.0],
        p2=[200 + x * 20, 200 + y * 20],
        tag="first3",
        color=(0, 255, 0),
    )


def show_info(title, message, selection_callback):
    # guarantee these commands happen in the same frame
    # with dpg.mutex():
    #     viewport_width = dpg.get_viewport_client_width()
    #     viewport_height = dpg.get_viewport_client_height()

    #     with dpg.window(label=title, modal=True, no_close=True) as modal_id:
    #         with dpg.plot(label="Snap", height=300, width=800):
    #             dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="xaxis")
    #             dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="yaxis")
    #             data_x, data_y = PanningPlot1.snap, list(
    #                 np.linspace(0, 500 / samplingRate, 500)
    #             )
    #             dpg.add_line_series(data_y, data_x, parent="yaxis")
    #             dpg.set_axis_limits("xaxis", 0, 2)
    #             dpg.set_axis_limits("yaxis", 0, 1)

    # guarantee these commands happen in another frame
    x, y = func.draw_vector_with_phase(
        func.find_phase(PanningPlot1.data, PanningPlot3.data)
    )
    dpg.draw_arrow(parent="left", p2=[200.0, 200.0], p1=[x * 20, y * 20])

    # dpg.split_frame()
    # width = dpg.get_item_width(modal_id)
    # height = dpg.get_item_height(modal_id)
    # dpg.set_item_pos(
    #     modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2]
    # )


def update_rpm(sender, app_data):
    new_rpm = app_data
    PanningPlot3.rpm = new_rpm
    start_tachometer_simulation()


with dpg.window(label="Com port", tag="comport"):
    dpg.add_text(f"{port}", tag="COM")
    dpg.add_button(label="Connect", callback=connect, tag="Button")
    dpg.add_input_int(label="RPM", default_value=60, callback=update_rpm)
with dpg.window(label="Zero start", tag="Zero"):
    dpg.add_button(label="analyse", callback=takesnap)
with dpg.window(label="1'st added mass", tag="1'st added"):
    dpg.add_input_double(label="Mass")
    dpg.add_button(label="analyse 1", callback=takesnap1)
with dpg.window(label="2'st added mass", tag="2'st added"):
    dpg.add_input_double(label="Mass")
    dpg.add_button(label="analyse 2", callback=takesnap2)


# Функция для преобразования из полярных координат в декартовы
def polar_to_cartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


# Данные для графика
r1, theta1 = 2.5, np.radians(45)  # Красная стрелка
r2, theta2 = 8, np.radians(225)  # Синяя стрелка
with dpg.window(label="Polar Plot Example", no_resize=False, tag="polarplot"):
    # Добавление канвы для рисования
    with dpg.drawlist(width=400, height=400, tag="left"):
        # Рисуем окружности
        for r in range(1, 11, 1):
            dpg.draw_circle((200, 200), r * 20, color=(200, 200, 200, 255), thickness=1)

        # Рисуем радиальные линии
        for angle in range(0, 360, 30):
            x, y = polar_to_cartesian(200, np.radians(angle))
            dpg.draw_line(
                (200, 200), (200 + x, 200 - y), color=(200, 200, 200, 255), thickness=1
            )

        # Метки углов
        for angle in [0, 90, 180, 270]:
            x, y = polar_to_cartesian(190, np.radians(angle))
            dpg.draw_text((190 + x, 190 - y), f"{angle}°", color=(255, 255, 255, 255))
    with dpg.drawlist(width=400, height=400, tag="right"):
        # Рисуем окружности
        for r in range(1, 11, 1):
            dpg.draw_circle((200, 200), r * 20, color=(200, 200, 200, 255), thickness=1)

        # Рисуем радиальные линии
        for angle in range(0, 360, 30):
            x, y = polar_to_cartesian(200, np.radians(angle))
            dpg.draw_line(
                (200, 200), (200 + x, 200 - y), color=(200, 200, 200, 255), thickness=1
            )

        # Метки углов
        for angle in [0, 90, 180, 270]:
            x, y = polar_to_cartesian(190, np.radians(angle))
            dpg.draw_text((190 + x, 190 - y), f"{angle}°", color=(255, 255, 255, 255))


# tachometer_thread = threading.Thread(target=PanningPlot3.start_simulation, args=(0.1,))
# tachometer_thread.start()
