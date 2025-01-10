def update_stats_tab(ui, songs):
    ui.lb_mst_lstnd_art.setText(most_listened_artist(songs).name)
    ui.lb_lst_lstnd_art.setText(least_listened_artist(songs).name)
    ui.lb_mst_lsnd_gnr.setText(most_listened_genre(songs).name)
    ui.lb_lst_lsnd_gnr.setText(least_listened_genre(songs).name)
    ui.lb_avg_streams.setText(str(media_streams(songs)))
    ui.lb_median_streams.setText(str(mediana_streams(songs)))

def most_listened_artist(songs):
    artists = []
    for song in songs:
        if song.artist not in artists:
            artists.append(song.artist)
    most_streams = 0
    most_listened = 0
    for artist in artists:
        if artist.total_streams > most_streams:
            most_streams = artist.total_streams
            most_listened = artist
    return most_listened

def least_listened_artist(songs):
    artists = []
    for song in songs:
        if song.artist not in artists:
            artists.append(song.artist)

    least_streams = artists[0].total_streams
    least_listened = artists[0]
    for artist in artists:
        if artist.total_streams < least_streams:
            least_streams = artist.total_streams
            least_listened = artist

    return least_listened

def most_listened_genre(songs):
    genres = []
    for song in songs:
        if song.genre and song.genre.name != "" and song.genre not in genres and song.genre.name != "Other":
            genres.append(song.genre)
    most_streams = 0
    most_streamed = None
    for genre in genres:
        if genre.total_streams > most_streams:
            most_streams = genre.total_streams
            most_streamed = genre

    return most_streamed

def least_listened_genre(songs):
    genres = []
    for song in songs:
        if song.genre.name != "" and song.genre not in genres and song.genre.name != "Other":
            genres.append(song.genre)
    least_streams = genres[0].total_streams
    least_streamed = genres[0]
    for genre in genres:
        if genre.total_streams < least_streams:
            least_streams = genre.total_streams
            least_streamed = genre

    return least_streamed

def media_streams(songs) -> int:
    soma = 0
    for song in songs:
        soma += song.total_streams

    media = soma / len(songs)
    return media

def mediana_streams(songs) -> int:
    if len(songs) % 2 == 0:
        soma = songs[len(songs) // 2].total_streams + songs[len(songs) // 2 + 1].total_streams
        mediana = soma / 2
    else:
        mediana = songs[len(songs) // 2].total_streams

    return mediana

def media_daily(songs) -> int:
    soma = 0
    for song in songs:
        soma += song.peak_daily

    media = soma / len(songs)
    return media

def mediana_daily(songs) -> int:
    if len(songs) % 2 == 0:
        soma = songs[len(songs) // 2].peak_daily + songs[len(songs) // 2 + 1].peak_daily
        mediana = soma / 2
    else:
        mediana = songs[len(songs) // 2].peak_daily

    return mediana


def songs(songs) -> int:
    return len(songs)

def num_artists(songs) -> int:
    artists = []
    for song in songs:
        if song.artist not in artists:
            artists.append(song.artist)

    return len(artists)

def num_genres(songs) -> int:
    genres = []
    for song in songs:
        if song.genre not in genres:
            genres.append(song.genre)

    return len(genres)
