from contextlib import contextmanager
from src.styling import Styles
from datetime import (
        datetime,
        timezone
        )
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QLineEdit,
        QFrame,
        QPushButton,
        QVBoxLayout,
        QLabel,
        QSizePolicy,
        QVBoxLayout,
        QColorDialog,
        )
from PyQt5.QtCore import (
        Qt,
        QTimer
        )

class Clock:
    clock_is_editable = False
    tray_action = None
    to_be_destroyed = False
    edit_mode = False
    timer_stylesheet_base = (""
            "font-size: 14pt;"
                           )
    def __init__(self, parent, timer_id:int, name:str, count:int, isActive:bool, color:str, timer_width:int,tray_action=None, tray_object=None, app=None):
        self.app = app
        self.timer_stylesheet_edit_disabled = self.timer_stylesheet_base + (""
                                 "background:transparent;"                
                                 f"border: none;"
                                 #"border:2px solid #708ebf;"
        )
        self.timer_stylesheet_edit_enabled =self.timer_stylesheet_base + (""
                                 "background:transparent;"                
                                 "border:2px solid #708ebf;"
                                  "border-radius: 5px;"

        )
        self.timer_width = timer_width
        self.parent = parent
        self.timer_id = timer_id
        self.name = name
        self.count = count
        self.isActive = isActive
        self.color = color
        self.tray_action = tray_action
        self.tray_object = tray_object
        self.initUi()

    def __str__(self):
        return f"{'[a]' if self.isActive else '   '}{self.name} {self._return_time()}"

    def initUi(self):
        self.clock_frame = QFrame()
        self.clock_frame.setObjectName("clockFrame")
        self.clock_frame.setFixedWidth(self.timer_width)
        self.clock_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        #self.clock_frame.setMinimumWidth(150)
        self._update_frame_stylesheet()
        self.clock_layout = QVBoxLayout(self.clock_frame)
        # setup label
        self.clock_name = QLineEdit(self.name, self.clock_frame)
        #self.clock_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clock_name.setAlignment(Qt.AlignCenter)
        self.clock_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.clock_name.textChanged.connect(self._update_clock_name)
        # pack label
        self.clock_layout.addWidget(self.clock_name, alignment=Qt.AlignCenter)
        # setup timer
        self.timer = QTimer(self.clock_frame)
        self.timer.timeout.connect(lambda: self._show_time())
        self.timer.start(100)
        if self.clock_is_editable:
            self.timer_display = QLineEdit("---",self.clock_frame)
            self.timer_display.setAlignment(Qt.AlignCenter)
            self.timer_display.setDisabled(True)
            self.timer_display.setStyleSheet(self.timer_stylesheet_edit_disabled)
        else:
            self.timer_display = QLabel("---", self.clock_frame)
        self.timer_display.setObjectName(f"clockTimer{self.timer_id}")
        # pack timer
        self.clock_layout.addWidget(self.timer_display, alignment=Qt.AlignCenter)
        # setup buttons
        self.control_time_btn = QPushButton("Start", self.clock_frame)
        self.control_time_btn.clicked.connect(lambda: self._control_time())
        #self.stop_btn = QPushButton("Stop", self.clock_frame)
        #self.stop_btn.clicked.connect(lambda: self._stop_time())
        self.reset_btn = QPushButton("Reset", self.clock_frame)
        self.reset_btn.clicked.connect(lambda: self._reset_time())
        sp_retain = self.reset_btn.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.reset_btn.setSizePolicy(sp_retain)
        self.control_time_btn.setSizePolicy(sp_retain)
        # pack buttson
        self.clock_layout.addWidget(self.control_time_btn)
        #self.clock_layout.addWidget(self.stop_btn)
        self.clock_layout.addWidget(self.reset_btn)
        # append clock
        self.parent.addWidget(self.clock_frame)
        self.delete_btn = QPushButton("", self.clock_frame)
        self.delete_btn.clicked.connect(self._set_to_destroy)
        self.delete_btn.setGeometry(1,1,30,30)
        self.delete_btn.hide()
        self.change_color_btn = QPushButton("", self.clock_frame)
        self.change_color_btn.setGeometry(1, 35, 30,30)
        self.change_color_btn.hide()
        self.change_color_btn.clicked.connect(self._open_color_picker)
        self.default_enabled_color = self.change_color_btn.palette().text().color().name()
        self._update_timer_stylesheet()

    def _show_time(self):
        if self.isActive:
            self.count += 1
            # save data
        self.timer_display.setText(self._return_time())
        self._update_tray_action()

    def _return_time(self):
        time_as_int = int(self.count / 10)
        return datetime.fromtimestamp(time_as_int, timezone.utc).strftime("%H:%M:%S")

    def _disable_edit_mode(self):
        self._update_frame_stylesheet()
        print(self.clock_name.objectName())
        self.control_time_btn.show()
        self.reset_btn.show()
        self.timer_display.setEnabled(False)
        self.clock_name.setEnabled(False)
        self.delete_btn.hide()
        self.change_color_btn.hide()
        self.edit_mode = False
        self._update_timer_stylesheet()

    def _enable_edit_mode(self):
        if self.isActive:
            self.timer_display.setObjectName("activeEdit")
            self.clock_name.setObjectName("activeEdit")
        else:
            self.timer_display.setObjectName("disabledEdit")
            self.clock_name.setObjectName("disabledEdit")
        self._update_frame_stylesheet()
        self.control_time_btn.hide()
        self.reset_btn.hide()
        self.timer_display.setEnabled(True)
        self.clock_name.setEnabled(True)
        self.delete_btn.show()
        self.change_color_btn.show()
        self.edit_mode = True
        self._update_timer_stylesheet()

    def _control_time(self):
        if self.isActive:
            self._stop_time()
        else:
            self._start_time()
        if self.tray_action is None:
            return

    def _set_to_destroy(self):
        self.to_be_destroyed = True
        self.tray_object.removeAction(self.tray_action)
        self.clock_frame.hide()
        if self.app is not None:
            self.app._check_timers_for_deletion()
        #timer.clock_frame.destroy()
    
    def _open_color_picker(self):
        dialog = QColorDialog(self.clock_frame)
        dialog.setOption(QColorDialog.ShowAlphaChannel, True)  # Example of setting options
        if dialog.exec_() == QColorDialog.Accepted:
            color = dialog.currentColor()
            if color.isValid():
                self.color = color.name()
                self._update_frame_stylesheet()

    def _update_frame_stylesheet(self):
        theme = f"{self.app.config.stylesheet}_timer"#.format(self.color)
        stylesheet = getattr(Styles, theme)
        formated_stylesheet = stylesheet.format(color=f"{self.color}")
        self.clock_frame.setStyleSheet(formated_stylesheet)

    def _update_clock_name(self):
        self.name = self.clock_name.text()

    def _update_tray_action(self):
        if self.tray_action is None:
            print("Tray object is None!")
            return
        self.tray_action.setText(str(self))

    def _start_time(self):
        self.isActive = True
        self._update_timer_stylesheet()
        self.control_time_btn.setText("Stop")

    def _stop_time(self):
        self.isActive = False
        self._update_timer_stylesheet()
        self.control_time_btn.setText("Start")

    def _reset_time(self):
        self.count = 0
        
    def _update_timer_stylesheet(self):
        if self.isActive:
            if self.edit_mode:
                print("activeEdit")
                self.timer_display.setObjectName("activeEdit")
                self.clock_name.setObjectName("activeEdit")
            else:
                print("active")
                self.timer_display.setObjectName("active")
                self.clock_name.setObjectName("active")
        else:
            if self.edit_mode:
                print("disabledEdit")
                self.timer_display.setObjectName("disabledEdit")
                self.clock_name.setObjectName("disabledEdit")
            else:
                print("disabled")
                self.timer_display.setObjectName("disabled")
                self.clock_name.setObjectName("disabled")
        self._update_frame_stylesheet()
        self._update_frame_stylesheet()
        self._update_frame_stylesheet()


        return
        enabled = self.default_enabled_color
        disabled = "#989898"
        if self.edit_mode:
            stylesheet = self.timer_stylesheet_edit_enabled
        else:
            stylesheet = self.timer_stylesheet_edit_disabled
        tray_font = QtGui.QFont()
        if self.isActive:
            stylesheet += "color: %s"%enabled
            tray_font.setBold(True)
        else:
            stylesheet += "color: %s"%disabled
            tray_stylesheet = "font-weight: normal"
        self.timer_display.setStyleSheet(stylesheet)
        self.clock_name.setStyleSheet(stylesheet)
        if self.tray_action is None:
            return
        self.tray_action.setFont(tray_font) # FIXME this doesnt work well

