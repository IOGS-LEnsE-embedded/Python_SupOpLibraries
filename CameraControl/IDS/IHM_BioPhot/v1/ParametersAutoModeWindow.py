# Libraries to import
import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QPushButton, QLabel, QLineEdit, QPushButton

"""
Colors :    Green  : #c5e0b4
            Blue   : #4472c4
            Orange : #c55a11
            Beige  : #fff2cc
            Grey1  : #f2f2f2
            Grey2  : #bfbfbf
"""


class Parameters_AutoMode_Window(QWidget):
    """
    Main Widget of our Main Window.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self):
        """
        Initialisation of the main Widget.
        """
        super().__init__()
        self.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 1px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")

        self.setWindowTitle("Parameters AutoMode Window")

        layout = QGridLayout()

        directoryLabel = QLabel("Directory")
        directoryLabel.setStyleSheet("border-style: none;")

        self.directoryPushButton = QPushButton("Directory")
        self.directoryPushButton.setStyleSheet("background: #c5e0b4; color: black;")
        self.directoryPushButton.clicked.connect(lambda : self.directory())


        zDisplacementLabel = QLabel("Z displacement")
        zDisplacementLabel.setStyleSheet("border-style: none;")

        self.zDisplacementLine = QLineEdit()
        self.zDisplacementLine.setStyleSheet("background: white; color: black;")

        zStepLabel = QLabel("Z Step")
        zStepLabel.setStyleSheet("border-style: none;")

        self.zStepLine = QLineEdit()
        self.zStepLine.setStyleSheet("background: white; color: black;")

        self.saveParametersPushButton = QPushButton("Save Parameters")
        self.saveParametersPushButton.setStyleSheet("background: #c5e0b4; color: black;")
        self.saveParametersPushButton.clicked.connect(lambda : self.saveParameters())

        

        layout.addWidget(directoryLabel, 0, 0, 1, 2) # row = 0, column = 0, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.directoryPushButton, 0, 2, 1, 2) # row = 0, column = 2, rowSpan = 1, columnSpan = 2
        layout.addWidget(zDisplacementLabel, 1, 0, 1, 2) # row = 1, column = 0, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.zDisplacementLine, 1, 3, 1, 1) # row = 1, column = 3, rowSpan = 1, columnSpan = 1
        layout.addWidget(zStepLabel, 2, 0, 1, 2) # row = 2, column = 0, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.zStepLine, 2, 3, 1, 1) # row = 2, column = 3, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.saveParametersPushButton, 3, 0, 1, 2) # row = 3, column = 0, rowSpan = 1, columnSpan = 2

        self.setLayout(layout)

    def directory(self):
        print("Directory push button : clicked.")

    def saveParameters(self):
        print("Save parameters push button : clicked.")



#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Parameters_AutoMode_Window(1)
    window.show()

    sys.exit(app.exec_())
