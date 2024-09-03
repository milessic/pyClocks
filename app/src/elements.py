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

class SettingsController(QWidget):
    fields = [
            [
                "Use System Topbar\n\t(not recommended)",
                "combobox",
                "usesystemtopbar",
                ["Yes", "No"],
                True
            ],
            [
                "Keep always-on-top",
                "combobox",
                "alwaysontop",
                ["Yes","No"],
                False
            ],
            [
                "Run As Tool\n\t(visible only from Tray)",
                "combobox",
                "runastool",
                ["Yes", "No"],
                False
            ],
            [
                "Saving interval\n\t(in seconds)",
                "input",
                "saveinterval",
                None,
                False
            ],
            [
                "Open Window When Starting",
                "combobox",
                "openwindowonstart",
                ["Yes", "No"],
                True

            ],
            [
                "Timer width\n\t(in pixels)",
                "input",
                "timerwidth",
                None,
                False
            ],
#            [
#                "App language",
#                "combobox",
#                "applanguage",
#                ["en", "pl"],
#            ],
#            [
#                "Clock Display Mode",
#                "combobox",
#                "clockdisplaymode",
#                ["digital", "analog"],
#            ],
        ]
    dragging = False
    def __init__(self, app, custom_top_nav:bool=True):
        super().__init__()
        self.reload_needed = False
        self.app = app
        self.nerd_font = self.app.nerd_font
        self.icon_topnav_path = self.app.icon_topnav_path
        self.setWindowIcon(self.app.icon)
        self.custom_top_nav = self.app.custom_top_nav
        self.app_name = self.app.app_name + " Settings"
        self.initUi()
        self._set_window_flags()
        #if self.custom_top_nav:
        #    self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window )
        #else:
        #    pass
            #self.setWindowFlags(Qt.Window )

    # def __del__(self):
        # TODO make additional app that will run and show QMessageBox in this case
        #if not self.custom_top_nav:
        #    QMessageBox.critical(self, "PyClocks Info", "Closing settings closes also app if system topbar is used!")

    def _set_window_flags(self):
        flags = Qt.Window
        for flag in self.app.flags:
            flags |= flag
        self.setWindowFlags( flags )


    def initUi(self):
        #self.setWindowTitle(self.app_name)
        #self.main_widget = QWidget(self)
        #self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self)
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
        self.base_config = self._get_form_data()

    def setup_form(self):
        self.form_layout = QVBoxLayout(self.settings_frame)
        self.app_description = QLabel(self.app.short_description, self)
        self.form_layout.addWidget(self.app_description)
        for field in self.fields:
            field_layout = QHBoxLayout()
            field_label = QLabel(field[0], self)
            field_label.setFixedWidth(230)
            field_default_value = getattr(self.app.config,field[2])
            if isinstance(field_default_value, bool):
                match field_default_value:
                    case True:
                        field_default_value = "Yes"
                    case False:
                        field_default_value = "No"
            elif isinstance(field_default_value, int):
                field_default_value = str(field_default_value)
            match field[1]:
                case "checkbox":
                    element = QCheckBox(self)
                    element.setChecked(field_default_value)
                case "input":
                    element = QLineEdit(self)
                    element.setText(field_default_value)
                case "combobox":
                    element = QComboBox(self)
                    for opt in field[3]:
                        element.addItem(opt)
                    index = element.findText(field_default_value)
                    element.setCurrentIndex(index)
                case _:
                    QMessageBox.critical(self, "Error", f"Cannot set field '{field}'!")
                    return
            element.setObjectName(field[2])
            field.append(element)
            field_layout.addWidget(field_label)
            field_layout.addWidget(element)
            self.form_layout.addLayout(field_layout)
        self.buttons_layout = QHBoxLayout()
        self.form_btn = QPushButton("Save settings", self)
        self.form_btn.clicked.connect(self._update_config)
        self.form_btn.setMaximumWidth(150)
        self.settings_saved = QLabel("Settings saved, window may be closed", self)
        self.settings_saved.setStyleSheet("color: green")
        self.settings_saved.hide()
        self.buttons_layout.addWidget(self.form_btn, alignment=Qt.AlignLeft)
        self.buttons_layout.addWidget(self.settings_saved, alignment=Qt.AlignLeft)
        self.form_layout.addLayout(self.buttons_layout)

    def show(self):
        super().show()
        if self.reload_needed:
            return
        self.base_config = self._get_form_data()

    def _get_form_data(self) -> list:
        data = []
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
            data.append((field[2],value,field[4]))
        return data

    def _update_config(self):
        # read inputs
        data = self._get_form_data()
        # set values
        for field in data:
            setattr(self.app.config, field[0], field[1])
        # save inputs
        self.app.config.update_config_file()
        # show user that it happened
        self.settings_saved.show()
        for base, actual in zip(self.base_config, data):
            if not base[2]: # skip if field does not need reset
                continue
            if actual[1] != base[1]:
                self.reload_needed = True
        if self.reload_needed:
            QMessageBox.information(self, "pyClocks - reload needed", "Some changes need app restart")
            self.base_config = self._get_form_data()
            self.reload_needed = False
        self.app._reload_settings()

    def _close(self):
        self.settings_saved.hide()
        self.destroy()

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
    def __init__(self, app_window, parent, icon_topnav_path, show_settings:bool=False,show_edit:bool=False):
        self.app_window = app_window
        self.show_settings = show_settings
        self.show_edit = show_edit
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
            self.top_nav_name.setStyleSheet("color: #dfdfdf")

            self.top_nav_left.addWidget(self.top_nav_icon)
            self.top_nav_left.addWidget(self.top_nav_name)

            # setup right side
            self.top_nav_right = QHBoxLayout()
            self.top_nav_right.setContentsMargins(10,0,10,0)
            self.top_nav_right.setSpacing(3)
            self.top_nav_right.setAlignment(Qt.AlignRight)
            
            # edit button
            if self.show_edit:
                self.edit_btn = QPushButton("", self.parent)
                #print(self.edit_btn.palette().text().color().name())
                #self.edit_btn.setIcon(self.app_window.settings_icon)
                self.edit_btn.setFixedWidth(25)
                self.edit_btn.setFixedHeight(25)
                self.edit_btn.clicked.connect(lambda: self.app_window._control_edit_mode())
                self.edit_btn.setStyleSheet("color: #dfdfdf")
                if self.app_window.nerd_font is not None:
                    self.edit_btn.setFont(QtGui.QFont(self.app_window.nerd_font))

            # edit button
            if self.show_settings:
                self.settings_btn = QPushButton("", self.parent)
                #self.settings_btn.setIcon(self.app_window.edit_icon)
                self.settings_btn.setFixedWidth(25)
                self.settings_btn.setFixedHeight(25)
                self.settings_btn.clicked.connect(lambda: self.app_window.show_settings())
                self.settings_btn.setStyleSheet("color: #dfdfdf")
                if self.app_window.nerd_font is not None:
                    self.settings_btn.setFont(QtGui.QFont(self.app_window.nerd_font))

            # minimize button
            self.minimize_btn = QPushButton("󰖰", self.parent)
            self.minimize_btn.setFixedWidth(25)
            self.minimize_btn.setFixedHeight(25)
            self.minimize_btn.clicked.connect(lambda: self.app_window._minimize())
            self.minimize_btn.setStyleSheet("color: #dfdfdf")
            if self.app_window.nerd_font is not None:
                self.minimize_btn.setFont(QtGui.QFont(self.app_window.nerd_font))

            # close button
            self.close_btn = QPushButton("", self.parent)
            self.close_btn.setFixedWidth(25)
            self.close_btn.setFixedHeight(25)
            self.close_btn.clicked.connect(self.app_window._close)
            self.close_btn.setStyleSheet("color: #dfdfdf")
            if self.app_window.nerd_font is not None:
                self.close_btn.setFont(QtGui.QFont(self.app_window.nerd_font))

            # place widgets
            if self.show_settings:
                self.top_nav_right.addWidget(self.edit_btn, alignment=Qt.AlignRight)
                self.top_nav_right.addWidget(self.settings_btn, alignment=Qt.AlignRight)
            self.top_nav_right.addWidget(self.minimize_btn, alignment=Qt.AlignRight)
            self.top_nav_right.addWidget(self.close_btn, alignment=Qt.AlignRight)

            # add Layouts
            self.top_nav.addLayout(self.top_nav_left)
            self.top_nav.addLayout(self.top_nav_right)
