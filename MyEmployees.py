from PyQt5.QtWidgets import *
import sys


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
        pass
    def layouts(self):
        '''deffining layouts for our application'''
        self.mainLayout=QHBoxLayout()
        self.leftLayout=QFormLayout()#employee informations
        self.rightMainLayout=QHBoxLayout()
        self.rightTopLayout=QHBoxLayout()#doesnt matter if hb or vb
        self.rightBottomLayout=QHBoxLayout()# 3buttons

        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightBottomLayout.addLayout(self.rightBottomLayout)
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightMainLayout)

def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
