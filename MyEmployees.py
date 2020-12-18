from PyQt5.QtWidgets import *
import sys
import sqlite3
from PyQt5.QtGui import QFont,QPixmap
import sys ,os
from PIL import Image # pillow is a huge package we just need Image
connection = sqlite3.connect("employees.db")
cursor = connection.cursor()
defaultImage="person.png" #if the employee dosnt have a picture

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Employees")
        self.setGeometry(450, 150, 750, 600)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        self.employeesList = QListWidget()
        self.btnNew = QPushButton("New")
        self.btnNew.clicked.connect(self.addEmployee)
        self.btnUpdate = QPushButton("Update")
        self.btnDelete = QPushButton("Delete")

    def layouts(self):
        '''deffining layouts for our application'''
        ##################Layout#########################
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QFormLayout()  # employee informations
        self.rightMainLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()  # doesnt matter if hb or vb
        self.rightBottomLayout = QHBoxLayout()  # 3buttons
        ###################Adding child layouts to main layouts##############
        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightMainLayout.addLayout(self.rightBottomLayout)
        self.mainLayout.addLayout(self.leftLayout, 40)  # 40% space area
        self.mainLayout.addLayout(self.rightMainLayout, 60)  # 60% space area
        ##################Adding widgets to layouts###################
        self.rightTopLayout.addWidget(self.employeesList)
        self.rightBottomLayout.addWidget(self.btnNew)
        self.rightBottomLayout.addWidget(self.btnUpdate)
        self.rightBottomLayout.addWidget(self.btnDelete)
        ########################Setting main layout####################
        self.setLayout(self.mainLayout)

    def addEmployee(self):
        self.newEmployee = AddEmployee()
        self.close()


class AddEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Employee")
        self.setGeometry(450, 150, 350, 600)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        #########################top layouts widgets##################
        self.setStyleSheet("background-color: white;font-size: 14pt;font-family:Times")
        self.title=QLabel("Add person")
        self.title.setStyleSheet("font-size: 24pt;font-family:Arial bold ;background-color:orange")
        self.imgAdd=QLabel()
        self.imgAdd.setPixmap(QPixmap("icons/person.png"))
        ########################bottom layouts widgets###############
        self.nameLbl = QLabel("Name :")
        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Employee Name")
        self.surnameLbl = QLabel("Surname :")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setPlaceholderText("Enter Employee surname")

        self.phoneLbl = QLabel("Phone :")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter Employee phone number")

        self.emailLbl = QLabel("Email :")
        self.emailEntry = QLineEdit()
        self.emailEntry.setPlaceholderText("Enter Employee email")

        self.nameLbl = QLabel("Name :")
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Employee Name")

        self.imgLbl=QLabel("Picture :")
        self.imgButton=QPushButton("Browse")
        self.imgButton.setStyleSheet("background-color:orange;font-size:10pt;font-family:Arial")
        self.imgButton.clicked.connect(self.uploadImage)

        self.addressLbl=QLabel("Address :")
        self.addressEditor=QTextEdit()
        self.addButton=QPushButton("Add")
        self.addButton.setStyleSheet("background-color:orange;font-size:10pt;font-family:Arial")


    def layouts(self):
        ####################creating main layouts################
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        ######################creating child layouts to main layouts#######3
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ######################## adding widgets to layouts#################
                    #####top layout####
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.imgAdd)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(100,20,100,30)#left,top,right,bottom
                    #####Bottom layout#######
        self.bottomLayout.addRow(self.nameLbl,self.nameEntry)
        self.bottomLayout.addRow(self.surnameLbl,self.surnameEntry)
        self.bottomLayout.addRow(self.phoneLbl,self.phoneEntry)
        self.bottomLayout.addRow(self.emailLbl,self.emailEntry)
        self.bottomLayout.addRow(self.imgLbl,self.imgButton)
        self.bottomLayout.addRow(self.addressLbl,self.addressEditor)
        self.bottomLayout.addRow("",self.addButton)
        ####################setting main layout for our second window########
        self.setLayout(self.mainLayout)

    def uploadImage(self):
        global defaultImage
        size=(128,128)#tuple width and hight
        self.fileName,ok=QFileDialog.getOpenFileName(self,"Upload image",'',"Image Files (*.jpg *.png")
        if ok:
            defaultImage=os.path.basename(self.fileName)#il nous donne le nom du picture.png sans tout le path
                                                        #replacing newfileName by defaultImage
            img=Image.open(self.fileName)#i used self.fileNAme bcz i need all the url
            img=img.resize(size)
            img.save("images/{}".format(defaultImage))# we are saving our chosen image in the image folder


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
