import sys
import pickle

from PyQt5.QtWidgets import QApplication, QMainWindow

from main_window import Ui_MainWindow
from postings import create_postings_files, read_postings_file
from table import CustomTableWidget

class Song:
    def __init__(self, title, artist, year, total_streams, peak_daily, genre):
        self.title = title
        self.artist = artist
        self.year = year
        self.total_streams = total_streams
        self.peak_daily = peak_daily
        self.genre = genre

    def __str__(self):
        return "Nome: " + self.title + " - Artista: " + self.artist.name + " - Ano: " + self.year

class Artist:
    def __init__(self, name, country, sex, total_streams, most_streamed_song, songs):
        self.name = name
        self.sex = sex
        self.total_streams = total_streams
        self.most_streamed_song = most_streamed_song
        self.songs = songs

        self.country = country
class Genre:
    def __init__(self, name, total_streams, most_streamed_song, most_streamed_artist):
        self.name = name
        self.total_streams = total_streams
        self.most_streamed_song = most_streamed_song
        self.most_streamed_artist = most_streamed_artist

def read_from_bin():
    with open("data.pkl", "rb") as bin_file:
        return pickle.load(bin_file)

def main():
    songs_read = read_from_bin()

    create_postings_files(songs_read)

    read_from_bin()
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    CustomTableWidget(ui.tableWidget, songs_read, 2, False, ui.comboBox, read_postings_file("years.pkl"), ui.lineEdit).create_table()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
