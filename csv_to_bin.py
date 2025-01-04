import csv
import pickle
from main import Song, Artist, Genre

def convert():
    songs = []
    artists = {}
    genres = {}

    with open("data.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for line in reader:
            artist_name, song_name = line["Artist and Title"].split(" - ", 1)
            if artist_name not in artists:
                artist = Artist(artist_name, None, None, 0, None, None)
                artists[artist_name] = artist

            genre_name = line["main_genre"]
            if genre_name not in genres:
                genre = Genre(genre_name, 0, None, None)
                genres[genre_name] = genre

            year = line["year"]
            total_streams = int(line["Streams"])
            peak_daily = int(line["Daily"])
            song = Song(song_name, artists[artist_name], year, total_streams, peak_daily, genres[genre_name])
            songs.append(song)

    for song in songs:
        artist = song.artist

        if artist.most_streamed_song is None or song.total_streams > artist.most_streamed_song.total_streams:
            artist.most_streamed_song = song

        artist.total_streams += song.total_streams

        genre = song.genre
        if genre.most_streamed_song is None or song.total_streams > genre.most_streamed_song.total_streams:
            genre.most_streamed_song = song

    for song in songs:
        artist = song.artist
        genre = song.genre

        if genre.most_streamed_artist is None or genre.most_streamed_artist.total_streams < artist.total_streams:
            genre.most_streamed_artist = artist

    with open("data.pkl", "wb") as bin_file:
        pickle.dump(songs, bin_file)
