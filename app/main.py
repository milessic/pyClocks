from src.app import ClocksApp
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QFontDatabase
import sys
import platform
import os
import json

font_path = os.path.join(os.path.dirname(__file__), "src/FiraCodeNerdFont-Regular.ttf")
# detect system
match platform.system():
    case "Linux":
        app_path = f"{os.getenv('HOME')}/.config/pyclocks"
    case "Windows":
        app_path = f"{os.getenv('APPDATA')}/pyclocks"
    case "Darwin":
        app_path = f"{os.getenv('HOME')}/.config/pyclocks"
    case _:
        print(f"Platform '{platform.system()}' not supported!")
        exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont(font_path)
    font = QFontDatabase.applicationFontFamilies(font_id)[0]
    if "--debug" in sys.argv:
        print(font_path)
    timers_path = f"{app_path}/default.json"
    for i, arg in enumerate(sys.argv):
        if arg == "-d":
            timers_path = sys.argv[i+1]
            continue
        if arg.startswith("-d"):
            timers_path = arg[2:]
            continue
    window = ClocksApp(
            timers_data_path=timers_path,
            clocks_app_folder_path=app_path,
            use_system_top_nav=False,
            nerd_font=font,
            )
    # run app
    sys.exit(app.exec_())
exit()
