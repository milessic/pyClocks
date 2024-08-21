from contextlib import contextmanager
from datetime import (
        datetime,
        timezone
        )
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QFrame,
        QPushButton,
        QVBoxLayout,
        QLabel,
        QVBoxLayout,
        )
from PyQt5.QtCore import (
        Qt,
        QTimer
        )

class Clock:
    def __init__(self, parent, timer_id:int, name:str, count:int, isActive:bool, color:str, tray_object=None):
        self.parent = parent
        self.timer_id = timer_id
        self.name = name
        self.count = count
        self.isActive = isActive
        self.color = color
        self.tray_object = tray_object
        self.initUi()

    def __str__(self):
        return f"{'[a]' if self.isActive else '   '}{self.name} {self._return_time()}"

    def initUi(self):
        self.clock_frame = QFrame()
        self.clock_frame.setStyleSheet(".QFrame {"
                f"border-color: {self.color};"
                "border-width: 2;"
                "border-style: solid;"
                "border-radius: 4;"
                "}"
                ".QLabel{"
                "font-size: 15pt"
                "}"
                )
        self.clock_layout = QVBoxLayout(self.clock_frame)
        # setup label
        self.clock_name = QLabel(self.name, self.clock_frame)
        # pack label
        self.clock_layout.addWidget(self.clock_name, alignment=Qt.AlignCenter)
        # setup timer
        self.timer = QTimer(self.clock_frame)
        self.timer.timeout.connect(lambda: self._show_time())
        self.timer.start(100)
        self.timer_display = QLabel("---",self.clock_frame)
        self.timer_display.setObjectName(f"clockTimer{self.timer_id}")
        # pack timer
        self.clock_layout.addWidget(self.timer_display, alignment=Qt.AlignCenter)
        # setup buttons
        self.start_btn = QPushButton("Start", self.clock_frame)
        self.start_btn.clicked.connect(lambda: self._start_time())
        self.stop_btn = QPushButton("Stop", self.clock_frame)
        self.stop_btn.clicked.connect(lambda: self._stop_time())
        self.reset_btn = QPushButton("Reset", self.clock_frame)
        self.reset_btn.clicked.connect(lambda: self._reset_time())
        # pack buttson
        self.clock_layout.addWidget(self.start_btn)
        self.clock_layout.addWidget(self.stop_btn)
        self.clock_layout.addWidget(self.reset_btn)
        # append clock
        self.parent.addWidget(self.clock_frame)
        self._update_timer_color()

    def _show_time(self):
        if self.isActive:
            self.count += 1
            # save data
        self.timer_display.setText(self._return_time())
        self._update_tray_object()

    def _return_time(self):
        time_as_int = int(self.count / 10)
        return datetime.fromtimestamp(time_as_int, timezone.utc).strftime("%H:%M:%S")

    def _control_time(self):
        if self.isActive:
            self._stop_time()
        else:
            self._start_time()
        if self.tray_object is None:
            return

    def _update_tray_object(self):
        if self.tray_object is None:
            print("Tray object is None!")
            return
        self.tray_object.setText(str(self))

    def _start_time(self):
        self.isActive = True
        self._update_timer_color()

    def _stop_time(self):
        self.isActive = False
        self._update_timer_color()

    def _reset_time(self):
        self.count = 0
        
    def _update_timer_color(self):
        enabled = "#FFFFFF"
        disabled = "#989898"
        stylesheet = ""
        tray_font = QtGui.QFont()
        if self.isActive:
            stylesheet += "color: %s"%enabled
            tray_font.setBold(True)
        else:
            stylesheet += "color: %s"%disabled
            tray_stylesheet = "font-weight: normal"
        self.timer_display.setStyleSheet(stylesheet)
        if self.tray_object is None:
            return
        self.tray_object.setFont(tray_font) # FIXME this doesnt work well

