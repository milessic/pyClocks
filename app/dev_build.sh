source ~/Repos/venvs/venv_pyqt5/bin/activate
echo "python3 -m PyInstaller main.py -n pyClocksDev$(python3 return_version.py) --add-data=src:src --onefile"
python3 -m PyInstaller main.py -n pyClocksDev$(python3 return_version.py) --add-data=src:src --onefile
