from PyQt5.QtWidgets import *
import sys
import sqlite3
from PyQt5.QtGui import QFont, QPixmap
import sys, os
from PIL import Image  # pillow is a huge package we just need Image

connection = sqlite3.connect("employees.db")
cursor = connection.cursor()
defaultImage = "person.png"  # if the employee dosnt have a picture
person_id=None #variable globale pour l'utiliser dun classe a l'autre. on peut pas utiliser self

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
        self.getEmployee()
        self.displayFirstRecord()
    def mainDesign(self):
        self.setStyleSheet("font-size: 14pt;font-family:Arial Bold;")
        self.employeesList = QListWidget()
        self.employeesList.itemClicked.connect(self.singleClick)
        self.btnNew = QPushButton("New")
        self.btnNew.clicked.connect(self.addEmployee)
        self.btnUpdate = QPushButton("Update")
        self.btnUpdate.clicked.connect(self.updateEmployee)
        self.btnDelete = QPushButton("Delete")
        self.btnDelete.clicked.connect(self.deleteEmployee)
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

    def getEmployee(self):
        query="SELECT id,name,sirname FROM employees"
        employees=cursor.execute(query).fetchall() #records
        #i dont use commit func bcz we are not changing anything in the data base
        #using for loop to exctract them
        for employee in employees:
            print (employee)#returns a tuple
            self.employeesList.addItem(str(employee[0])+"-"+employee[1]+"-"+employee[2])#str bcz id is an integer
    def displayFirstRecord(self):
        #to display one record : oredre by rowid ascending and the limit is 1 (1record)
        query="SELECT * FROM employees ORDER BY ROWID ASC LIMIT 1"# iwantnt to display every feild
        employee=cursor.execute(query).fetchone()
        img =QLabel()
        img.setPixmap(QPixmap("images/{}".format(employee[5])))
        name=QLabel(employee[1])
        surname=QLabel(employee[2])
        phone=QLabel(employee[3])
        email=QLabel(employee[4])
        address=QLabel(employee[6])
        self.leftLayout.setVerticalSpacing(20)#20 pixels between each widget
        self.leftLayout.addRow("",img)
        self.leftLayout.addRow("Name:",name)
        self.leftLayout.addRow("Surname: ",surname)
        self.leftLayout.addRow("Phone: ",phone)
        self.leftLayout.addRow("Email: ",email)
        self.leftLayout.addRow("Address: ",address)

    def singleClick(self):
        ####delete previous wigets and replace them with the chosen person###
        for i in reversed(range(self.leftLayout.count())):
            widget=self.leftLayout.takeAt(i).widget()
            print(widget)
            if widget is not None:
                widget.deleteLater()
        #######replacing the deleted widgets by the selected ones###########
        employee=self.employeesList.currentItem().text()
        id=employee.split("-")[0]#we used split to get the id from our string and search in databbase using the id
        print(id)
        query=("SELECT * FROM employees WHERE id=?")
        person=cursor.execute(query,(id,)).fetchone()#after query we should use a tuple / so a single item tuple=(1,)
        print(person)
        img = QLabel()
        img.setPixmap(QPixmap("images/{}".format(person[5])))
        name = QLabel(person[1])
        surname = QLabel(person[2])
        phone = QLabel(person[3])
        email = QLabel(person[4])
        address = QLabel(person[6])
        self.leftLayout.setVerticalSpacing(20)  # 20 pixels between each widget
        self.leftLayout.addRow("", img)
        self.leftLayout.addRow("Name:", name)
        self.leftLayout.addRow("Surname: ", surname)
        self.leftLayout.addRow("Phone: ", phone)
        self.leftLayout.addRow("Email: ", email)
        self.leftLayout.addRow("Address: ", address)

    def deleteEmployee(self):
        if self.employeesList.selectedItems():
            person=self.employeesList.currentItem().text()
            id = person.split("-")[0]
            nbox=QMessageBox.question(self,"WARNING","Are you sure you wante to delete this person?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if nbox == QMessageBox.Yes:#whenever you want to change something in database you need to use try except block
                try:
                    query="DELETE FROM employees WHERE id=?"
                    cursor.execute(query,(id,))#tuple
                    connection.commit()
                    QMessageBox.information(self, "Information", "Person has not been deleted !!")
                    #after deleting the person we should update our window by closing and openning it
                    self.close()
                    self.main=Main()

                except :
                    QMessageBox.information(self,"WARNING","Person has not been deleted !!")
        else:
            QMessageBox.information(self,"Warning","Please select a person first ")

    def updateEmployee(self):
        global person_id
        if self.employeesList.selectedItems():
            person =self.employeesList.currentItem().text()
            person_id=person.split("-")[0]
            self.updateWindow=UpdateEmployee()
            self.close()

        else:
            QMessageBox.information(self,"Warning","Please selecte a person to update")


############################ UpdateEmployee Class #########################
class UpdateEmployee(QWidget):
    def __init__(self):
        print("Ahhhhhhh class")
        super().__init__()
        self.setWindowTitle("Update Employee")
        self.setGeometry(450, 150, 350, 600)
        self.UI()
        self.show()

    def UI(self):
        self.getPerson()
        self.mainDesign()
        self.layouts()


    def closeEvent(self, QCloseEvent):# when we close the seconde window we obtaine a close event
        self.main=Main()        #whenever we close the seconde windows
                                #we return to the first one by creating the main class everytime
                                #main class contains self.show so it appears by itself
    def getPerson(self):
        global person_id
        query="SELECT * FROM employees WHERE id=?"
        employee=cursor.execute(query,(person_id,)).fetchone()#employee => (4,'john','snow','+95151315','jon@gmail.com',"person.pmg","winterfall")
        print("employee",employee)
        self.name=employee[1]
        self.surname=employee[2]
        self.phone=employee[3]
        self.email=employee[4]
        self.image=employee[5]
        self.address=employee[6]

    def mainDesign(self):

        #########################top layouts widgets##################
        self.setStyleSheet("background-color: white;font-size: 14pt;font-family:Times")
        self.title = QLabel("Update person")
        self.title.setStyleSheet("font-size: 24pt;font-family:Arial bold ;background-color:orange")
        self.imgAdd = QLabel()
        self.imgAdd.setPixmap(QPixmap("images/{}".format(self.image)))
        ########################bottom layouts widgets###############
        self.nameLbl = QLabel("Name :")
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.name)

        #self.nameEntry.setPlaceholderText("Enter Employee Name")
        self.surnameLbl = QLabel("Surname :")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setText(self.surname)
        #self.surnameEntry.setPlaceholderText("Enter Employee surname")

        self.phoneLbl = QLabel("Phone :")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setText(self.phone)
        #self.phoneEntry.setPlaceholderText("Enter Employee phone number")

        self.emailLbl = QLabel("Email :")
        self.emailEntry = QLineEdit()
        self.emailEntry.setText(self.email)
        #self.emailEntry.setPlaceholderText("Enter Employee email")

        # self.nameLbl = QLabel("Name :")
        # self.nameEntry = QLineEdit()
        # #self.nameEntry.setPlaceholderText("Enter Employee Name")

        self.imgLbl = QLabel("Picture :")
        self.imgButton = QPushButton("Browse")
        self.imgButton.setStyleSheet("background-color:orange;font-size:10pt;font-family:Arial")
        self.imgButton.clicked.connect(self.uploadImage)

        self.addressLbl = QLabel("Address :")
        self.addressEditor = QTextEdit()
        self.addressEditor.setText(self.address)
        self.addButton = QPushButton("Update")
        self.addButton.setStyleSheet("background-color:orange;font-size:10pt;font-family:Arial")
        self.addButton.clicked.connect(self.updateEmployee)

    def layouts(self):
        ####################creating main layouts################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        ######################creating child layouts to main layouts#######3
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ######################## adding widgets to layouts#################
        #####top layout####
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.imgAdd)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(100, 20, 100, 30)  # left,top,right,bottom
        #####Bottom layout#######
        self.bottomLayout.addRow(self.nameLbl, self.nameEntry)
        self.bottomLayout.addRow(self.surnameLbl, self.surnameEntry)
        self.bottomLayout.addRow(self.phoneLbl, self.phoneEntry)
        self.bottomLayout.addRow(self.emailLbl, self.emailEntry)
        self.bottomLayout.addRow(self.imgLbl, self.imgButton)
        self.bottomLayout.addRow(self.addressLbl, self.addressEditor)
        self.bottomLayout.addRow("", self.addButton)
        ####################setting main layout for our second window########
        self.setLayout(self.mainLayout)

    def uploadImage(self):
        global defaultImage
        size = (128, 128)  # tuple width and hight
        self.fileName, ok = QFileDialog.getOpenFileName(self, "Upload image", '', "Image Files (*.jpg *.png")
        if ok:
            defaultImage = os.path.basename(self.fileName)  # il nous donne le nom du picture.png sans tout le path
            # replacing newfileName by defaultImage
            img = Image.open(self.fileName)  # i used self.fileNAme bcz i need all the url
            img = img.resize(size)
            img.save("images/{}".format(defaultImage))  # we are saving our chosen image in the image folder

    def updateEmployee(self):
        global defaultImage
        global person_id
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        img = defaultImage
        address = self.addressEditor.toPlainText()
        if (name and surname and phone != ""):
            try:  # if you want to make a data base record we should use try exept
                query = "UPDATE employees set name =?, sirname=?, phone=?, email=?, image=?,address=? WHERE id=?" #update function
                cursor.execute(query, (name, surname, phone, email, img, address,person_id))
                connection.commit()
                QMessageBox.information(self, "Success", "Person has been updated")
                self.close() #it returns to the main window grace a close event
            except:
                QMessageBox.warning(self, "Warning", "Person has not been updated")
        else:
            QMessageBox.warning(self, "WARNING", "Fields can not be empty")















######################################Add EMployee Class#################################
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


    def closeEvent(self, QCloseEvent):# when we close the seconde window we obtaine a close event
        self.main=Main()        #whenever we close the seconde windows
                                #we return to the first one by creating the main class everytime
                                #main class contains self.show so it appears by itself

    def mainDesign(self):
        #########################top layouts widgets##################
        self.setStyleSheet("background-color: white;font-size: 14pt;font-family:Times")
        self.title = QLabel("Add person")
        self.title.setStyleSheet("font-size: 24pt;font-family:Arial bold ;background-color:orange")
        self.imgAdd = QLabel()
        self.imgAdd.setPixmap(QPixmap("icons/person.png"))
        ########################bottom layouts widgets###############
        self.nameLbl = QLabel("Name :")
        self.nameEntry = QLineEdit()
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

        # self.nameLbl = QLabel("Name :")
        # self.nameEntry = QLineEdit()
        # self.nameEntry.setPlaceholderText("Enter Employee Name")

        self.imgLbl = QLabel("Picture :")
        self.imgButton = QPushButton("Browse")
        self.imgButton.setStyleSheet("background-color:orange;font-size:10pt;font-family:Arial")
        self.imgButton.clicked.connect(self.uploadImage)

        self.addressLbl = QLabel("Address :")
        self.addressEditor = QTextEdit()
        self.addButton = QPushButton("Add")
        self.addButton.setStyleSheet("background-color:orange;font-size:10pt;font-family:Arial")
        self.addButton.clicked.connect(self.newEmployee)

    def layouts(self):
        ####################creating main layouts################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        ######################creating child layouts to main layouts#######3
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ######################## adding widgets to layouts#################
        #####top layout####
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.imgAdd)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(100, 20, 100, 30)  # left,top,right,bottom
        #####Bottom layout#######
        self.bottomLayout.addRow(self.nameLbl, self.nameEntry)
        self.bottomLayout.addRow(self.surnameLbl, self.surnameEntry)
        self.bottomLayout.addRow(self.phoneLbl, self.phoneEntry)
        self.bottomLayout.addRow(self.emailLbl, self.emailEntry)
        self.bottomLayout.addRow(self.imgLbl, self.imgButton)
        self.bottomLayout.addRow(self.addressLbl, self.addressEditor)
        self.bottomLayout.addRow("", self.addButton)
        ####################setting main layout for our second window########
        self.setLayout(self.mainLayout)

    def uploadImage(self):
        global defaultImage
        size = (128, 128)  # tuple width and hight
        self.fileName, ok = QFileDialog.getOpenFileName(self, "Upload image", '', "Image Files (*.jpg *.png")
        if ok:
            defaultImage = os.path.basename(self.fileName)  # il nous donne le nom du picture.png sans tout le path
            # replacing newfileName by defaultImage
            img = Image.open(self.fileName)  # i used self.fileNAme bcz i need all the url
            img = img.resize(size)
            img.save("images/{}".format(defaultImage))  # we are saving our chosen image in the image folder

    def newEmployee(self):
        global defaultImage
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        img = defaultImage
        address = self.addressEditor.toPlainText()
        if (name and surname and phone != ""):
            try:  # if you want to make a data base record we should use try exept
                query = "INSERT INTO employees (name,sirname,phone,email,image,address) VALUES (?,? ,?, ?, ?,?)"
                cursor.execute(query, (name, surname, phone, email, img, address))
                connection.commit()
                QMessageBox.information(self, "Success", "Person has been added")
                self.close() #it returns to the main window grace a close event
            except:
                QMessageBox.warning(self, "Warning", "Person has not been added")
        else:
            QMessageBox.warning(self, "WARNING", "Fields can not be empty")


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
