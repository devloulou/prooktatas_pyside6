import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.button_is_cheked = True
        self.setWindowTitle("My App")


        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        # ez a signal - 
        self.button.clicked.connect(self.the_button_was_toggled)
        self.button.setChecked(self.button_is_cheked)

        self.setCentralWidget(self.button)

    def the_button_was_toggled(self, checked):
        # self.button_is_cheked = checked
        self.button_is_cheked = self.button.isChecked()
        print('Checked?', checked)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
