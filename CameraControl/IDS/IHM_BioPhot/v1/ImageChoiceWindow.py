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


class Image_Choice_Window(QWidget):
    """
    Main Widget of our Main Window.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, imageNumber):
        """
        Initialisation of the main Widget.
        """
        super().__init__()
        self.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 1px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")

        self.setWindowTitle("Image " + str(imageNumber) + "Choice")

        layout = QGridLayout()

        imagelabel = QLabel("Image " + str(imageNumber))
        imagelabel.setStyleSheet("border-style: none;")

        self.imageChoiceLine = QLineEdit()
        self.imageChoiceLine.setStyleSheet("background: white; color: black;")

        self.imagePreview = QPushButton("Image Preview")
        self.imagePreview.setStyleSheet("background: #c5e0b4; color: black;")
        self.imagePreview.clicked.connect(self.preview)

        self.imageSave = QPushButton("Save Image")
        self.imageSave.setStyleSheet("background: #c5e0b4; color: black;")
        self.imageSave.clicked.connect(self.save)

        self.imageView = QLabel()
        self.imageView.setStyleSheet("background-color: #4472c4; border-width: 2px; padding: 20px;")
        

        layout.addWidget(imagelabel, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.imageChoiceLine, 0, 1, 1, 3) # row = 0, column = 1, rowSpan = 1, columnSpan = 3
        layout.addWidget(self.imagePreview, 1, 0, 1, 2) # row = 1, column = 0, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.imageSave, 2, 0, 1, 2) # row = 2, column = 0, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.imageView, 3, 1, 3, 3) # row = 3, column = 1, rowSpan = 3, columnSpan = 3

        self.setLayout(layout)

    def preview(self):
        print("Image preview push button : clicked.")

    def save(self):
        print("Image save push button : clicked.")



#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Image_Choice_Window(1)
    window.show()

    sys.exit(app.exec_())
