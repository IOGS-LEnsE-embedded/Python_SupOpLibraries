# Libraries to import
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QGridLayout, QPushButton, QProgressBar
import sys
from ParametersAutoModeWindow import Parameters_AutoMode_Window

#-------------------------------------------------------------------------------------------------------

class Automatic_Mode_Widget(QWidget):
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
        self.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 2px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
        
        self.parametersAutoModeWindow = Parameters_AutoMode_Window()

        group_box = QGroupBox("Automatic Mode")

        self.setWindowTitle("Automatic Mode")

        # Creating the main layout
        layout = QGridLayout()
        
        # Creating and adding our settings
        self.parametersButton = QPushButton("Parameters")
        self.parametersButton.setStyleSheet("background: #c5e0b4; border-style: solid; border-width: 1px; font: bold; color: black")
        self.parametersButton.clicked.connect(lambda : self.parametersAutoModeWindow.show())

        self.startButton = QPushButton("START")
        self.startButton.setStyleSheet("background: #c5e0b4; border-style: solid; border-width: 1px; font: bold; color: black")
        self.startButton.clicked.connect(self.progressioBarSetValue)

        self.progressionBar = QProgressBar()


        layout.addWidget(self.parametersButton, 0, 2, 1, 1) # row = 0, column = 2, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.startButton, 0, 3, 1, 1) # row = 0, column = 3, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.progressionBar, 1, 2, 1, 2) # row = 1, column = 2, rowSpan = 1, columnSpan = 2
        

        group_box.setLayout(layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1 <=> QHBoxLayout or V

        
        self.setLayout(main_layout)

    def progressioBarSetValue(self):
        self.progressionBar.setValue(95)


# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Automatic_Mode_Widget()
    window.show()

    sys.exit(app.exec_())