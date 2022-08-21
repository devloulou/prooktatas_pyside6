from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, 
                                QPushButton, QLabel, QHBoxLayout, 
                                QSizePolicy, QSpacerItem)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

from .customWidgets import BackdropImageWidget

class MovieDetails(BackdropImageWidget):
    close_details = Signal()

    def __init__(self):
        super().__init__()
        self.setVisible(False)

        main_layout = QHBoxLayout(self)

        self.poster = QLabel()
        self.poster.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.poster.setMaximumWidth(320)
        main_layout.addWidget(self.poster)

        details_layout = QVBoxLayout()
        details_layout.setAlignment(Qt.AlignTop)
        main_layout.addLayout(details_layout)

        title_layout = QHBoxLayout()
        details_layout.addLayout(title_layout)
        self.title = QLabel()
        self.title.setObjectName("movie_title")

        self.release_date = QLabel()
        self.release_date.setObjectName("small_text")

        self.rating = QLabel()
        self.rating.setObjectName("small_text")

        overview_lbl = QLabel("Overview")
        overview_lbl.setObjectName("subtitle")

        self.description = QLabel()
        self.description.setWordWrap(True)

        title_layout.addWidget(self.title)
        title_layout.addWidget(self.release_date)

        title_layout.addItem(QSpacerItem(10,10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #01d277; font-size: 16px; padding: 15px; border: none; border-radius: 5px")
        
        title_layout.addWidget(close_btn)

        play_btn = QPushButton('Play Me')
        play_btn.setStyleSheet("background-color: #01d277; font-size: 16px; padding: 15px; border: none; border-radius: 5px")
        
        details_layout.addWidget(self.rating)

        details_layout.addWidget(overview_lbl)
        details_layout.addWidget(self.description)

        main_layout.addWidget(play_btn)

        close_btn.clicked.connect(self.close_action)
        play_btn.clicked.connect(self.play_video)

    def set_movie(self, movie):
        self.movie = movie

        movie_pixmap = QPixmap(movie.poster)

        self.poster.setPixmap(movie_pixmap)
        self.title.setText(movie.title)
        self.rating.setText( f"Raing: {movie.rating}")
        self.release_date.setText(f" ({movie.release_date})"  )
        self.description.setText(movie.description)

        self.set_backdrop_image(movie.backdrop)

        self.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_action()

    def close_action(self):
        self.close_details.emit()

    def play_video(self):
        pass