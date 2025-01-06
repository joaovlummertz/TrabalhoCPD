import sys
import pickle

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from btree import BTree
from main_window import Ui_MainWindow
from table import CustomTableWidget
from btree import BTree
import trietree

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
    # list = []
    # Kpop = Genre("Kpop", 0, None, None)
    # NewJeans = Artist("New Jeans", "Korea", "Fem", 0, None, [])
    # temp = Song("Right Now", NewJeans, 2024, 100, 10, Kpop)
    # list.append(temp)
    # temp = Song("Supernatural", NewJeans, 2024, 200, 15, Kpop)
    # list.append(temp)
    # TaylorSwift = Artist("Taylor Swift", "USA","Fem",  0, None, [])
    # Pop = Genre("Pop", 0, None, None)
    # temp = Song("Blank Space", TaylorSwift, 2014, 1500, 150, Pop)
    # list.append(temp)
    #
    # #aqui começa a atualizar os espaços de música mais ouvida de cada artista e genero
    # for song in list:
    #     if song.genre.most_streamed_song == None or song.genre.most_streamed_song.total_streams < song.total_streams:
    #         song.genre.most_streamed_song = song
    #         song.genre.most_streamed_artist = song.artist
    #     song.artist.songs.append(song)
    #     if song.artist.most_streamed_song ==  None or song.artist.most_streamed_song.total_streams < song.total_streams:
    #         song.artist.most_streamed_song = song
    #     song.artist.total_streams += song.total_streams
    #
    # for song in list:
    #     if song.genre.most_streamed_artist == None or song.genre.most_streamed_artist.total_streams < song.artist.total_streams:
    #         song.genre.most_streamed_artist = song.artist
    #
    # #incluindo novo item na lista
    # Enhypen = Artist("Enhypen", "Korea", "Masc", 0, None, [])
    # temp = Song("Daydream", Enhypen, 2024, 1000, 100, Kpop)
    # list.append(temp)
    # temp = Song("No doubt", Enhypen, 2024, 1050, 100, Kpop)
    # list.append(temp)
    #
    # #tem que fazer todo o processo de novo
    # for song in list:
    #     if song.genre.most_streamed_song == None or song.genre.most_streamed_song.total_streams < song.total_streams:
    #         song.genre.most_streamed_song = song
    #         song.genre.most_streamed_artist = song.artist
    #     song.artist.songs.append(song)
    #     if song.artist.most_streamed_song ==  None or song.artist.most_streamed_song.total_streams < song.total_streams:
    #         song.artist.most_streamed_song = song
    #     song.artist.total_streams += song.total_streams
    #
    # for song in list:
    #     if song.genre.most_streamed_artist == None or song.genre.most_streamed_artist.total_streams < song.artist.total_streams:
    #         song.genre.most_streamed_artist = song.artist
    #
    # #processo de ordenamento por streams usando b-tree
    # Stream = btree.BTree(2)
    # for indice in range(0, len(list)):
    #     Stream.insert(list[indice].total_streams, indice)
    #
    # list_t = []
    # Stream.display(list_t)
    # for indice in list_t:
    #     print(list[indice].title, list[indice].total_streams)


    #import csv_to_bin
    #csv_to_bin.convert()
    songs_read = read_from_bin()
    b_tree = BTree(2)
    for i in range(len(songs_read)):
        b_tree.insert(songs_read[i].total_streams, i)

    display = []
    b_tree.display(display)

    #coisas do arquivo invertido
    arquivo = []
    years = []
    #coloca todos os anos disponíveis numa lista e os ordena
    for song in songs_read:
        if song.year not in years:
            years.append(song.year)
    years.sort()
    #coloca todos os índices das músicas na lista arquivo se tiverem o mesmo ano
    #a forma que é colocado é: (ano, músicas[])
    for year in years:
        templist = []
        for i in range(0, len(songs_read)):
            if songs_read[i].year == year:
                templist.append(i)
        arquivo.append((year, templist))

    with open("years.pkl", "wb") as bin_file:
        pickle.dump(arquivo, bin_file)


    #forma de ordenar e filtrar pelo ano ao mesmo tempo
    ordena = []
    arvore = BTree(2)
    for i in range(0, len(arquivo[-1][1])):
        arvore.insert(songs_read[arquivo[-1][1][i]].total_streams, arquivo[-1][1][i])

    arvore.display(ordena)

    ordena.reverse()
    #for indice in ordena:
     #   print(songs_read[indice], songs_read[indice].total_streams)

    # uso da trie para pesquisar músicas
    trie = trietree.Trie()
    for i in range(0, len(songs_read)):
        if not trie.search(songs_read[i].title):
            trie.insert(songs_read[i].title, i)


    trie_list = []
    trie.allthatstartswith("Blank", trie_list)
    #for i in trie_list:
      #  print(songs_read[i])

    #uso da trie para pesquisar artistas
    trie2 = trietree.Trie()

    for song in songs_read:
        if not trie.search(song.artist.name):
            indices_list = []
            #procura o índice de todas as músicas do artista
            for i in range(0, len(songs_read)):
                if songs_read[i].artist.name == song.artist.name:
                    indices_list.append(i)
            #insere a lista com os indices na trie junto com o nome do artista
            trie2.insert(song.artist.name, indices_list)

    trie2_list = []
    trie2.allthatstartswith("Imagine Dragons", trie2_list)
    for artist in range(0, len(trie2_list)):
        for i in trie2_list[artist]:
            print(songs_read[i])

    read_from_bin()
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    CustomTableWidget(ui.tableWidget, songs_read, 2, False).create_table()

    window.show()
    sys.exit(app.exec_())




if __name__ == "__main__":
    main()
