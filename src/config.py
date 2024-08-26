import configparser
from pathlib import Path
from getpass import getpass
import platform
import os
from pathlib import Path


class Config:
    def __init__(self):
        self.platform = platform.system()
        match self.platform:
            case "Linux":
                self.home_path= f"{os.getenv('HOME')}"
                self.pyclocks_path = Path(f"{self.home_path}/.config/pyclocks")
                self.pyclocks_path.mkdir(parents=True, exist_ok=True)
                self.config_path = Path(self.pyclocks_path, ".pyclocks.ini")
            #case "Windows":
            #case "Darwin":
            case _:
                raise NotImplemented("pyClocks is supported for Linux only for now!")
        self.c = configparser.ConfigParser()
        self.c.read(self.config_path)

        # GENERAL
        self.applanguage = self.c["GENERAL"]["applanguage"]
        self.usesystemtopbar = bool(int(self.c.get("GENERAL", "usesystemtopbar")))

        # DISPLAY
        self.openwindowonstart = bool(int(self.c.get("DISPLAY", "openwindowonstart")))
        self.clockdisplaymode = self.c.get("DISPLAY", "clockdisplaymode")


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



