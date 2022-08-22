import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QFileDialog

from modules.movie_browser import MovieBrowser
from modules.movie_details import MovieDetails
from helpers.movie_db import get_popular_movies
from helpers.file_helper import get_files

class MovieLibrary(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Library")
        self.resize(1000, 800)
        self.showMaximized()

        central_Widget = QWidget()
        self.setCentralWidget(central_Widget)

        main_layout = QVBoxLayout(central_Widget)
        main_layout.setContentsMargins(0,0,0,0)

        # main menu
        menu = self.menuBar()

        settings_menu = menu.addMenu("&Content")

        add_folder_action = QAction("Add Folder", settings_menu)
        add_folder_action.triggered.connect(self.add_folder_action)
        settings_menu.addAction(add_folder_action)

        # add_movie_action = QAction("Add Movie", settings_menu)
        # add_movie_action.triggered.connect(self.add_movie_acion)
        # settings_menu.addAction(add_movie_action)

        # settings_menu.addSeparator()

        add_popular_movies = QAction("Add Popular Movies", settings_menu)
        add_popular_movies.triggered.connect(self.add_popular_movies)
        settings_menu.addAction(add_popular_movies)

        settings_menu.addSeparator()

        # manage_folder_action = QAction("Manage Movies", settings_menu)
        # manage_folder_action.triggered.connect(self.manage_movies_action)
        # settings_menu.addAction(manage_folder_action)

        self.movie_browser = MovieBrowser()
        main_layout.addWidget(self.movie_browser)

        self.movie_details = MovieDetails()
        main_layout.addWidget(self.movie_details)

        self.movie_browser.movie_list.show_detail.connect(self.show_details)
        self.movie_details.close_details.connect(self.hide_details)

    def show_details(self, movie):
        self.movie_browser.setVisible(False)

        self.movie_details.setVisible(True)
        self.movie_details.set_movie(movie)

    def hide_details(self):
        self.movie_browser.setVisible(True)
        self.movie_details.setVisible(False)

    def add_folder_action(self):
        folder = QFileDialog.getExistingDirectory(self, "Select folder:", "c:")

        if folder:
            self.movie_browser.movie_list.create_movies(get_files(folder))

    def add_movie_acion(self):
        files = QFileDialog.getOpenFileNames(self, "Select movie files:", "c:", "Movie File (*.mkv)")

    def add_popular_movies(self):
        popular_movie_list = get_popular_movies()

        file_list = [f"movieDB/{i['original_title']}" for i in popular_movie_list]

        self.movie_browser.movie_list.create_movies(file_list)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MovieLibrary()
    win.show()
    app.exec()