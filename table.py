from PyQt5.QtWidgets import QTableWidgetItem

from btree import BTree

class CustomTableWidget:
    # The table can be sorted by a specific column and in ascending or descending order
    def __init__(self, table_widget, data, sort_by, ascending_order):
        self.table_widget = table_widget
        self.data = data
        self.sort_by = sort_by
        self.ascending_order = ascending_order

    def on_header_click(self, index):
        if index == self.sort_by:
            self.ascending_order = not self.ascending_order
        else:
            self.sort_by = index
        self.update_table()

    def create_b_tree(self):
        b_tree = BTree(2)
        for i in range(len(self.data)):
            if self.sort_by == 0:
                b_tree.insert(self.data[i].title, i)
            elif self.sort_by == 1:
                b_tree.insert(self.data[i].artist.name, i)
            elif self.sort_by == 2:
                b_tree.insert(self.data[i].total_streams, i)
            elif self.sort_by == 3:
                b_tree.insert(self.data[i].peak_daily, i)
            elif self.sort_by == 4:
                b_tree.insert(self.data[i].year, i)
            else:
                b_tree.insert(self.data[i].genre.name, i)

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

        header = self.table_widget.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(lambda index: self.on_header_click(index))

        if not self.ascending_order:
            display = reversed(display)

        self.populate_table(display)

    def update_table(self):
        display = self.create_b_tree()
        if not self.ascending_order:
            display = reversed(display)
        self.populate_table(display)
