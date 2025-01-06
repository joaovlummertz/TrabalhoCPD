import sys
import pickle

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

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

def create_postings_file(songs_read):
    file = []
    years = []
    # coloca todos os anos disponíveis numa lista e os ordena
    for song in songs_read:
        if song.year not in years:
            years.append(song.year)
    years.sort()
    # coloca todos os índices das músicas na lista arquivo se tiverem o mesmo ano
    # a forma que é colocado é: (ano, músicas[])
    for year in years:
        templist = []
        for i in range(0, len(songs_read)):
            if songs_read[i].year == year:
                templist.append(i)
        file.append((year, templist))

    with open("years.pkl", "wb") as bin_file:
        pickle.dump(file, bin_file)

    return file

def main():
    songs_read = read_from_bin()

    #coisas do arquivo invertido
    file = create_postings_file(songs_read)
    #forma de ordenar e filtrar pelo ano ao mesmo tempo
    ordena = []
    tree = BTree(2)
    for i in range(0, len(file[-1][1])):
        tree.insert(songs_read[file[-1][1][i]].total_streams, file[-1][1][i])

    tree.display(ordena)

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
