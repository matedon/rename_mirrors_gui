import sys
import json
import os
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from pathlib import Path
import json

if os.path.isfile('./config/config.json') == False:
    shutil.copy2('./config/default_config.json', './config/config.json')
with open('./config/config.json', 'r') as f:
    config = json.load(f)

class MirrorModel(QtCore.QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(MirrorModel, self).__init__(*args, **kwargs)



class MainWindow(QtWidgets.QMainWindow):
    clNum = 0
    paths = []
    lists = []

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('renamemirrors.ui', self)
        self.model = MirrorModel()
        self.load()

    def duplicateLayout(self):
        self.clNum = self.clNum + 1
        layout2 = QVBoxLayout()
        #cwName = self.layoutv1.objectName() + '__c' + str(self.clNum)
        #self.layouth1.addLayout(self.layout2, objectName = cwName)
        self.layouth1.addLayout(layout2)

        # Iterate over widgets in layoutv1
        for index in range(self.layoutv1.count()):
            widget = self.layoutv1.itemAt(index).widget()
            if widget is not None:
                cwName = widget.objectName() + '__' + str(self.clNum)
                cw = type(widget)(objectName = cwName)
                layout2.addWidget(cw)
                cw.installEventFilter(self)
                if "path" in cw.objectName():
                    self.paths.append(cw)
                    # TODO: DOUBLECLICK NOT WORKS!
                    cw.itemDoubleClicked = self.listDoubleClick
                if "list" in cw.objectName():
                    self.lists.append(cw)

    def eventFilter(self, obj, event):
        #print('eventFilter', event.type(), obj.objectName())
        if event.type() == QtCore.QEvent.KeyPress and "path" in obj.objectName():
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                self.listFill(obj.text(), int(obj.objectName().split('__')[1]))
                return True
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.single_click_timer.start()
            return True
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.single_click_timer.stop()
            print('double click')
            return True
        return super(MainWindow, self).eventFilter(obj, event)

    def load(self):
        self.single_click_timer = QtCore.QTimer()
        self.single_click_timer.setInterval(200)
        self.single_click_timer.timeout.connect(self.single_click)

        self.paths.append(self.path1)
        self.lists.append(self.list1)
        self.listFill(config['paths'][0])
        self.list1.itemDoubleClicked.connect(self.listDoubleClick)
        #self.addButton.pressed.connect(self.list1)
        self.path1.returnPressed.connect(self.listFill)
        self.dev1.clicked.connect(self.duplicateLayout)

    def single_click(self):
        self.single_click_timer.stop()
        print('timeout, must be single click')

    def listFill(self, route=None, num=0):
        path = self.paths[num]
        list = self.lists[num]
        if (route is None):
            route = path.text()
        path.setText(route)
        directory = Path(route)
        directories = [entry for entry in directory.iterdir()]
        list.clear()
        list.addItem('[. .]')
        for dir_name in directories:
            if (dir_name.is_dir()):
                name = '[' + dir_name.name + ']'
            else:
                name = dir_name.name
            list.addItem(name)

    def listDoubleClick(self, item):
        path = self.path1.text().rstrip(os.sep)
        itemText = item.text()
        isBack = False
        if (itemText == '[. .]'):
            isBack = True
        isDir = False
        if (itemText[0] == '['):
            isDir = True
            itemText = itemText.lstrip('[').rstrip(']')
        if (isBack):
            path = os.path.dirname(path)
        else:
            path = path + os.sep + itemText
        print(path)
        if isDir:
            self.listFill(path)


    

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
