from PyQt5.QtWidgets import *
import sys
import sqlite3

connection = sqlite3.connect("employees.db")
cursor = connection.cursor()


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

    def mainDesign(self):
        pass
    def layouts(self):
        ####################creating main layouts################
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        ######################creating child layouts to main layouts#######3
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.bottomLayout)

        ####################setting main layout for our second window########
        self.setLayout(self.mainLayout)


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
