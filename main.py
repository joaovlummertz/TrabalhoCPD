import sys
import pickle
from PyQt5.QtWidgets import QApplication, QMainWindow

import csv_to_bin
from input_window import Ui_Dialog
from insert import Insert
from main_window import Ui_MainWindow
from postings import create_postings_files, read_postings_file
from table import CustomTableWidget
from stats import update_stats_tab

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
    songs = []
    with open("data.pkl", "rb") as bin_file:
        songs = pickle.load(bin_file)

    for song in songs:
        if song.artist.songs is None:
            song.artist.songs = []

        if song.genre.most_streamed_song is None or song.genre.most_streamed_song.total_streams < song.total_streams:
            song.genre.most_streamed_song = song
            song.genre.most_streamed_artist = song.artist
        song.artist.songs.append(song)
        if song.artist.most_streamed_song is None or song.artist.most_streamed_song.total_streams < song.total_streams:
            song.artist.most_streamed_song = song
        song.artist.total_streams += song.total_streams

    for song in songs:
        song.genre.total_streams = song.total_streams
        if song.genre.most_streamed_artist is None or song.genre.most_streamed_artist.total_streams < song.artist.total_streams:
            song.genre.most_streamed_artist = song.artist

    return songs

def main():
    #csv_to_bin.convert()
    songs_read = read_from_bin()

    create_postings_files(songs_read)

    read_from_bin()
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    table = CustomTableWidget(ui.tableWidget, songs_read, 2, False, ui.comboBox, read_postings_file("years.pkl"), ui.lineEdit, ui.horizontalLayout)
    table.create_table()
    Insert(ui.insert_button, table, ui).setup_dialog()

    update_stats_tab(ui, songs_read)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
