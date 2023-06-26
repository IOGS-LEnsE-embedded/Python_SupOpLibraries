# Libraries to import
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from CameraWidget import Camera_Widget
from CameraSettings import Camera_Settings_Widget
from HardwareConnection import Hardware_Connection_Widget
from DMDSettings import DMD_Settings_Widget
from AutomaticMode import Automatic_Mode_Widget
from PiezoControl import Piezo_Control_Widget

#-------------------------------------------------------------------------------------------------------

"""
Colors :    Green  : #c5e0b4
            Blue   : #4472c4
            Orange : #c55a11
            Beige  : #fff2cc
            Grey1  : #f2f2f2
            Grey2  : #bfbfbf
"""



class MainWidget(QWidget):
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

        self.setStyleSheet("background: #f2f2f2;")
        # Create the several widgets
        self.cameraWidget = Camera_Widget()
        self.cameraSettingsWidget = Camera_Settings_Widget()
        self.hardwareConnectionWidget = Hardware_Connection_Widget()
        self.DMDSettingsWidget = DMD_Settings_Widget()
        self.automaticModeWidget = Automatic_Mode_Widget()
        self.piezoControlWidget = Piezo_Control_Widget()

        # Create and add the widgets into the layout
        layoutMain = QGridLayout()
        self.setLayout(layoutMain)

        layoutMain.addWidget(self.cameraWidget, 0, 0, 4, 4) # row = 0, column = 0, rowSpan = 4, columnSpan = 4
        layoutMain.addWidget(self.cameraSettingsWidget, 4, 0, 3, 4) # row = 5, column = 0, rowSpan = 3, columnSpan = 4
        layoutMain.addWidget(self.hardwareConnectionWidget, 0, 5, 1, 4) # row = 0, column = 4, rowSpan = 1, columnSpan = 3
        layoutMain.addWidget(self.DMDSettingsWidget, 1, 5, 2, 4) # row = 1, column = 5, rowSpan = 2, columnSpan = 4
        layoutMain.addWidget(self.automaticModeWidget, 3, 5, 1, 4) # row = 3, column = 5, rowSpan = 1, columnSpan = 4
        layoutMain.addWidget(self.piezoControlWidget, 4, 5, 3, 4) # row = 3, column = 5, rowSpan = 1, columnSpan = 4

        self.cameraWidget.connectCamera()
        self.cameraWidget.launchVideo()

        self.initSettings()


    def initSettings(self):
        """
        Method used to setup the settings.
        """

        # Initialisation of the exposure setting
        self.cameraSettingsWidget.exposureTime.floatListToSelect = self.cameraWidget.generateExpositionRangeList(1000)
        self.cameraSettingsWidget.exposureTime.slider.setRange(0, len(self.cameraSettingsWidget.exposureTime.floatListToSelect) - 1)
        self.cameraSettingsWidget.exposureTime.setValue(15)

        self.cameraSettingsWidget.exposureTime.slider.valueChanged.connect(
            lambda : self.cameraWidget.camera.set_exposure(self.cameraSettingsWidget.exposureTime.value))


        # Initialisation of the FPS setting
        minFPS, maxFPS = self.cameraWidget.getFPSRange()
        self.cameraSettingsWidget.FPS.slider.setMinimum(minFPS)
        self.cameraSettingsWidget.FPS.slider.setMaximum(maxFPS)

        self.cameraSettingsWidget.FPS.slider.valueChanged.connect(
            lambda : self.cameraWidget.camera.set_frame_rate(self.cameraSettingsWidget.FPS.getValue()))
        self.cameraSettingsWidget.FPS.slider.valueChanged.connect(
            lambda : print(f"FPS : {self.cameraWidget.camera.get_frame_rate()}"))
        
        self.cameraSettingsWidget.FPS.setValue(self.cameraSettingsWidget.FPS.getValue())

        # Initialisation of the BlackLevel setting
        self.cameraSettingsWidget.blackLevel.slider.setMinimum(1)
        self.cameraSettingsWidget.blackLevel.slider.setMaximum(256)
        #         self.cameraSettingsWidget.blackLevel.setValue(int(self.cameraWidget.camera.get_black_level())) # camera's blacklevel

        self.cameraSettingsWidget.blackLevel.slider.valueChanged.connect(
            lambda : self.cameraWidget.camera.set_black_level(self.cameraSettingsWidget.blackLevel.getValue()))

#-------------------------------------------------------------------------------------------------------

class MainWindow(QMainWindow):
    """
    Our main window.

    Args:
        QMainWindow (class): QMainWindow can contain several widgets.
    """
    def __init__(self):
        """
        Initialisation of the main Window.
        """
        super().__init__()

        # Variables

        # Define Window title
        self.setWindowTitle("BioPhot")
        #self.setGeometry(50, 50, 1200, 800)

        # Set the widget as the central widget of the window
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
