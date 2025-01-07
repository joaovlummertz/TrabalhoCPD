from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

from btree import BTree

class CustomTableWidget:
    # The table can be sorted by a specific column and in ascending or descending order
    def __init__(self, table_widget, data, sort_by, ascending_order, combo_box, postings):
        self.table_widget = table_widget
        self.data = data
        self.sort_by = sort_by
        self.ascending_order = ascending_order
        self.combo_box = combo_box
        self.postings = postings

    def on_header_click(self, index):
        self.highlight_column(False)
        if index == self.sort_by:
            self.ascending_order = not self.ascending_order
        else:
            self.sort_by = index
        self.update_table()
        self.highlight_column(True)

    def create_b_tree(self):
        b_tree = BTree(2)

        postings = self.postings
        max_index = len(self.data)
        selected_year = None
        curr_text = self.combo_box.currentText()
        if curr_text and curr_text != "Todos":
            selected_year = int(curr_text) - 2010
            max_index = len(postings[selected_year][1])
        for i in range(max_index):
            data = self.data[i]
            index = i
            if curr_text and curr_text != "Todos":
                data = self.data[postings[selected_year][1][i]]
                index = postings[selected_year][1][i]

            if self.sort_by == 0:
                b_tree.insert(data.title, index)
            elif self.sort_by == 1:
                b_tree.insert(data.artist.name, index)
            elif self.sort_by == 2:
                b_tree.insert(data.total_streams, index)
            elif self.sort_by == 3:
                b_tree.insert(data.peak_daily, index)
            elif self.sort_by == 4:
                b_tree.insert(data.year, index)
            else:
                b_tree.insert(data.genre.name, index)
            print(data.year)

        display = []
        b_tree.display(display)
        return display

    def populate_table(self, display):
        for row, i in enumerate(display):
            self.table_widget.setItem(row, 0, QTableWidgetItem(self.data[i].title))
            self.table_widget.setItem(row, 1, QTableWidgetItem(self.data[i].artist.name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(self.data[i].total_streams)))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(self.data[i].peak_daily)))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(int(float(self.data[i].year))))) # Believe it or not, this casting is actually correct.
            self.table_widget.setItem(row, 5, QTableWidgetItem(self.data[i].genre.name))

    def create_table(self):
        display = self.create_b_tree()

        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(display))
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["Música", "Artista", "Total de repr.", "Rec. diário", "Ano", "Gênero"])

        self.combo_box.currentIndexChanged.connect(lambda index: self.update_table())

        self.combo_box.addItem("Todos")
        for i in range(2010, 2024):
            self.combo_box.addItem(str(i))

        self.combo_box.setCurrentIndex(0)

        header = self.table_widget.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(lambda index: self.on_header_click(index))
        header.setSectionResizeMode(QHeaderView.Stretch)

        if not self.ascending_order:
            display = reversed(display)

        self.populate_table(display)

    def update_table(self):
        display = self.create_b_tree()
        self.table_widget.setRowCount(len(display))
        if not self.ascending_order:
            display = reversed(display)
        self.populate_table(display)

    def highlight_column(self, highlight):
        item = self.table_widget.horizontalHeaderItem(self.sort_by)
        font = item.font()
        font.setBold(highlight)
        item.setFont(font)
