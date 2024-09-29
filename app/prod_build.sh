source ~/Repos/venvs/venv_pyqt5/bin/activate
VERSION=$(python3 return_version.py)
APP_NAME="pyClocks${VERSION}"
echo "Creating build for version $APP_NAME"
# build
python3 -m PyInstaller main.py -n $APP_NAME --add-data=src:src --onefile --clean
# create folder to be archived
echo -e "\nCreating folder with ${APP_NAME}"
mkdir $APP_NAME
cp pyclocks.desktop ./$APP_NAME/pyclocks.desktop
cp pyClocks.ico ./$APP_NAME
cp ./dist/$APP_NAME $APP_NAME
python3 update_version_in_desktop.py "./${APP_NAME}/pyclocks.desktop"
# create targz
echo -e "\nCreating targz"
tar -czvf "./dist/${APP_NAME}.tar.gz" "./${APP_NAME}" 
cd ..
rm -rf $APP_NAME
echo "Created and archived build for $APP_NAME"
