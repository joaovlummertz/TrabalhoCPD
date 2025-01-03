import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import main_window
from main_window import Ui_MainWindow

class Song:
    def __init__(self, title, artist, year, total_streams, peak_daily, genre):
        self.title = title
        self.artist = artist
        self.year = year
        self.total_streams = total_streams
        self.peak_daily = peak_daily
        self.genre = genre

class Artist:
    def __init__(self, name, country, sex, total_streams, most_streamed_song, songs):
        self.name = name
        self.country = country
        self.sex = sex
        self.total_streams = total_streams
        self.most_streamed_song = most_streamed_song
        self.songs = songs

class Genre:
    def __init__(self, name, total_streams, most_streamed_song, most_streamed_artist):
        self.name = name
        self.total_streams = total_streams
        self.most_streamed_song = most_streamed_song
        self.most_streamed_artist = most_streamed_artist

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()