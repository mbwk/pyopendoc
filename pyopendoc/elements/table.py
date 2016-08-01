from .element import IndexableElement, Element
import copy

class Cell(Element):
    def write(self, content):
        # See if we can grab an existing span element
        pass

class Row(IndexableElement):
    def _get_child_class(self):
        return Cell

    def _get_child_selector(self):
        return './table:table-cell'

class Table(IndexableElement):
    def _get_child_class(self):
        return Row

    def _get_child_selector(self):
        return './table:table-row'

    def clone_row(self, row_index, new_row_index):
        # Let it raise if doesn't exist
        row = self[row_index]
        new_row = copy.deepcopy(row)
        self.insert(new_row_index, new_row)
        return new_row
