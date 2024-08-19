import json
from datetime import (
        datetime,
        timezone
        )
from PyQt5.QtWidgets import (
        QFrame,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QVBoxLayout,
        QLabel,
        QHBoxLayout,
        QVBoxLayout,
        QWidget,
        )
from PyQt5.QtCore import (
        Qt,
        QTime,
        QTimer
        )
import os

class ClocksApp(QMainWindow):
    dragging = False
    timers_data = []
    timers = []
    app_name = "PyClocks"
    default_config = {
            "always-on-top": True
            }
    config = {}
    timer_i = -1
    custom_top_nav = False
    start_date = datetime.now().strftime("%y-%m-%d")

    def __init__(
            self,
            clocks_app_folder_path:str,
            timers_data_path:str,
            config_data:dict | None = None
            ):
        super().__init__()
        self.clocks_app_folder_path = clocks_app_folder_path
        self.timers_data_path = timers_data_path
        print(clocks_app_folder_path)
        self.history_file = os.path.join(self.clocks_app_folder_path, "history_" + self.start_date + os.path.basename(self.timers_data_path))
        print(self.history_file)
        try:
            timers_data = json.load(open(self.timers_data_path, "r"))
        except FileNotFoundError:
            QMessageBox.critical(self, "Could not find Clocks file", f"Could not find clocks file under '{self.timers_data_path}'!")
            exit()
        except Exception as e:
            QMessageBox.critical(self, "Could not load Clocks file", f"Could not laod clocks file located under '{self.timers_data_path}' due to {type(e).__name__}: {e}!")
            exit()
        self.setupTimers(timers_data)

        # setup configs
        if config_data is not None:
            self.setupConfigs(config_data)
        # setup app and UI
        self.initUi()
        if self.config.get("always-on-top"):
            self.setWindwowFlags(Qt.WindowStaysOnTopHint)
        if self.custom_top_nav:
            self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()
        self._update_timer_color()

    def setupTimers(self, timers_data:list[dict]):
        if timers_data:
            for timer in timers_data:
                if self._validate_timer_data(timer):
                    self.timers_data.append(timer)
        else:
            self.timers_data = []

    def initUi(self):
        # set app name and main widget
        self.setWindowTitle(self.app_name)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        # create layout
        self.layout = QVBoxLayout(self.main_widget)
        # create topbar
        if self.custom_top_nav:
            self.top_nav = QHBoxLayout()
            self.close_btn = QPushButton("x", self)
            self.close_btn.setFixedWidth(30)
            self.close_btn.clicked.connect(self._close)
            self.top_nav.addWidget(self.close_btn, alignment=Qt.AlignRight)
            self.layout.addLayout(self.top_nav)

        # create timers
        self.timers_frame = QFrame(self)
        self.timers_layout = QHBoxLayout(self.timers_frame)
        for timer in self.timers_data:
            self.createClock(timer)
        self.layout.addWidget(self.timers_frame)

    def createClock(self, timer_data:dict):
        self.timer_i += 1
        this_i = self.timer_i + 0
        # setup frame and layout
        clock_frame = QFrame(self.timers_frame)
        clock_frame.setStyleSheet(".QFrame {"
                f"border-color: {timer_data['Color']};"
                "border-width: 2;"
                "border-style: solid;"
                "border-radius: 4;"
                "}"
                ".QLabel{"
                                  "font-size: 15pt"
                "}"
                )
        
        clock_layout = QVBoxLayout(clock_frame)
        # setup label
        clock_name = QLabel(timer_data.get("Name"), clock_frame)
        # pack label
        clock_layout.addWidget(clock_name, alignment=Qt.AlignCenter)
        # setup timer
        timer = QTimer(clock_frame)
        timer.timeout.connect(lambda: self._show_time(this_i))
        timer.start(100)
        timer_display = QLabel("---",clock_frame)
        timer_display.setObjectName(f"clockTimer{this_i}")
        # pack timer
        clock_layout.addWidget(timer_display, alignment=Qt.AlignCenter)
        # setup buttons
        start_btn = QPushButton("Start", clock_frame)
        start_btn.clicked.connect(lambda: self._start_time(this_i))
        stop_btn = QPushButton("Stop", clock_frame)
        stop_btn.clicked.connect(lambda: self._stop_time(this_i))
        reset_btn = QPushButton("Reset", clock_frame)
        reset_btn.clicked.connect(lambda: self._reset_time(this_i))
        # pack buttson
        clock_layout.addWidget(start_btn)
        clock_layout.addWidget(stop_btn)
        clock_layout.addWidget(reset_btn)
        # append clock
        self.timers_layout.addWidget(clock_frame)
        clock_object = {
                "name": timer_data["Name"],
                "isActive": False,
                "count": timer_data["Time"],
                "color": timer_data["Color"],
                "object": clock_frame,
                "display": timer_display,
                }
        self.timers.append(clock_object)

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

    def _close(self):
        exit()

    def _get_data_for_save(self):
        data = []
        for clock in self.timers:
            timer = {"Name": clock['name'], 'Color': clock['color'], "Time": clock['count']}
            data.append(timer)
        return data
    # timer methods
    def _show_time(self, clock_object_i:int):
        clock_object = self.timers[clock_object_i]
        if clock_object["isActive"]:
            clock_object["count"] += 1
            # save data
            data_for_save = self._get_data_for_save()
            try:
                json.dump(data_for_save,open(self.timers_data_path,"w"), indent=4)
            except Exception as e:
                pass
            try:
                json.dump(data_for_save, open(self.history_file,"w"))
            except Exception as e:
                print(f"Cannot save history due to {e}")
        time_as_int = int(clock_object["count"] / 10)
        time_as_text = datetime.fromtimestamp(time_as_int, timezone.utc).strftime("%H:%M:%S")

        clock_object["display"].setText(time_as_text)

    def _start_time(self, clock_object_i:int):
        self.timers[clock_object_i]["isActive"] = True
        self._update_timer_color()

    def _stop_time(self, clock_object_i:int):
        self.timers[clock_object_i]["isActive"] = False
        self._update_timer_color()

    def _reset_time(self, clock_object_i:int):
        self.timers[clock_object_i]["count"] = 0
        
    def _update_timer_color(self):
        enabled = "#FFFFFF"
        disabled = "#989898"
        stylesheet = ""
        for i, timer in enumerate(self.timers):
            if timer["isActive"]:
                stylesheet += f"#clockTimer{i}" + "{color: %s}"%enabled
            else:
                stylesheet += f"#clockTimer{i}" + "{color: %s}"%disabled
        self.setStyleSheet(stylesheet)

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


