from contextlib import contextmanager
from configparser import ConfigParser
import json
import sys
from datetime import (
        datetime,
        )
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QLabel,
        QAction,
        QFrame,
        QMenu,
        QSystemTrayIcon,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QVBoxLayout,
        QHBoxLayout,
        QVBoxLayout,
        QWidget,
        )
from PyQt5.QtCore import (
        Qt,
        QTimer
        )
import os
from src.clocks import Clock
from src.elements import MyTopNav, SettingsController
from src.config import Config

class ClocksApp(QMainWindow):
    dragging = False
    timers_data = []
    timers = []
    app_name = "PyClocks"
    default_config = {
            "always-on-top": True
            }
    timer_i = -1
    start_date = datetime.now().strftime("%y-%m-%d")

    def __init__(
            self,
            clocks_app_folder_path:str,
            timers_data_path:str,
            config_data:dict | None = None,
            use_system_top_nav:bool=True,
            ):
        super().__init__()
        self.config = Config()
        self.custom_top_nav = not self.config.usesystemtopbar
        self.icon_path = os.path.join(os.path.dirname(__file__),"icon.png")
        self.icon_topnav_path = os.path.join(os.path.dirname(__file__),"icon_27.png")
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(self.icon_path))
        self.setWindowIcon(self.icon)
        self.clocks_app_folder_path = clocks_app_folder_path
        self.timers_data_path = timers_data_path
        self.history_file = os.path.join(self.clocks_app_folder_path, "history_" + self.start_date + os.path.basename(self.timers_data_path))
        timers_data = {}
        try:
            timers_data = json.load(open(self.timers_data_path, "r"))
        except FileNotFoundError:
            QMessageBox.critical(self, "Could not find Clocks file", f"Could not find clocks file under '{self.timers_data_path}'!")
        except Exception as e:
            QMessageBox.critical(self, "Could not load Clocks file", f"Could not laod clocks file located under '{self.timers_data_path}' due to {type(e).__name__}: {e}!")
            exit()
        self.setupTimers(timers_data)

        # setup configs
        if config_data is not None:
            self.setupConfigs(config_data)
        # setup app and UI
        self.initUi()
        #if self.config.get("always-on-top"):
        #    self.setWindwowFlags(Qt.WindowStaysOnTopHint | Qt.Window)
        if self.custom_top_nav:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.Tool)
        else:
            self.setWindowFlags(Qt.Tool)
        self.setMinimumSize(130,231)
        if self.config.openwindowonstart:
            self.show()
        self.initSettings()
        self.initTray()

    def setupTimers(self, timers_data:list[dict]):
        if timers_data:
            for timer in timers_data:
                if self._validate_timer_data(timer):
                    self.timers_data.append(timer)
        else:
            self.timers_data = []
        # setup timer to save data
        self.app_timer = QTimer()
        self.app_timer.timeout.connect(lambda: self._run_timer())
        self.app_timer.start(100)

    def _run_timer(self):
        data_for_save = self._get_data_for_save()
        try:
            json.dump(data_for_save,open(self.timers_data_path,"w"), indent=4)
        except Exception as e:
            pass
        try:
            json.dump(data_for_save, open(self.history_file,"w"))
        except Exception as e:
            print(f"Cannot save history due to {e}")

    def initUi(self):
        # set app name and main widget
        self.setWindowTitle(self.app_name)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        # create layout
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        # create topbar
        if self.custom_top_nav:
            self.top_nav_frame = QFrame()
            self.top_nav_frame.setContentsMargins(0,0,0,0)
            self.top_nav_frame.setFixedHeight(30)
            self.top_nav_frame.setStyleSheet("""
            QFrame {
            background: #1e1e1e;
            border: none;
            }
            QPushButton {
            background: #1e1e1e;
            }
            """
            )
            self.top_nav = MyTopNav(self, self.top_nav_frame, self.icon_topnav_path, True, True)
            self.main_layout.addWidget(self.top_nav_frame)
        # create timers
        self.timers_frame = QFrame(self)
        self.timers_layout = QHBoxLayout(self.timers_frame)
        for timer in self.timers_data:
            self.createClock(timer)
        self.main_layout.addWidget(self.timers_frame)

    def initSettings(self):
        self.settings_window = SettingsController(self)

    def initTray(self):
        self.tray = QSystemTrayIcon()
        self.tray_menu = QMenu()
        #show_action = QAction("Show", self)
        #show_action.triggered.connect(self.show_window)
        for t in self.timers:
            clock_action = QAction(str(t), self)
            clock_action.triggered.connect(t._control_time)
            self.tray_menu.addAction(clock_action)
            t.tray_object = clock_action
        self.tray_menu.addSeparator()
        self.tray_menu.addAction("Show app", self.show_window)
        self.tray_menu.addAction("Settings", self.show_settings)
        self.tray_menu.addAction("Exit", sys.exit)
        self.tray.setContextMenu(self.tray_menu)
        self.tray.setIcon(self.icon)
        self.tray.show()

    def _control_edit_mode(self):
        print("Edit mode Not implemented")

    def createClock(self, timer_data:dict):
        self.timer_i += 1
        clock = Clock(
                self.timers_layout, 
                self.timer_i + 0,
                timer_data["Name"],
                timer_data["Time"],
                isActive=False,
                color=timer_data["Color"]
                )
        # setup frame and layout
        self.timers.append(clock)

    def setupConfigs(self, config_data:dict):
        for k,v in self.default_config.items():
            self.config[k] = config_data.get(k, v) 

    def _validate_timer_data(self, timer_data:dict) -> bool:
        validation_passed = True
        schema = {
                "Name": str,
                "Color": str,
                "Time": int
                }
        for k,v in schema.items():
            if timer_data.get(k) is None:
                QMessageBox.warning(self, "Error", f"Timer data din't contain {k}!")
                validation_passed = False
            if not isinstance(timer_data[k], schema[k]):
                QMessageBox.warning(self, "Error", f"{k} should be {v.__name__}, but is {type(timer_data[k]).__name__}")
                validation_passed = False
        return validation_passed

    def show_settings(self):
        self.initSettings()
        self.settings_window.show()

    def show_window(self):
        #if self.isMinimized():
        #    self.showNormal()
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _minimize(self):
        #self.showNormal()
        self.showMinimized()
        #self.hide()

    def _close(self):
        sys.exit()

    def _get_data_for_save(self):
        data = []
        for clock in self.timers:
            timer = {"Name": clock.name, 'Color': clock.color, "Time": clock.count}
            data.append(timer)
        return data

    # timer methods
    # Events
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()


