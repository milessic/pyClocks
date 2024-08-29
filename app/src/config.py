import configparser
from pathlib import Path
from getpass import getpass
import platform
import os
from pathlib import Path


class Config:
    default_config = """[GENERAL]
applanguage = en
noidea = confusediam
usesystemtopbar = 0
runastool = 1

[DISPLAY]
openwindowonstart = 1
clockdisplaymode = digital

    """
    def __init__(self, app_path):
        self.platform = platform.system()
        self.pyclocks_path = Path(app_path)
        self.pyclocks_path.mkdir(parents=True, exist_ok=True)
        self.config_path = Path(self.pyclocks_path, ".pyclocks.ini")
        #case "Windows":
        #case "Darwin":
        self.c = configparser.ConfigParser()
        self.c.read(self.config_path)
        if len(self.c) < 2:
            self._create_new_config()

        try:
            # GENERAL
            self.applanguage = self.c["GENERAL"]["applanguage"]
            self.usesystemtopbar = bool(int(self.c.get("GENERAL", "usesystemtopbar")))
            self.runastool = bool(int(self.c["GENERAL"]["runastool"]))

            # DISPLAY
            self.openwindowonstart = bool(int(self.c.get("DISPLAY", "openwindowonstart")))
            self.clockdisplaymode = self.c.get("DISPLAY", "clockdisplaymode")
        except:
            self._create_new_config()
            

    def _create_new_config(self):
        del self.c
        print("Didn't detect valid config file, creating default one")
        with open(self.config_path, "w") as f:
            f.write(self.default_config)
        self.c = configparser.ConfigParser()
        self.c.read(self.config_path)

    def _save_config(self):
        with open(self.config_path, "w") as f:
            self.c.write(f)

    def update_config_file(self):
        self._save_config()

    @property
    def applanguage(self):
        return self.c["GENERAL"]["applanguage"]

    @applanguage.setter
    def applanguage(self, value:str):
        # TODO supported language check
        self._applanguage = value
        self.c.set("GENERAL", "applanguage", value)

    @property
    def usesystemtopbar(self):
        return bool(int(self.c["GENERAL"]["usesystemtopbar"]))

    @usesystemtopbar.setter
    def usesystemtopbar(self, value:bool):
        if value:
            self._usesystemtopbar = "1"
        else:
            self._usesystemtopbar = "0"
        self.c.set("GENERAL", "usesystemtopbar", self._usesystemtopbar)

    @property
    def openwindowonstart(self):
        return bool(int(self.c["DISPLAY"]["openwindowonstart"]))
    
    @openwindowonstart.setter
    def openwindowonstart(self, value:bool):
        if value:
            self._openwindowonstart = "1"
        else:
            self._openwindowonstart = "0"
        self.c.set("DISPLAY", "openwindowonstart", self._openwindowonstart)

    @property
    def clockdisplaymode(self):
        return self.c["DISPLAY"]["clockdisplaymode"]

    @clockdisplaymode.setter
    def clockdisplaymode(self, value):
        self.c.set("DISPLAY", "clockdisplaymode", value)

    @property
    def runastool(self):
        return bool(int(self.c.get("GENERAL", "runastool")))

    @runastool.setter
    def runastool(self, value):
        v = "0"
        if value:
            v = "1"
        self.c.set("GENERAL", "runastool", v)



