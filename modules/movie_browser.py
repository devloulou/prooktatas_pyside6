
import os

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLineEdit, \
    QPushButton, QListWidget, QListWidgetItem, QItemDelegate, QStyle, QProgressBar, QTreeWidget, \
    QTreeWidgetItem, QHeaderView
from PySide6.QtGui import QPen, QBrush, QColor, QPixmap
from PySide6.QtCore import Qt, QSize, QRect, Signal, QThread


from helpers.mongo_helper import MongoHelper
from objects.movie import Movie


class MovieBrowser(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignTop)

        # self.search_bar = SearchBar()
        # main_layout.addWidget(self.search_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.movie_list = MovieList()
        main_layout.addWidget(self.movie_list)

        self.movie_list.movie_downloader.download_started.connect(self.start_progress)
        self.movie_list.movie_downloader.download_progress.connect(self.download_progress)
        self.movie_list.movie_downloader.download_progress_finished.connect(self.progress_bar.setVisible)


    def start_progress(self, movie_list_length):
        self.progress_bar.setMaximum(movie_list_length)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

    def download_progress(self, download_data):
        self.progress_bar.setValue(download_data["progress_value"])
        self.progress_bar.setFormat(download_data["movie_file"])


class MovieList(QListWidget):
    show_detail = Signal(object)
    client = MongoHelper()

    def __init__(self):
        super(MovieList, self).__init__()

        self.movie_downloader = DownloaderWorker()

        self.setItemDelegate(MovieListDelegate())
        self.setSpacing(5)

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setSelectionMode(QListWidget.ExtendedSelection)

        self.itemDoubleClicked.connect(self.show_details_action)

        self.movie_db_list = Movie.get_all_movies_from_db()
        self.refresh()

        self.movie_downloader.download_finished.connect(self.update_movie_list)

    def show_details_action(self, item):
        self.show_detail.emit(item.movie)

    def update_movie_list(self, movie_object):
        self.movie_db_list.append(movie_object)
        self.refresh()

    def create_movies(self, files):
        self.movie_db_list = []

        self.movie_downloader.set_file_list(files)
        self.movie_downloader.start()

    def refresh(self):
        self.clear()

        for movie_object in self.movie_db_list:
            MovieItem(self, movie_object)

class DownloaderWorker(QThread):
    download_finished = Signal(object)

    download_started = Signal(int)
    download_progress = Signal(dict)
    download_progress_finished = Signal(bool)

    def __init__(self):
        super(DownloaderWorker, self).__init__()

        self.file_list = []

    def set_file_list(self, file_list):
        self.file_list = file_list

    def run(self):
        self.download_started.emit(len(self.file_list))

        for index, file in enumerate(self.file_list):
            self.download_progress.emit({"progress_value": index, "movie_file":f"Downloading data for: {os.path.basename(file)}..."})

            movie_object = Movie(movie_path=file, client=MovieList.client)
            self.download_finished.emit(movie_object)

        self.download_progress_finished.emit(False)


class MovieListDelegate(QItemDelegate):
    def __init__(self):
        super(MovieListDelegate, self).__init__()

        self.outline_pen = QPen(QColor("#444444"))
        self.background_brush = QBrush(QColor("black"))
        self.selected_brush = QBrush(QColor(76, 228, 239, 80))
        self.mouse_over_brush = QBrush(QColor("yellow"))
        self.poster_pixmap = QPixmap()
        # self.temp_poster = pixmap.scaled(MovieItem.poster_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paint(self, painter, option, index):
        rect = option.rect

        poster_file = index.data(Qt.UserRole)
        self.poster_pixmap.load(poster_file)
        poster_file_rescaled = self.poster_pixmap.scaled(MovieItem.poster_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        painter.setPen(self.outline_pen)
        painter.setBrush(self.background_brush)
        painter.drawRect(rect)

        # posters
        poster_rect = QRect(rect.x(), rect.y(), poster_file_rescaled.width(), poster_file_rescaled.height())
        poster_rect.moveCenter(rect.center())
        painter.drawPixmap(poster_rect, poster_file_rescaled)

        if option.state & QStyle.State_Selected:
            painter.setBrush(self.selected_brush)
            painter.drawRect(rect)

class MovieItem(QListWidgetItem):
    poster_size = QSize(200, 300)

    def __init__(self, parentWidget, movie_object):
        super(MovieItem, self).__init__(parentWidget)
        self.setSizeHint(self.poster_size)
        self.movie = movie_object

        self.setData(Qt.UserRole, movie_object.poster)

    def has_name(self, filter_string):
        item_filter_string = self.movie.title.lower()
        item_filter_string += f" {self.movie.release_date}"
        item_filter_string += f" {self.movie.rating}"

        if filter_string.lower() in item_filter_string:
            return True

        return False