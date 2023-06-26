# Libraries to import
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGroupBox, QGridLayout, QPushButton, QComboBox
import sys


#-------------------------------------------------------------------------------------------------------

class Hardware_Connection_Widget(QWidget):
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
        self.setStyleSheet("background-color: #c55a11; border-radius: 10px; border-width: 2px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
        
        group_box = QGroupBox("Hardware Connection")

        self.setWindowTitle("Hardware Connection")

        # Creating the main layout
        layout = QGridLayout()
        
        # Creating and adding our settings
        labelPiezo = QLabel("Piezo")
        labelPiezo.setStyleSheet("border-style: none")

        labelDMD = QLabel("DMD")
        labelDMD.setStyleSheet("border-style: none")

        self.hardwareSelectionComboBox = QComboBox()
        self.hardwareSelectionComboBox.setStyleSheet("background: #fff2cc; border-style: solid; border-width: 1px; font: bold; color: black;")

        self.connectionPushButton = QPushButton("Connection")
        self.connectionPushButton.setStyleSheet("background: #c5e0b4; border-style: solid; border-width: 1px; font: bold; color: black")
        self.connectionPushButton.clicked.connect(self.connection)

        layout.addWidget(labelPiezo, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1
        layout.addWidget(labelDMD, 1, 0, 1, 1) # row = 1, column = 0, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.hardwareSelectionComboBox, 0, 1, 1, 1) # row = 0, column = 1, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.connectionPushButton, 1, 1, 1, 1) # row = 1, column = 1, rowSpan = 1, columnSpan = 1
        
        

        group_box.setLayout(layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1 <=> QHBoxLayout or V

        
        self.setLayout(main_layout)

    def connection(self):
        print("Connection button clicked : connection.")

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Hardware_Connection_Widget()
    window.show()

    sys.exit(app.exec_())