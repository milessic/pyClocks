from src.clocks import ClocksApp
from PyQt5.QtWidgets import QApplication
import sys
import os
import json

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timers_path = f"{os.getenv('HOME')}/.pyclocks.json"
    for i, arg in enumerate(sys.argv):
        if arg == "-d":
            timers_path = sys.argv[i+1]
            continue
        if arg.startswith("-d"):
            timers_path = arg[2:]
            continue
    window = ClocksApp(
            timers_data_path=timers_path,
            clocks_app_folder_path=os.path.join(str(os.getenv('HOME')),".pyclocks/"))
    window.show()
    sys.exit(app.exec_())
exit()
