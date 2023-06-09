import sys
import json
import os
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from pathlib import Path
import json

if os.path.isfile('./config/config.json') == False:
    shutil.copy2('./config/default_config.json', './config/config.json')
with open('./config/config.json', 'r') as f:
    config = json.load(f)

qt_creator_file = "renamemirrors.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class MirrorModel(QtCore.QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(MirrorModel, self).__init__(*args, **kwargs)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = MirrorModel()
        self.load()
        #self.addButton.pressed.connect(self.list1)
        self.path1.returnPressed.connect(self.list1fill)

    def load(self):
        self.list1fill(config['paths'][0])
        self.list1.itemDoubleClicked.connect(self.listDoubleClick)

    def list1fill(self, path=None):
        if (path is None):
            path = self.path1.text()
        self.path1.setText(path)
        directory = Path(path)
        #directories = [entry for entry in directory.iterdir() if entry.is_dir()]
        directories = [entry for entry in directory.iterdir()]
        self.list1.clear()
        self.list1.addItem('[. .]')
        for dir_name in directories:
            if (dir_name.is_dir()):
                name = '[' + dir_name.name + ']'
            else:
                name = dir_name.name
            self.list1.addItem(name)

    def listDoubleClick(self, item):
        path = self.path1.text().strip(os.sep)
        itemText = item.text()
        isBack = False
        if (itemText == '[. .]'):
            isBack = True
        isDir = False
        if (itemText[0] == '['):
            isDir = True
            itemText = itemText.strip('[').strip(']')
        if (isBack):
            path = os.path.dirname(path)
        else:
            path = path + os.sep + itemText
        print(path)
        if isDir:
            self.list1fill(path)


    

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
