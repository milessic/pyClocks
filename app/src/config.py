import configparser
from pathlib import Path
from getpass import getpass
import platform
import os
from pathlib import Path


class Config:
    default_config = """[GENERAL]
applanguage = en
usesystemtopbar = 0
runastool = 1
saveinterval = 60
alwaysontop = 0

[DISPLAY]
stylesheet = system
openwindowonstart = 1
clockdisplaymode = digital
timerwidth = 250

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
            self.saveinterval= self.c["GENERAL"]["saveinterval"]
            self.alwaysontop = self.c["GENERAL"]["alwaysontop"] # FIXME setting alwaysontop as 1

            # DISPLAY
            self.openwindowonstart = bool(int(self.c.get("DISPLAY", "openwindowonstart")))
            self.clockdisplaymode = self.c.get("DISPLAY", "clockdisplaymode")
            self.timerwidth = self.c.get("DISPLAY", "timerwidth")
            self.stylesheet = self.c.get("DISPLAY", "stylesheet")
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
        if not value or str(value) == "0":
            self._usesystemtopbar = "0"
        else:
            self._usesystemtopbar = "1"
        self.c.set("GENERAL", "usesystemtopbar", self._usesystemtopbar)

    @property
    def saveinterval(self):
        return int(float(self.c.get("GENERAL", "saveinterval")))

    @saveinterval.setter
    def saveinterval(self, value:str):
        self.c.set("GENERAL", "saveinterval", value)

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
        if not value or str(value) == "0":
            v = "0"
        else:
            v = "1"
        self.c.set("GENERAL", "runastool", v)

    @property
    def alwaysontop(self):
        return bool(int(self.c.get("GENERAL", "alwaysontop")))

    @alwaysontop.setter
    def alwaysontop(self, value):
        if not value or str(value) == "0":
            v = "0"
        else:
            v = "1"
        self.c.set("GENERAL", "alwaysontop", v)

    @property
    def timerwidth(self):
        return int(self.c.get("DISPLAY", "timerwidth"))
    
    @timerwidth.setter
    def timerwidth(self,value):
        try:
            value = int(float(value))
        except:
            return
        self.c.set("DISPLAY", "timerwidth", str(value))

    @property
    def stylesheet(self):
        return self.c.get("DISPLAY", "stylesheet")

    @stylesheet.setter
    def stylesheet(self, value):
        # TODO add validation
        self.c.set("DISPLAY", "stylesheet", value)






