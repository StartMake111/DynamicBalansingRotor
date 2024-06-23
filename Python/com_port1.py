from pyfirmata2 import Arduino
import dearpygui.dearpygui as dpg
import numpy as np
import time

PORT = Arduino.AUTODETECT
samplingRate = 100


class ArduinoUNO:
    def __init__(self, name, parent):
        self.data = []
        self.name = name
        self.parent = parent
        self.snap = []
        with dpg.plot(label=name, height=300, width=800):
            dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="xaxis" + name)
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="yaxis" + name)
            data_x, data_y = list(np.linspace(-1, 1, 5000)), list(
                np.linspace(0, 1000 / samplingRate, 5000)
            )
            dpg.add_line_series(data_x, data_y, tag=name, parent="yaxis" + name)
            # dpg.set_axis_limits_auto = True
            dpg.set_axis_limits("xaxis" + self.name, 0, 5)
            dpg.set_axis_limits("yaxis" + self.name, 0, 2)

    def update(self):
        self.data = self.data[-500:]
        dpg.configure_item(
            self.name,
            x=np.linspace(0, len(self.data) / samplingRate, len(self.data)),
            y=self.data,
        )

    def addData(self, d):
        self.data.append(d * 3.3)

    def takeSnapshot(self) -> list:
        self.snap = self.data
        self.max_ = max(enumerate(self.snap), key=lambda x: x[1])[0]
        print(self.max_)
        return self.data


class TachometerSimulationPlot:
    def __init__(self, name, parent, rpm):
        self.data = []
        self.name = name
        self.parent = parent
        self.snap = []
        self.rpm = rpm  # частота вращения в оборотах в минуту
        self.angle = 0  # начальный угол
        self.running = False  # флаг для управления потоком

        with dpg.plot(label=name, height=300, width=800):
            dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="xaxis" + name)
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="yaxis" + name)
            data_x, data_y = list(np.linspace(0, 5, 5000)), list(np.zeros(5000))
            dpg.add_line_series(data_x, data_y, tag=name, parent="yaxis" + name)
            # dpg.set_axis_limits("xaxis" + self.name, 0, 5)
            # dpg.set_axis_limits("yaxis" + self.name, -1, 1)

    def update(self):
        self.data = self.data[-500:]
        dpg.configure_item(
            self.name,
            x=np.linspace(
                0, len(self.data) / 100, len(self.data)
            ),  # предположим, что samplingRate = 1000
            y=self.data,
        )

    def addData(self, d):
        self.data.append(d * 3.3)
        self.update()

    def simulate(self, dt):
        # Обновляем угол на основе времени и скорости вращения (rpm)
        self.angle += (self.rpm / 60) * 360 * dt
        self.angle %= 360  # поддерживаем угол в пределах 0-360 градусов

        # Определяем значение тахометра
        if 0 <= self.angle < 180:
            value = 0.5
        else:
            value = -0.5

        self.addData(value)

    def start_simulation(self, dt):
        self.running = True
        while self.running:
            self.simulate(dt)
            time.sleep(dt)

    def stop_simulation(self):
        self.running = False
