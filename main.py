import sys
import pickle
from PyQt5.QtWidgets import QApplication, QMainWindow

import csv_to_bin
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

def insert_song(song_title, year, song_streams, song_peak, artist_name, genre_name):
    songs = read_from_bin()
    newartist = None
    newgenre = None
    genre_songs = []
    artist_songs = []
    #verifica se o artista e o gênero já estão na lista
    for song in songs:
        if artist_name == song.artist.name:
            song.artist.total_streams += song_streams
            newartist = song.artist
            artist_songs.append(song)
        if genre_name == song.genre.name:
            song.genre.total_streams += song_streams
            newgenre = song.genre
            genre_songs.append(song)

    #se não estão cria novo
    if newartist is None:
        newartist = Artist(artist_name, "Not informed", "Not informed", song_streams, None, [])
    if newgenre is None:
        newgenre = Genre(genre_name, song_streams, None, newartist)

    #cria música
    newartist.songs = artist_songs
    newsong = Song(song_title, newartist, year, song_streams, song_peak, newgenre)
    #atuliza as músicas do artista
    newsong.artist.songs.append(newsong)
    genre_songs.append(newsong)

    for song in genre_songs:
        if song.genre.most_streamed_song is not None and song.total_streams > song.genre.most_streamed_song.total_streams:
            song.genre.most_streamed_song = song.total_streams

    for song in newsong.artist.songs:
        if song.artist.most_streamed_song is not None and song.total_streams > song.artist.most_streamed_song.total_streams:
            song.artist.most_streamed_song = song.total_streams

    songs.append(newsong)

    with open("data.pkl", "wb") as bin_file:
        pickle.dump(songs, bin_file)


def main():
    csv_to_bin.convert()
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
