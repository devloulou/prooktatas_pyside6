from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QColor, QBrush,  QPixmap
from PySide6.QtCore import Qt, QRect

class BackdropImageWidget(QWidget):
    def __init__(self):
        super(BackdropImageWidget, self).__init__()
        self.backdrop_image = ""
        self.painter = QPainter()

        self.pixmap = QPixmap(self.backdrop_image)
        self.fill_brush = QBrush(QColor(0, 0, 0, 210))

    def set_backdrop_image(self, image_path):
        self.backdrop_image = image_path
        self.pixmap.load(image_path)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.draw()
        self.painter.end()

    def draw(self):
        rect = self.rect()

        scaled_image = self.pixmap.scaledToWidth(rect.width(), Qt.SmoothTransformation)

        if scaled_image.height() < rect.height():
            scaled_image = self.pixmap.scaledToHeight(rect.height(), Qt.SmoothTransformation)

        image_rect = QRect(rect.x(), rect.y(), scaled_image.width(), scaled_image.height())
        image_rect.moveCenter(rect.center())
        self.painter.drawPixmap(image_rect, scaled_image)

        self.painter.setBrush(self.fill_brush)
        self.painter.setPen(Qt.NoPen)
        self.painter.drawRect(rect)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = BackdropImageWidget()
    win.set_backdrop_image(r"C:\Users\kovac\movie_meta_images\f91517d0-c89c-4bb4-b360-b154f238b98b_backdrop.jpg")
    win.show()
    app.exec()