from PyQt5.QtWidgets import (
        QHBoxLayout,
        QFrame,
        QLabel,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QVBoxLayout,
        QWidget,
        QCheckBox,
        QComboBox,
        )
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class SettingsController(QMainWindow):
    fields = [
            [
                "Use System Topbar",
                "combobox",
                "usesystemtopbar",
                ["Yes", "No"]
                ],
            [
                "Open Window When Starting",
                "combobox",
                "openwindowonstart",
                ["Yes", "No"]
            ],
            [
                "App language",
                "combobox",
                "applanguage",
                ["en", "pl"],
            ],
            [
                "Clock Display Mode",
                "combobox",
                "clockdisplaymode",
                ["digital", "analog"],
            ],
        ]
    dragging = False
    def __init__(self, app, custom_top_nav:bool=True):
        super().__init__()
        self.app = app
        self.icon_topnav_path = self.app.icon_topnav_path
        self.custom_top_nav = custom_top_nav
        self.app_name = self.app.app_name + " Settings"
        self.initUi()
        if self.custom_top_nav:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window )


    def initUi(self):
        self.setWindowTitle(self.app_name)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
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
            self.top_nav = MyTopNav(self, self.top_nav_frame, self.icon_topnav_path)

            self.main_layout.addWidget(self.top_nav_frame)
        # set settings frame
        self.settings_frame = QFrame(self)
        self.main_layout.addWidget(self.settings_frame)
        self.setup_form()

    def setup_form(self):
        self.form_layout = QVBoxLayout()
        for field in self.fields:
            field_layout = QHBoxLayout()
            field_label = QLabel(field[0], self)
            field_label.setFixedWidth(230)
            match field[1]:
                case "checkbox":
                    element = QCheckBox(self)
                case "input":
                    element = QLineEdit(self)
                case "combobox":
                    element = QComboBox(self)
                    for opt in field[3]:
                        element.addItem(opt)
                case _:
                    QMessageBox.critical(self, "Error", f"Cannot set field '{field}'!")
            element.setObjectName(field[2])
            field.append(element)
            field_layout.addWidget(field_label)
            field_layout.addWidget(element)
            self.form_layout.addLayout(field_layout)
        self.form_btn = QPushButton("Save settings", self)
        self.form_btn.clicked.connect(self._update_config)
        self.main_layout.addLayout(self.form_layout)

    def _update_config(self):
        # read inputs
        for field in self.fields:
            match field[1]:
                case "checkbox":
                    value = field[-1].isChecked()
                case "input":
                    value = field[-1].text()
                case "combobox":
                    value = field[-1].currentText()
                    if value.lower() == "yes":
                        value = True
                    elif value.lower() == "no":
                        value = False
                case _:
                    raise NotImplemented(f"Field type '{field[1]}' is not supported.")
            setattr(self.app.config, field[2], value)
        # save inputs
        self.app.config.update_config_file()
    def _close(self):
        self.destroy()
        pass

    def _minimize(self):
        pass
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
        
class MyTopNav():
    def __init__(self, app_window, parent, icon_topnav_path):
        self.app_window = app_window
        self.parent = parent
        self.icon_topnav_path = icon_topnav_path
        self.initUi()

    def initUi(self):
            self.top_nav = QHBoxLayout(self.parent)
            self.top_nav.setContentsMargins(0,0,0,0)
            # setup left side
            self.top_nav_left = QHBoxLayout()
            self.top_nav_left.setAlignment(Qt.AlignLeft)
            self.top_nav_left.setContentsMargins(10, 0, 10, 0)
            self.top_nav_icon_pixmap = QtGui.QPixmap()
            self.top_nav_icon_pixmap.load(self.icon_topnav_path)
            #self.top_nav_icon_pixmap.scaledToHeight(30)
            #self.top_nav_icon_pixmap.scaled(10, 10)
            self.top_nav_icon = QLabel()
            self.top_nav_icon.setPixmap(self.top_nav_icon_pixmap)
            self.top_nav_name = QLabel(self.app_window.app_name, None)

            self.top_nav_left.addWidget(self.top_nav_icon)
            self.top_nav_left.addWidget(self.top_nav_name)

            # setup right side
            self.top_nav_right = QHBoxLayout()
            self.top_nav_right.setContentsMargins(10,0,10,0)
            self.top_nav_right.setSpacing(3)
            self.top_nav_right.setAlignment(Qt.AlignRight)
            self.close_btn = QPushButton("x", self.parent)
            self.close_btn.setFixedWidth(25)
            self.close_btn.setFixedHeight(25)
            self.close_btn.clicked.connect(self.app_window._close)
            self.minimize_btn = QPushButton("-", self.parent)
            self.minimize_btn.setFixedWidth(25)
            self.minimize_btn.setFixedHeight(25)
            self.minimize_btn.clicked.connect(lambda: self.app_window._minimize())
            self.top_nav_right.addWidget(self.minimize_btn, alignment=Qt.AlignRight)
            self.top_nav_right.addWidget(self.close_btn, alignment=Qt.AlignRight)

            # add Layouts
            self.top_nav.addLayout(self.top_nav_left)
            self.top_nav.addLayout(self.top_nav_right)
