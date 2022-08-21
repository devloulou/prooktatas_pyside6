import sys
from random import choice

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

"""
Firstly, the windowTitleChanged signal is not always emitted when setting the window title. 
The signal only fires if the new title is changed from the previous one. 
If you set the same title multiple times, the signal will only be fired the first time. 
It is important to double-check the conditions under which signals fire, 
to avoid being surprised when using them in your app.
"""

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong'
]

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.n_times_clicked = 0

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.windowTitleChanged.connect(self.the_window_title_changed)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        print("Clicked")
        new_window_title = choice(window_titles)
        print(f"Setting title: {new_window_title}")
        self.setWindowTitle(new_window_title)   


    def the_window_title_changed(self, window_title):
        print(f"Window title changed: {window_title}")

        if window_title == "Something went wrong":
            self.button.setDisabled(True)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
