# Libraries to import
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGroupBox, QSlider, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt
import sys
import math
import numpy as np

#-------------------------------------------------------------------------------------------------------

class Piezo_Control_Widget(QWidget):
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
        
        group_box = QGroupBox("Piezo Control")

        self.setWindowTitle("Piezo Control")

        # Creating the main layout
        layout = QGridLayout()
        
        # Creating and adding our settings
        self.ZAxis = Setting_Widget_Float(settingLabel = " Z Axis ")
        self.FineZ = Setting_Widget_Int(settingLabel = " Fine Z ")

        label = QLabel("Final Value")
        label.setStyleSheet("border-style: none")

        self.finalValueLine =  QLineEdit()
        self.finalValueLine.setStyleSheet("background-color: white; padding: 4px; color: black; border-style: solid; border-width: 1px;")


        layout.addWidget(self.ZAxis, 0, 0, 1, 3) # row = 0, column = 0, rowSpan = 1, columnSpan = 3
        layout.addWidget(self.FineZ, 1, 0, 1, 3) # row = 1, column = 0, rowSpan = 1, columnSpan = 3

        layout.addWidget(label, 2, 1, 1, 1) # row = 2, column = 1, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.finalValueLine, 2, 2, 1, 1) # row = 2, column = 2, rowSpan = 1, columnSpan = 1



        group_box.setLayout(layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 0 <=> QHBoxLayout or V

        
        self.setLayout(main_layout)

#-------------------------------------------------------------------------------------------------------

class Setting_Widget_Int(QWidget):
    """
    Our sub-setting widget.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, settingLabel, minimumValue = 0, maximumValue = 100, initialisationValue = 50):
        """
        Initialisation of our setting widget.

        Args:
            settingLabel (str): name of the setting box
            minimumValue (int, optional): minimum value of the setting. Defaults to 0.
            maximumValue (int, optional): maximum value of the setting. Defaults to 100.
            initialisationValue (int, optional): base value of the setting. Defaults to 50.
        """
        super().__init__()
        
        self.setStyleSheet("border-style: none")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(minimumValue)
        self.slider.setMaximum(maximumValue)
        self.slider.setValue(initialisationValue)
        self.selectionLabel = settingLabel

        layout = QGridLayout()


        # Create a line widget and place it into the grid layout
        self.line = QLineEdit(self)
        self.line.setStyleSheet("background-color: white; padding: 4px; color: black; border-style: solid; border-width: 1px;")
        layout.addWidget(self.line, 0, 6, 1, 2) # row = 0, column = 6, rowSpan = 1, columnSpan = 2
        self.line.textChanged.connect(self.linetextValueChanged)
        self.slider.valueChanged.connect(self.sliderValueChanged)

        # Create a label widget and place it into the grid layout
        self.labelValue = QLabel(self.selectionLabel +"= " + str(initialisationValue))
        layout.addWidget(self.labelValue, 0, 0, 1, 2) # row = 0, column = 1, rowSpan = 1, columnSpan = 2

        layout.addWidget(self.slider, 0, 2, 1, 4) # row = 0, column = 2, rowSpan = 1, columnSpan = 4


        self.setLayout(layout)

    def linetextValueChanged(self, text):
        """
        Method used to set the self.value, self and the labelValue text each time the line is triggered.

        Args:
            text (str): string that'll be converted in float to changed the important values.
        """
        self.value = int(text)
        self.labelValue.setText(self.selectionLabel + "= " + str(text))
        self.slider.setValue(int(text))

    def sliderValueChanged(self, value):
        """
        Method used to set the self.value and and the labelValue text each time the slider is triggered.

        Args:
            value (int): useful value of the slider.
        """
        self.value = value
        self.labelValue.setText(self.selectionLabel + "= "+ str(value))

    def getValue(self):
        """
        Method used to get the value of the slider.

        Returns:
            int: value of the slider.
        """
        return self.slider.value()

    def setValue(self, value):
        """
        Method used to get the value of the slider.

        Args:
            value (int):  useful value of the slider.

        Raises:
            ValueError: Out of bounds.
        """
        if value < self.slider.minimum() or value > self.slider.maximum():
            raise ValueError("Value is out of range")
        self.slider.setValue(value)

#-------------------------------------------------------------------------------------------------------

class Setting_Widget_Float(QWidget):
    """
    Widget designed to select a value in a list.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, settingLabel, floatListToSelect = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]):
        """
        Initialiszation of the widget.

        Args:
            selectionLabel (str): name given to the box and to the unit.
            floatListToSelect (list): list that will be described by the slider.
        """
        super().__init__()
        self.floatListToSelect = floatListToSelect
        self.selectionLabel = settingLabel
        self.value = 0.01
        self.initUI()

    def initUI(self):
        """
        Sub-initialization method
        """
        self.setStyleSheet("border-style: none")

        layout = QGridLayout()

        # Create a line widget and place it into the grid layout
        self.line = QLineEdit(self)
        self.line.setStyleSheet("background-color: white; padding: 4px; color: black; border-style: solid; border-width: 1px;")
        layout.addWidget(self.line, 0, 6, 1, 2) # row = 0, column = 6, rowSpan = 1, columnSpan = 2
        self.line.textChanged.connect(self.linetextValueChanged)

        # Create a label widget and place it into the grid layout
        self.labelValue = QLabel()
        layout.addWidget(self.labelValue, 0, 0, 1, 2) # row = 0, column = 1, rowSpan = 1, columnSpan = 2

        # Create a slider widget and place it into the grid layout
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, len(self.floatListToSelect) - 1)
        self.slider.valueChanged.connect(self.sliderValueChanged)

        layout.addWidget(self.slider, 0, 2, 1, 4) # row = 0, column = 2, rowSpan = 1, columnSpan = 4
        
        self.setLayout(layout)

    def sliderValueChanged(self, value):
        """
        Method used to set the self.value and and the labelValue text each time the slider is triggered.

        Args:
            value (float): useful value of the slider.
        """
        self.value = self.floatListToSelect[value]
        self.labelValue.setText(self.selectionLabel + "= "+ str(math.floor(self.value * 100) / 100))

    def linetextValueChanged(self, text):
        """
        Method used to set the self.value, self and the labelValue text each time the line is triggered.

        Args:
            text (str): string that'll be converted in float to changed the important values.
        """
        self.value = float(text)
        self.labelValue.setText(self.selectionLabel + str(math.floor(float(text) * 100) / 100))
        self.setValue(float(text))
    
    def setValue(self, value):
        """
        Method used to set the value of the slider without using a long line each time.
        It sets the nearest value present in the list from the real value to the slider.

        Args:
            value (float): near value that will be put.
        """
        self.slider.setValue(np.argmin(np.abs(self.floatListToSelect - value)))

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Piezo_Control_Widget()
    window.show()

    sys.exit(app.exec_())
