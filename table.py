from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QPushButton, QLabel

from btree import BTree
from trietree import Trie

from postings import read_postings_file

class CustomTableWidget:
    # The table can be sorted by a specific column and in ascending or descending order
    def __init__(self, table_widget, data, sort_by, ascending_order, combo_box, years_postings, line_edit, pagination_layout):
        self.table_widget = table_widget
        self.data = data
        self.sort_by = sort_by
        self.ascending_order = ascending_order
        self.combo_box = combo_box
        self.years_postings = years_postings
        self.line_edit = line_edit
        self.pagination_layout = pagination_layout

        self.current_page = 0
        self.items_per_page = 50
        self.total_pages = 1

        self.prev_button = QPushButton("<")
        self.next_button = QPushButton(">")
        self.page_label = QLabel("Página 1 de 1")
        #self.page_label.setMinimumSize(300, 20)
        self.page_label.setAlignment(Qt.AlignCenter)

        self.create_pagination_controls()

    def create_pagination_controls(self):
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.next_button)

        self.update_pagination_controls(self.data)

    def update_pagination_controls(self, data):
        self.total_pages = (len(data) + self.items_per_page - 1) // self.items_per_page
        self.page_label.setText(f"Página {self.current_page + 1} de {self.total_pages}")
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table(self.line_edit.text())

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_table(self.line_edit.text())

    def on_header_click(self, index, search=None):
        self.highlight_column(False)
        if index == self.sort_by:
            self.ascending_order = not self.ascending_order
        else:
            self.sort_by = index
        self.update_table(search)
        self.highlight_column(True)

    def create_b_tree(self):
        b_tree = BTree(2)

        data = self.data

        postings = self.years_postings
        max_index = len(data)
        selected_year = None
        curr_text = self.combo_box.currentText()
        if curr_text and curr_text != "Todos":
            selected_year = int(curr_text) - 2010
            if (selected_year + 2010) == int(postings[selected_year][0]):
                max_index = len(postings[selected_year][1])
            else:
                for i in range(len(self.years_postings)):
                    if self.years_postings[i][0] == (selected_year + 2010):
                        max_index = len(postings[i][1])

        for i in range(max_index):
            obj = data[i]
            index = i
            if curr_text and curr_text != "Todos":
                obj = data[postings[selected_year][1][i]]
                index = postings[selected_year][1][i]

            if self.sort_by == 0:
                b_tree.insert(obj.title, index)
            elif self.sort_by == 1:
                b_tree.insert(obj.artist.name, index)
            elif self.sort_by == 2:
                b_tree.insert(obj.total_streams, index)
            elif self.sort_by == 3:
                b_tree.insert(obj.peak_daily, index)
            elif self.sort_by == 4:
                b_tree.insert(obj.year, index)
            else:
                b_tree.insert(obj.genre.name, index)

        display = []
        b_tree.display(display)
        return display

    def create_trie_tree(self, prefix):
        songs = Trie()
        artist = Trie()

        artists_postings = read_postings_file("artists.pkl")

        year = self.combo_box.currentText()
        if year and year != "Todos":
            year = int(year)

        for i in range(0, len(self.data)):
            obj = self.data[i]
            obj_year = int(float(obj.year))
            if not songs.search(obj.title.lower()) and (year == "Todos" or obj_year == year):
                songs.insert(obj.title.lower(), i)

        for song in self.data:
            if not artist.search(song.artist.name.lower()):
                indices_list = artists_postings[song.artist.name.lower()]
                artist.insert(song.artist.name.lower(), indices_list)

        display = []

        temp = []
        artist.allthatstartswith(prefix, temp)
        for art in range(0, len(temp)):
            for i in temp[art]:
                if int(float(self.data[i].year)) == year or year == "Todos":
                    display.append(i)

        songs.allthatstartswith(prefix, display)

        return display

    def populate_table(self, display):
        start_index = self.current_page * self.items_per_page
        end_index = min(start_index + self.items_per_page, len(display))
        paginated_display = display[start_index:end_index]

        self.table_widget.setRowCount(len(paginated_display))
        for row, i in enumerate(paginated_display):
            self.table_widget.setItem(row, 0, QTableWidgetItem(self.data[i].title))
            self.table_widget.setItem(row, 1, QTableWidgetItem(self.data[i].artist.name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(self.data[i].total_streams)))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(self.data[i].peak_daily)))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(int(float(self.data[i].year)))))
            self.table_widget.setItem(row, 5, QTableWidgetItem(self.data[i].genre.name))

        self.update_pagination_controls(display)

    def create_table(self):
        display = self.create_b_tree()

        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(display))
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["Música", "Artista", "Total de repr.", "Rec. diário", "Ano", "Gênero"])

        self.combo_box.currentIndexChanged.connect(lambda index: self.update_table(self.line_edit.text()))

        self.combo_box.addItem("Todos")
        for i in range(len(self.years_postings)):
            self.combo_box.addItem(str(int(float(self.years_postings[i][0]))))

        self.combo_box.setCurrentIndex(0)

        self.line_edit.textChanged.connect(lambda text: self.update_table(text))

        header = self.table_widget.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(lambda index: self.on_header_click(index, self.line_edit.text()))
        header.setSectionResizeMode(QHeaderView.Stretch)

        if not self.ascending_order:
            display = list(reversed(display))

        self.populate_table(display)

    def update_table(self, search=None):
        display = []
        if not search:
            display = self.create_b_tree()
        else:
            display = self.create_trie_tree(search.lower())
        self.table_widget.setRowCount(len(display))
        if not self.ascending_order:
            display = list(reversed(display))
        self.populate_table(display)

    def highlight_column(self, highlight):
        item = self.table_widget.horizontalHeaderItem(self.sort_by)
        font = item.font()
        font.setBold(highlight)
        item.setFont(font)
