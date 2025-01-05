import sys
import pickle
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import Ui_MainWindow
import btree

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
    #aqui começa a fazer uma lista com três músicas, duas delas do mesmo artista
    list = []
    Kpop = Genre("Kpop", 0, None, None)
    NewJeans = Artist("New Jeans", "Korea", "Fem", 0, None, [])
    temp = Song("Right Now", NewJeans, 2024, 100, 10, Kpop)
    list.append(temp)
    temp = Song("Supernatural", NewJeans, 2024, 200, 15, Kpop)
    list.append(temp)
    TaylorSwift = Artist("Taylor Swift", "USA","Fem",  0, None, [])
    Pop = Genre("Pop", 0, None, None)
    temp = Song("Blank Space", TaylorSwift, 2014, 1500, 150, Pop)
    list.append(temp)

    #aqui começa a atualizar os espaços de música mais ouvida de cada artista e genero
    for song in list:
        if song.genre.most_streamed_song == None or song.genre.most_streamed_song.total_streams < song.total_streams:
            song.genre.most_streamed_song = song
            song.genre.most_streamed_artist = song.artist
        song.artist.songs.append(song)
        if song.artist.most_streamed_song ==  None or song.artist.most_streamed_song.total_streams < song.total_streams:
            song.artist.most_streamed_song = song
        song.artist.total_streams += song.total_streams

    for song in list:
        if song.genre.most_streamed_artist == None or song.genre.most_streamed_artist.total_streams < song.artist.total_streams:
            song.genre.most_streamed_artist = song.artist

    #incluindo novo item na lista
    Enhypen = Artist("Enhypen", "Korea", "Masc", 0, None, [])
    temp = Song("Daydream", Enhypen, 2024, 1000, 100, Kpop)
    list.append(temp)
    temp = Song("No doubt", Enhypen, 2024, 1050, 100, Kpop)
    list.append(temp)

    #tem que fazer todo o processo de novo
    for song in list:
        if song.genre.most_streamed_song == None or song.genre.most_streamed_song.total_streams < song.total_streams:
            song.genre.most_streamed_song = song
            song.genre.most_streamed_artist = song.artist
        song.artist.songs.append(song)
        if song.artist.most_streamed_song ==  None or song.artist.most_streamed_song.total_streams < song.total_streams:
            song.artist.most_streamed_song = song
        song.artist.total_streams += song.total_streams

    for song in list:
        if song.genre.most_streamed_artist == None or song.genre.most_streamed_artist.total_streams < song.artist.total_streams:
            song.genre.most_streamed_artist = song.artist

    #processo de ordenamento por streams usando b-tree
    Stream = btree.BTree(2)
    for indice in range(0, len(list)):
        Stream.insert(list[indice].total_streams, indice)

    list_t = []
    Stream.display(list_t)
    for indice in list_t:
        print(list[indice].title, list[indice].total_streams)





    #import csv_to_bin
    #csv_to_bin.convert()
    songs_read = read_from_bin()
    for song in songs_read:
        print(song)
    read_from_bin()
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()