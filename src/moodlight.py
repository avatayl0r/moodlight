import sys
import os
import subprocess as subproc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QDialog, QGroupBox, QWidget, QGridLayout, QMenuBar,
    QFileDialog)

import com_ui
import moodlight_config as config


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.app_name = com_ui.UIProperties.get_app_name()
        self.version = com_ui.UIProperties.get_version()
        self.developer = com_ui.UIProperties.get_developer_name()
        self.setWindowTitle(f"{self.app_name} || Version {self.version}")
        self.setWindowIcon(com_ui.UIProperties.get_app_icon())
        self.setFixedSize(
            com_ui.UIProperties.get_app_width(),
            com_ui.UIProperties.get_app_height())

        with open(config.APP_STYLE, "r", encoding="UTF-8") as stylesheet:
            self.setStyleSheet(stylesheet.read())
        self.moodlight_ui = MoodlightUI()
        self.setMenuBar(self.menu_bar())
        self.setCentralWidget(self.moodlight_ui)

    def menu_bar(self) -> QMenuBar:
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu("File")

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app)

        help_menu = menubar.addMenu("Help")

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.about_info)

        return menubar

    def about_info(self):
        msg_box = com_ui.CommonUI.message_box(
            self,
            title = "About Moodlight",
            text = "Moodlight is an app for mood tracking and mental health.",
            info_text = f"""Version: v{self.version}
            \nDeveloped by: {self.developer}""")
        msg_box.exec_()

    def exit_app(self):
        self.close()

class MoodlightUI(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.moodlight_instance = Moodlight(self)
        main_layout = self.setup_ui()
        self.setLayout(main_layout)

    def setup_ui(self):
        main_layout = QVBoxLayout()

        graph_group = QGroupBox("Moodlight Graph")
        graph_layout = QGridLayout()

        graph = self.moodlight_instance.draw_graph(
            date = datetime.datetime.now().strftime("%Y-%m-%d"),
            mood_ratings = {
                "am": [5, 6, 7, 8, 9, 10, 8],
                "pm": [10, 9, 2, 4, 6, 4, 3]
            }
        )

        graph_layout.addWidget(graph)
        graph_group.setLayout(graph_layout)

        main_layout.addWidget(graph_group)
        return main_layout

class Moodlight:
    def __init__(self, moodlight_ui) -> None:
        self.moodlight_ui = moodlight_ui

    def draw_graph(self, date, mood_ratings) -> FigureCanvas:
        fig = plt.figure()
        plt.style.use("seaborn-v0_8-poster")
        figCanvas = FigureCanvas(fig)

        weekdays = np.array([
                "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        df_am = pd.DataFrame({
            "date_of_week": weekdays,
            "mood_ratings": mood_ratings["am"]})

        df_pm = pd.DataFrame({
            "date_of_week": weekdays,
            "mood_ratings": mood_ratings["pm"]})

        plt.plot(df_am["date_of_week"], df_am["mood_ratings"])
        plt.plot(df_pm["date_of_week"], df_pm["mood_ratings"])

        plt.title(date)
        plt.xticks(rotation=30, ha="right")
        plt.xlabel("Week")
        plt.ylabel("Mood Rating")

        return figCanvas


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
