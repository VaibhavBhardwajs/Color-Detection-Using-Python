from PyQt6.QtWidgets import QApplication,QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QListWidget
from PyQt6.QtCore import Qt
import os
from PyQt6.QtGui import QPixmap
import cv2
import pandas as pd

#app setting
app=QApplication([])
window=QWidget()
window.setWindowTitle("Color Detector")
window.resize(900,700)

#Widget/Objects
picture=QLabel("Image Will Appear here")
picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
picture.setStyleSheet(f"background-color: white; color: black;border: 2px solid; border-radius: 5px")
btn_load=QPushButton("Load Image")
color=QLabel("--")
color.setAlignment(Qt.AlignmentFlag.AlignCenter)
color.hide()

#App Design
master_layout=QVBoxLayout()
row1=QVBoxLayout()
row2=QVBoxLayout()

row1.addWidget(picture)
row2.addWidget(color)
row2.addWidget(btn_load)

master_layout.addLayout(row1,90)
master_layout.addLayout(row2,10)
window.setLayout(master_layout)

#all app settings
clicked=False
r=g=b=xpos=ypos=0
index=["color","color_name","hex","R","G","B"]
csv=pd.read_csv('colors.csv',names=index,header=None)
class colordetect(QWidget):
    def load_img(self):
        def __init__(self):
            super().__init__()
            self.img=None

        img_path,_ = QFileDialog.getOpenFileName(None,"Select Image", "","Image files( *.jpg;*.jpeg;*.png)")

        # Check if a file was selected
        if img_path:
            self.image=QPixmap(img_path)
            self.img=cv2.imread(img_path)
            self.show_img()

        
    
    def show_img(self):
        picture.hide()
        w,h=picture.width(),picture.height()
        self.scaled_image=self.image.scaled(w,h,Qt.AspectRatioMode.KeepAspectRatio)
        picture.setPixmap(self.scaled_image)
        picture.show()
    


    def getColorName(self,R,G,B):
        minimum=10000
        for i in range(len(csv)):
            d=abs(R- int(csv.loc[i,"R"]))+abs(G- int(csv.loc[i,"G"]))+abs(B- int(csv.loc[i,"B"]))
            if d<=minimum:
                minimum=d
                cname=csv.loc[i,"color_name"]    
        return cname

    def mousePressEvent(self,event):
        global r,g,b,xpos,ypos,clicked
        if event.button()==Qt.MouseButton.LeftButton and self.img is not None:
            #get coords
            label__pos=picture.mapFromGlobal(event.globalPosition().toPoint())
            x=label__pos.x()
            y=label__pos.y()

            #Get the scale factor
            scale_x=self.img.shape[1]/self.scaled_image.width()
            scale_y=self.img.shape[0]/self.scaled_image.height()

            #convert Qlabel coords to image coords
            x=int(x*scale_x)
            y=int(y*scale_y)

            #Ensure coords are within image
            if x>=self.img.shape[1] or y>=self.img.shape[0]:
                return

            #Get Color
            b,g,r =self.img[y,x]
            b=int(b)
            g=int(g)
            r=int(r)

            #update label
            color_name=self.getColorName(r,g,b)
            color.setText(f'Color: {color_name} | R={r} G={g} B={b}')
            color.setStyleSheet(f"background-color: rgb({r}, {g}, {b}); color: white;")
            color.show()
            clicked=True



#events
main=colordetect()
btn_load.clicked.connect(main.load_img)
window.mousePressEvent=main.mousePressEvent



window.show()
app.exec()