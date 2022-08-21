import sys

from PySide6.QtWidgets import QApplication, QWidget

# egy application instance kell applikációnként
# ha nem kell command line argument, akkor a QApplication([]) is elég
app = QApplication(sys.argv)

# QWidget maga az ablak
window = QWidget()
window.show()

app.exec_()