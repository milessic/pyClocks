from src.__init__ import VERSION
from return_version import return_version
import sys

file_name = sys.argv[1]
with open(file_name, "r") as f:
    lines = f.readlines()
    lines[2] = f"Version={VERSION.removeprefix('v')}\n"
    lines[6] = f"Name=pyClocks{return_version()}\n"
    lines[5] = f"Exec=~/Programs/pyClocks{return_version()}\n"
with open(file_name, "w") as f:
    f.writelines(lines)
    
print(f"{file_name} version updated")
