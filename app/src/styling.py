from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication


class Styles:
    # SYSTEM
    app = QApplication([])
    system = ("""
        QFrame{
            border: none;
        }
        QFrame#noClocksFrame{
        """
            f"border: 3px solid {app.palette().color(QPalette.WindowText).name()};"
        """
        }
        QFrame#noClocksFrame>QLabel {
                font-size: 12pt;
        """
            f"color: 3px solid {app.palette().color(QPalette.WindowText).name()};"
        """
            }
        QFrame#topNav {
            background: #1e1e1e;
            border: none;
            }
        QFrame#topNav>QPushButton {
            background: #1e1e1e;
            }
        QFrame#topNav>QLabel{
            background: #1e1e1e;
        }
        """)
    system_timer = ("""
        QFrame#clockFrame{{
            border-color: {color};
            border-width: 3;
            border-style: solid;
            border-radius: 4;
        }}
        QFrame#clockFrame>.QLineEdit{{
            background:transparent;
            font-size: 15pt;
        }}
        """
        """
        QLineEdit#active,QLabel#active{{
        """
            f"color: {app.palette().color(QPalette.WindowText).name()};"
        """
            background:transparent;               
            border: none;
        }}
        QLineEdit#disabled,QLabel#disabled{{
            """
            f"color: {app.palette().color(QPalette.Shadow).name()};"
            """
            border: none;
        }}
        QLineEdit#activeEdit,QLabel#activeEdit{{
        """
            f"color: {app.palette().color(QPalette.WindowText).name()};"
        """
            background:transparent;               
            border:2px solid #708ebf;
            border-radius: 5px;
        }}
        QLineEdit#disabledEdit,QLabel#disabledEdit{{
        """
            f"color: {app.palette().color(QPalette.Shadow).name()};"
        """
            background:transparent;               
            border:2px solid #708ebf;
            border-radius: 5px;
        }}
    """)
    app.exit()
    del(app)

    # LIGTH MODE
    light = """
        
        QMainWindow,QWidget {
            background: #efefef;
            color: #1e1e1e;
        }
        QFrame{
            border: none;
            background: #efefef;
        }
        QFrame#noClocksFrame{
            border: 3px solid #1e1e1e;
        }
        QFrame#noClocksFrame>QLabel {
                font-size: 12pt;
                color: #1e1e1e;
            }
        QFrame#topNav {
            background: #1e1e1e;
            border: none;
            }
        QFrame#topNav>QPushButton {
            background: #1e1e1e;
            }
        QFrame#topNav>QLabel{
            background: #1e1e1e;
        }
    """
    light_timer = """
        QFrame#clockFrame{{
            border-color: {color};
            border-width: 3;
            border-style: solid;
            border-radius: 4;
        }}
        QFrame#clockFrame>.QLineEdit{{
            background:transparent;
            font-size: 15pt;
        }}
        QLineEdit#active,QLabel#active{{
            color: #1e1e1e;
            background:transparent;               
            border: none;
        }}
        QLineEdit#disabled,QLabel#disabled{{
            color: #989898;
            border: none;
        }}
        QLineEdit#activeEdit,QLabel#activeEdit{{
            color: #1e1e1e;
            background:transparent;               
            border:2px solid #708ebf;
            border-radius: 5px;
        }}
        QLineEdit#disabledEdit,QLabel#disabledEdit{{
            color: #989898;
            background:transparent;               
            border:2px solid #708ebf;
            border-radius: 5px;
        }}

    """
        
    # DARK MODE 
    dark = """
        QMainWindow,QWidget {
            background: #121212;
            color: #FFFFFF;
        }
        QFrame{
            border: none;
            background: #121212;
        }
        QFrame#noClocksFrame{
            border: 3px solid #FFFFFF;
        }
        QFrame#noClocksFrame>QLabel {
                font-size: 12pt;
                color: #FFFFFF;
            }
        QFrame#topNav {
            background: #1e1e1e;
            border: none;
            }
        QFrame#topNav>QPushButton {
            background: #1e1e1e;
            }
        QFrame#topNav>QLabel{
            background: #1e1e1e;
        }
            """
    dark_timer = """
        QFrame#clockFrame{{
            border-color: {color};
            border-width: 3;
            border-style: solid;
            border-radius: 4;
        }}
        QFrame#clockFrame>.QLineEdit{{
            background:transparent;
            font-size: 15pt;
        }}
        QLineEdit#active,QLabel#active{{
            color: #FFFFFF;
            background:transparent;               
            border: none;
        }}
        QLineEdit#disabled,QLabel#disabled{{
            color: #989898;
            border: none;
        }}
        QLineEdit#activeEdit,QLabel#activeEdit{{
            color: #FFFFFF;
            background:transparent;               
            border:2px solid #708ebf;
            border-radius: 5px;
        }}
        QLineEdit#disabledEdit,QLabel#disabledEdit{{
            color: #989898;
            background:transparent;               
            border:2px solid #708ebf;
            border-radius: 5px;
        }}

    """
    def return_style_names(self):
        return [style for style in Styles.__dict__.keys() if not(style.endswith("_timer")) and not(style.startswith("__"))][:-1]


