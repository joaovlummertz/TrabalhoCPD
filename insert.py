import pickle

from PyQt5.QtWidgets import QMainWindow, QDialog

from input_window import Ui_Dialog


class Insert:
    def __init__(self, dialog_button):
        self.dialog_button = dialog_button
        self.window = QDialog()
        self.dialog_widget = Ui_Dialog()
        self.dialog_widget.setupUi(self.window)

    def setup_dialog(self):
        self.dialog_button.clicked.connect(lambda : self.window.exec_())
        self.window.accepted.connect(self.insert)

    def insert(self):
        title = self.dialog_widget.input_title.text()
        artist = self.dialog_widget.input_artist.text()
        streams = int(self.dialog_widget.input_streams.text())
        daily = int(self.dialog_widget.input_daily.text())
        year = str(float(self.dialog_widget.input_year.text()))
        genre = self.dialog_widget.input_genre.text()
        persist_song(title, year, streams, daily, artist, genre)

def persist_song(song_title, year, song_streams, song_peak, artist_name, genre_name):
    from main import read_from_bin, Song, Artist, Genre
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