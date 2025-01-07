import pickle
from collections import defaultdict


def create_postings_files(songs_read):
    years_file = []
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
        years_file.append((year, templist))

    artist_indices = defaultdict(list)
    for i, song in enumerate(songs_read):
        artist_indices[song.artist.name.lower()].append(i)

    with open("years.pkl", "wb") as bin_file:
        pickle.dump(years_file, bin_file)

    with open("artists.pkl", "wb") as bin_file:
        pickle.dump(artist_indices, bin_file)

def read_postings_file(file):
    with open(file, "rb") as bin_file:
        return pickle.load(bin_file)