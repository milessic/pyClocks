class Styles:
    system = """
        QFrame{
            border: none;
        }
        """
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
    dark = """
            #no_clocks_frame{
                border: 3px solid #FFFFFF;
            }
            """
