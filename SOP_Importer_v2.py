import hou
import os
from PySide2 import QtWidgets

class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        self.setWindowTitle("SOP IMPORTER")
        self.setFixedSize(250, 100)

        layout = QtWidgets.QVBoxLayout(self)
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        label = QtWidgets.QLabel("Choose next options:")
        layout.addWidget(label)
        layout.addItem(spacer)

        self.shaders_checkbox = QtWidgets.QCheckBox("Create shaders")
        self.cameras_checkbox = QtWidgets.QCheckBox("Import cameras")
        self.file_button = QtWidgets.QPushButton("ChooseExternalAsRef")
        self.file_button.setFixedSize(150, 20)

        
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.file_button.clicked.connect(self.on_file_button_clicked)


        layout.addWidget(self.file_button)
        layout.addWidget(self.shaders_checkbox)
        layout.addWidget(self.cameras_checkbox)
        layout.addWidget(button_box)

    def on_file_button_clicked(self):
         file_dialog = QtWidgets.QFileDialog(self, "Open file", "", "USD Files (*.usd *.usda *.usdc)")
         file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
         if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()
            if file_path:
                self.file_button.setText(', '.join(file_path)) 
                file_paths = self.file_button.text().split(';')    
                for path in file_paths:
                    if path:
                        AssetReference_node = hou.node('/stage').createNode('assetreference')
                        AssetReference_node.parm('filepath').set(path)
                        AssetReference_node.setName(os.path.basename(path))
                        AssetReference_node.setPosition((0, 0))

                        y = -1.5
                        


    def selected_option(self):
        selected_nodes = hou.selectedNodes() 
        root_dir = hou.node('/stage/')
        once_create = False
        x, y = 0, 0

        for current_node in selected_nodes:
            if current_node.type().name() == 'geo':
                sopimport_node = root_dir.createNode('sopimport')
                sopimport_node.parm('soppath').set(current_node.path())
                sopimport_node.setName(current_node.name())
                sopimport_node.setPosition((x, y))
                
                y -= 1.5 

                matlib_node = root_dir.createNode('materiallibrary')
                matlib_node.parm('assign1').set(True)
                matlib_node.setName(f"{current_node.name()}_material")
                matlib_node.setPosition((x, y - 1.5))
                matlib_node.setInput(0, sopimport_node)

                if self.shaders_checkbox.isChecked():
                      #initialize shader node
                    mtlxstandard_surface_node = matlib_node.createNode('mtlxstandard_surface')
                    mtlxstandard_surface_node.setName(f"{current_node.name()}_shader")
                    matlib_node.parm('matnode1').set(mtlxstandard_surface_node.path())
                    y += 1.5
                   
              
                x -= 1.5

            elif current_node.type().name() == 'cam' and not once_create and self.cameras_checkbox.isChecked():
                sceneimport_node = root_dir.createNode('sceneimport::2.0')
                sceneimport_node.setName('cameras')
                sceneimport_node.parm('objects').set('*')
                sceneimport_node.parm('filter').set('Cameras')
                sceneimport_node.setPosition((x, y))  
                x -= 1.5
                once_create = True


dialog = MyDialog()
result = dialog.exec_()

if result == QtWidgets.QDialog.Accepted:
    dialog.selected_option()
else:
    print("Dialog cancelled.")
