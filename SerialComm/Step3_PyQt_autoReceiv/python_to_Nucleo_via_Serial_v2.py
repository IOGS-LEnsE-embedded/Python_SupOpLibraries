# -*- coding: utf-8 -*-
"""
First application to send and receive data from a Nucleo board
    

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Tue Jan 26 20:34:05 2023

@author: julien.villemejane
"""

from serial import Serial
import serial.tools.list_ports
from threading import Timer, Thread, Event

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QWidget
)
from PyQt5.uic import loadUi


class RepeatTimer(Timer):  
    """
    Create Timer that repeats action at a specific time interval.
    Based on threading.Timer class

    my_timer = RepeatTimer(time, function) 

    ...
    
    Methods
    -------
    run():
        Executes a specific function when time is reached.
    """
    
    def run(self):  
        '''
        Executes a specific function when time is reached.

        Returns
        -------
        None.

        '''
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)   



class MyWindow(QMainWindow):
    """
    Create a simple GUI for serial communication with a Nucleo Board.
    The GUI is based on PyQt5.
    Tested on Nucleo-L476RG.
    @see : https://github.com/IOGS-LEnsE-embedded/Python_SupOpLibraries/blob/main/SerialComm/Step1_script/main_L476RG_Nucleo_prog.cpp

    This class requires the Python_to_Nucleo_ihm_v1.ui file,
    designed with QtDesigner.
    @see : https://github.com/IOGS-LEnsE-embedded/Python_SupOpLibraries/blob/main/SerialComm/Step2_PyQt_send/Python_to_Nucleo_ihm_v1.ui
    
    ...

    Attributes
    ----------
    ports : tuple[str]
        list of the serial ports
    comPortList : QComboBox
        graphical list object to display serial ports list
    connectBt : QButton
        graphical button object linked to the Nucleo connection function
        called connectToNucleo
    appQuitBt : QButton
        graphical button object to close the application, linked to
        quitApp function
    ledOnBt : QButton
        graphical button object to switch on the led on the Nucleo board
        linked to switchOnLed function    
    ledOffBt : QButton
        graphical button object to switch off the led on the Nucleo board
        linked to switchOffLed function   
    serNuc : Serial
        serial connection to the Nucleo board @115200 bauds
    connected : int
        flag to know if board is connected
    timer : RepeatTimer 
        timer object to test Board reception each 100 ms  
    
    
    Methods
    -------
    __init__(parent=None):
        Construct the GUI object.
    __del__():
        Destroy the GUI object.
    connectToNucleo():
        Connect GUI to the Nucleo board.    
    quitApp():
        Quit the GUI application.
    switchOnLed():
        Send command to switch on the LED on the Nucleo board.
    switchOffLed():
        Send command to switch off the LED on the Nucleo board.
    getSerialData():
        Get data from the Nucleo board, if any.
    
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("Python_to_Nucleo_ihm_v1.ui", self)
        # To obtain the list of the communication ports
        self.ports = serial.tools.list_ports.comports()
        self.ports.sort()
        # To clear the list on the window
        self.comPortList.clear()
        # To add all the communication ports to the list
        for port, desc, hwid in sorted(self.ports):
            self.comPortList.addItem(f"{port} [{desc}]")
        # To link click to actions
        self.connectBt.clicked.connect(self.connectToNucleo)
        self.appQuitBt.clicked.connect(self.quitApp)
        self.ledOnBt.clicked.connect(self.switchOnLed)
        self.ledOffBt.clicked.connect(self.switchOffLed)
        # To create an empty serial connection
        self.serNuc = Serial()
        self.connected = 0
        self.timer = RepeatTimer(0.5, self.getSerialData)  
        self.timer.start() #recalling run  
            
    def __del__(self):
        self.serNuc.close()
        self.timer.cancel()
    
    def connectToNucleo(self):
        if(self.connected == 0):
            self.selectPort = self.ports[self.comPortList.currentIndex()].name
            self.serNuc = Serial(self.selectPort, 115200)
            self.connected = 1
            self.connectBt.setEnabled(False)
            self.ledOnBt.setEnabled(True)
            self.ledOffBt.setEnabled(True)
            self.lenseLabel.setText(f"Connected to {self.selectPort}")
            
    def quitApp(self):
        self.timer.cancel()
        self.connected = 0
        self.serNuc.close()
        self.close()
        
    def switchOnLed(self):
        if(self.connected):
            self.serNuc.write(bytes('a','utf-8'))
            while self.serNuc.inWaiting() != 0:
                pass
            self.data = self.serNuc.read(1)
            self.lenseLabel.setText(f"Switch On Led ({self.data})")

    def switchOffLed(self):
        if(self.connected):
            self.serNuc.write(bytes('e','utf-8'))
            while self.serNuc.inWaiting() != 0:
                pass
            self.data = self.serNuc.read(1)
            self.lenseLabel.setText(f"Switch Off Led ({self.data})")
    
    def getSerialData(self):
        print("HERE")
        if(self.connected):
            if(self.serNuc.inWaiting() != 0):
                data_cnt = self.serNuc.inWaiting()
                print(str(data_cnt))
                self.data = self.serNuc.read(data_cnt)
                self.lenseLabel.setText(f"DATA {data_cnt}")

    def closeApp(self):
        self.timer.cancel()
        self.connected = 0
        self.close()
        self.closeEvent(None)
        
    def closeEvent(self, event):
        self.timer.cancel()
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    win = MyWindow()
    win.show()
    sys.exit(app.exec())