import hou
import os
from PySide2 import QtWidgets
import json 

class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        
        self.input = None
        
        #window main parms
        self.setWindowTitle("Json Cam import")
        WIDTH = 300
        HEIGHT = 100
           
        #window set size
        self.setFixedSize(WIDTH, HEIGHT)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        #buttons
        self.file_button = QtWidgets.QPushButton("Choose Camera Json File")
        self.label_focallength = QtWidgets.QLabel("Focal Length:")
        self.input_focallength = QtWidgets.QLineEdit()


        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.accepted.connect(self.on_ok_clicked)
        #button connected to import func
        self.file_button.clicked.connect(self.on_file_button_clicked)
        
        layout.addWidget(self.file_button)
        layout.addWidget(self.label_focallength)
        layout.addWidget(self.input_focallength)
        layout.addWidget(button_box)
        
    #import func    
    def on_file_button_clicked(self):
    
        file_dialog = QtWidgets.QFileDialog(self, "Open file", "", "Json Files (*.json)") 
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        
        if file_dialog.exec_(): 

            file_paths = file_dialog.selectedFiles() 

            if file_paths: 

                self.file_button.setText('; '.join(file_paths))

                for path in file_paths:

                    with open(path, 'r') as camera_data:
                       
                        self.input = json.load(camera_data)
      
                        
    def on_ok_clicked(self):

        cam_node = hou.node('/obj/').createNode('cam')
        camera_transform = self.input['cameraTransform']['rows']
                       
        tx = camera_transform[0][3]
        ty = camera_transform[1][3]
        tz = camera_transform[2][3]

        cam_node.parm('tx').set(tx)
        cam_node.parm('ty').set(ty)
        cam_node.parm('tz').set(tz)

        #problem markdown. Probably need to find the right way to convert matrix 4x4 to Eulers
       #------------------------------------------------------------------------->                 
                    
        camera_rotate = self.input['cameraTransform']['rows']
                       
        rx, ry, rz = hou.Matrix4([camera_transform[0], 
                                  camera_transform[1], 
                                  camera_transform[2], 
                                  camera_transform[3]]).extractRotates()
                                  
                       
        cam_node.parm('rx').set(rx)
        cam_node.parm('ry').set(ry)
        cam_node.parm('rz').set(rz)
                            
        print('Rotatation:', rx, ry, rz)
                                                              
        cam_node.parm('resx').set(self.input['imageWidth'])        
        print(self.input['imageWidth'])
  
        cam_node.parm('resy').set(self.input['imageHeight'])
        print(self.input['imageHeight'])
                            
        #aperture
        relfocal = self.input['relativeFocalLength']
                        
        #manual focal lengh
                        
        if self.input_focallength.text(): 
            self.focalLength = float(self.input_focallength.text()) 
        else: 
            print("No focal length to compute aperture")
                        
        cam_node.parm('aperture').set(2*(self.focalLength/relfocal))

dialog = MyDialog()
result = dialog.exec_()

if result == QtWidgets.QDialog.Accepted:
    None
else:
    print("Dialog cancelled.")
