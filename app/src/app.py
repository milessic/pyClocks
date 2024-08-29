from contextlib import contextmanager
from configparser import ConfigParser
import json
import sys
from datetime import (
        datetime,
        )
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QSizeGrip,
        QLabel,
        QAction,
        QSizePolicy,
        QFrame,
        QMenu,
        QScrollArea,
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
from src.random_hex_generator import generate_random_hex

VERSION = "v1.1"
class ClocksApp(QMainWindow):
    dragging = False
    timers_data = []
    timers = []
    app_name = "PyClocks"
    version = VERSION
    short_description = app_name + " " + version + " - " + "milessic, 2024"
    default_config = {
            "always-on-top": True
            }
    timer_i = -1
    start_date = datetime.now().strftime("%y-%m-%d")
    edit_mode = False
    top_nav_height = 0

    def __init__(
            self,
            clocks_app_folder_path:str,
            timers_data_path:str,
            config_data:dict | None = None,
            use_system_top_nav:bool=True,
            nerd_font:str|None=None
            ):
        super().__init__()
        self.nerd_font = nerd_font
        self.edit_icon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), "edit_icon.svg"))
        #self.settings_icon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), "settings_icon.png"))
        self.settings_icon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), "settings_icon.svg"))
        self.clocks_app_folder_path = clocks_app_folder_path
        self.config = Config(self.clocks_app_folder_path)
        self.custom_top_nav = not self.config.usesystemtopbar
        self.icon_path = os.path.join(os.path.dirname(__file__),"icon.png")
        self.icon_topnav_path = os.path.join(os.path.dirname(__file__),"icon_27.png")
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(self.icon_path))
        self.setWindowIcon(self.icon)
        self.timers_data_path = timers_data_path
        self.history_file = os.path.join(self.clocks_app_folder_path, "history_" + self.start_date + os.path.basename(self.timers_data_path))
        timers_data = {}
        try:
            timers_data = json.load(open(self.timers_data_path, "r"))
        except FileNotFoundError:
            #QMessageBox.critical(self, "Could not find Clocks file", f"Could not find clocks file under '{self.timers_data_path}'!")
            pass
        except Exception as e:
            QMessageBox.critical(self, "Could not load Clocks file", f"Could not laod clocks file located under '{self.timers_data_path}' due to {type(e).__name__}: {e}!")
            exit()
        self.setupTimers(timers_data)

        # setup configs
        if config_data is not None:
            self.setupConfigs(config_data)
        # setup app and UI
        self.initUi()
        self.gripSize = 16
        self.grips = []
        for i in range(4):
            grip = QSizeGrip(self)
            grip.setStyleSheet("background: transparent")
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)
        #if self.config.get("always-on-top"):
        #    self.setWindwowFlags(Qt.WindowStaysOnTopHint | Qt.Window)
        if self.custom_top_nav:
            if self.config.runastool:
                self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.Tool)
            else:
                self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window )
        else:
            if self.config.runastool:
                self.setWindowFlags( Qt.Window | Qt.Tool)
            else:
                self.setWindowFlags( Qt.Window )
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
            self.topnav_height = self.top_nav_frame.height()
            self.main_layout.addWidget(self.top_nav_frame)
        # create timers
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_widget.setLayout(self.container_layout)

        #self.scroll_content = QWidget(self.scroll_area)
        self.timers_frame = QFrame()
        self.timers_frame.setStyleSheet("margin: 10px;")
        #self.timers_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.timers_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.scroll_area.setWidget(self.container_widget)

        #self.timers_frame = QWidget(self.scroll_area)
        self.timers_layout = QHBoxLayout()
        self.container_layout.addLayout(self.timers_layout)
        #self.timers_layout.setContentsMargins(10, 10, 10, 10)  # Adjust as needed
        #self.timers_layout.setSpacing(10)  # Adjust the spacing between widgets

        #self.scroll_area.setLayout(self.timers_layout)
        self.initNoClocksUi()
        if not len(self.timers_data):
            self.no_clocks_frame.show()
        for timer in self.timers_data:
            self.createClock(timer)
        #self.main_layout.addWidget(self.timers_frame)
        self.main_layout.addWidget(self.scroll_area)
        self.add_new_timer_btn = QPushButton("", self.main_widget)
        if self.nerd_font is not None:
            self.add_new_timer_btn.setFont(QtGui.QFont(self.nerd_font))
        self.add_new_timer_btn.hide()
        self.add_new_timer_btn.clicked.connect(lambda: self.createClock({"Name":"","Color":generate_random_hex(), "Time":0,"Active":False}, True, True))
        #self.add_new_timer_btn.setFlat(True)
        #self.add_new_timer_btn.setStyleSheet("border: 3px solid #e3e3e3;color: #e3e3e3;font-size: 30pt;")
        self.add_new_timer_btn.setStyleSheet("font-size: 30pt;")


    def initNoClocksUi(self):
        self.no_clocks_frame = QFrame()
        self.no_clocks_layout = QHBoxLayout(self.no_clocks_frame)
        self.no_clocks_label = QLabel("There are no clocks\nEnter edit mode \nand click   to create one", self.no_clocks_frame)
        self.no_clocks_frame.setStyleSheet("""
            .QFrame{
                border: 3px solid #FFFFFF;
            }
            .QLabel{
                font-size: 12pt;
            }
        """)
        self.no_clocks_layout.addWidget(self.no_clocks_label)
        self.timers_layout.addWidget(self.no_clocks_frame)
        self.no_clocks_frame.hide()

    def initSettings(self):
        self.settings_window = SettingsController(self)

    def initTray(self):
        self.tray = QSystemTrayIcon()
        self.tray_menu = QMenu()
        #show_action = QAction("Show", self)
        #show_action.triggered.connect(self.show_window)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction("Show app", self.show_window)
        self.tray_menu.addAction("Edit Mode", self._control_edit_mode)
        self.tray_menu.addAction("Settings", self.show_settings)
        self.tray_menu.addAction("Exit", sys.exit)
        for t in self.timers:
            self._append_clock_to_tray(t)
        self.tray.setContextMenu(self.tray_menu)
        self.tray.setIcon(self.icon)
        self.tray.show()

    def _append_clock_to_tray(self,t):
        clock_action = QAction(str(t), self)
        clock_action.triggered.connect(t._control_time)
        clock_action.setObjectName(t.name)
        self.tray_menu.addAction(clock_action)
        t.tray_object = self.tray_menu 
        t.tray_action = clock_action

    def _control_edit_mode(self):
        # set + button geometry
        appw, apph = (self.width()-70, self.height())
        try:
            self.add_new_timer_btn.setGeometry(appw, self.topnav_height + 10, 60,apph-45)
        except AttributeError:
            self.add_new_timer_btn.setGeometry(appw, 10, 60,apph-20)
        # set edit mode
        if self.edit_mode:
            self.edit_mode = False
            self.add_new_timer_btn.hide()
        else:
            self.edit_mode = True
            self.add_new_timer_btn.show()
        # update timers
        for timer in self.timers:
            if self.edit_mode:
                timer._enable_edit_mode()
            else:
                timer._disable_edit_mode()
                self._check_timers_for_deletion()


    def _check_timers_for_deletion(self):
        for i,timer in enumerate(self.timers):
            if timer.to_be_destroyed:
                timer.clock_frame.hide()
                timer.clock_frame.destroy()
                self.timers.pop(i)
                action = self.findChild(QAction, timer.name)
                self.tray_menu.removeAction(action)
        if not len(self.timers):
            self.no_clocks_frame.show()

                
    def createClock(self, timer_data:dict, enable_edition:bool=False, update_tray:bool=False):
        self.no_clocks_frame.hide()
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
        if enable_edition:
            clock._enable_edit_mode()
        if update_tray:
            self._append_clock_to_tray(clock)

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
    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        # top right
        self.grips[1].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[3].move(0, rect.bottom() - self.gripSize)

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


