source ~/Repos/venvs/venv_pyqt5/bin/activate
python3 -m PyInstaller main.py -n pyClocks$(python3 return_version.py) --add-data=src:src --onefile
