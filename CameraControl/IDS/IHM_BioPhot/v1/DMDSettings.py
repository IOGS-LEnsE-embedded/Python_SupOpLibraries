# Libraries to import
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGroupBox, QGridLayout, QPushButton
import sys
from ImageChoiceWindow import Image_Choice_Window

#-------------------------------------------------------------------------------------------------------

class DMD_Settings_Widget(QWidget):
    """
    Widget used to set our less important options.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self):
        """
        Initialisation of our widget.
        """
        super().__init__()
        self.setStyleSheet("background-color: #c55a11; border-radius: 10px; border-width: 1px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
        
        group_box = QGroupBox("DMD Settings")

        self.setWindowTitle("DMD Settings")

        #Creating image choice window to show them later
        self.imageChoiceWindowWidget1 = Image_Choice_Window(1)
        self.imageChoiceWindowWidget2 = Image_Choice_Window(2)
        self.imageChoiceWindowWidget3 = Image_Choice_Window(3)



        # Creating the main layout
        layout = QGridLayout()
        
        self.apercuTestPushButton = QPushButton("View Test")
        self.apercuTestPushButton.setStyleSheet("background: #c5e0b4; color: black;")
        self.apercuTestPushButton.clicked.connect(self.ApercuPushButton)

        self.testPushButton = QPushButton("TEST")
        self.testPushButton.setStyleSheet("background: #c5e0b4; color: black;")
        self.testPushButton.clicked.connect(self.TestPushButton)

        self.imageChoiceLoad1 = Image_Choice_Load_Widget(1)
        self.imageChoiceLoad1.imageChoicePushButton.clicked.connect(lambda : self.imageChoiceWindowWidget1.show())
        self.imageChoiceLoad1.loadButton.clicked.connect(self.ImageLoad1)

        self.imageChoiceLoad2 = Image_Choice_Load_Widget(2)
        self.imageChoiceLoad2.imageChoicePushButton.clicked.connect(lambda : self.imageChoiceWindowWidget2.show())
        self.imageChoiceLoad2.loadButton.clicked.connect(self.ImageLoad2)

        self.imageChoiceLoad3 = Image_Choice_Load_Widget(3)
        self.imageChoiceLoad3.imageChoicePushButton.clicked.connect(lambda : self.imageChoiceWindowWidget3.show())
        self.imageChoiceLoad3.loadButton.clicked.connect(self.ImageLoad3)

        layout.addWidget(self.apercuTestPushButton, 0, 2, 1, 1) # row = 0, column = 2, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.testPushButton, 0, 3, 1, 1) # row = 0, column = 3, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.imageChoiceLoad1, 1, 0, 1, 4) # row = 1, column = 0, rowSpan = 1, columnSpan = 4
        layout.addWidget(self.imageChoiceLoad2, 2, 0, 1, 4) # row = 2, column = 0, rowSpan = 1, columnSpan = 4
        layout.addWidget(self.imageChoiceLoad3, 3, 0, 1, 4) # row = 3, column = 0, rowSpan = 1, columnSpan = 4
        

        group_box.setLayout(layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1 <=> QHBoxLayout or V

        
        self.setLayout(main_layout)

    def ApercuPushButton(self):
        print("Apercu Push Button : clicked.")

    def TestPushButton(self):
        print("Test Push Button : clicked.")

    def ImageLoad1(self):
        print("Image Load 1 Push Button : clicked.")

    def ImageLoad2(self):
        print("Image Load 2 Push Button : clicked.")

    def ImageLoad3(self):
        print("Image Load 3 Push Button : clicked.")

class Image_Choice_Load_Widget(QWidget):
    """
    Widget used to set our less important options.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, imageNumber):
        """
        Initialisation of our widget.
        """
        super().__init__()
        self.setStyleSheet("")

        layout = QGridLayout()

        imageNumberLabel = QLabel("Image " + str(imageNumber))
        imageNumberLabel.setStyleSheet("border-style: none; color: white;")

        self.imageChoicePushButton = QPushButton("Image Choice")
        self.imageChoicePushButton.setStyleSheet("background: #c5e0b4; color: black;")

        self.loadButton = QPushButton("LOAD")
        self.loadButton.setStyleSheet("background: #c5e0b4; color: black;")

        layout.addWidget(imageNumberLabel, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1 
        layout.addWidget(self.imageChoicePushButton, 0, 1, 1, 2) # row = 0, column = 1, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.loadButton, 0, 3, 1, 1) # row = 0, column = 3, rowSpan = 1, columnSpan = 1 

        self.setLayout(layout)
        

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DMD_Settings_Widget()
    window.show()

    sys.exit(app.exec_())