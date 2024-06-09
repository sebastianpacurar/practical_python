from tabulate import tabulate

from scripts.utils_global.ColorPalette import ColorPalette
from scripts.utils_global.console_table.Layout import Layout


class ConsoleTable:
    def __init__(
            self,
            data: list[list],
            headers: list[str],
            title: str | None = None,
            text_color: ColorPalette = ColorPalette.GRAY_70,
            layout: Layout = Layout.FANCY_GRID,
            is_indexed: bool = False,
            clear_empty_cols: bool = False,
            str_align: str = 'center'
    ) -> None:
        self._data = data
        self._headers = headers
        self._text_color = text_color
        self._clear_empty_cols = clear_empty_cols
        self._layout = layout
        self._is_indexed = is_indexed
        self._str_align = str_align
        self._title = title
        self._rows = self.build_tabulate()

    def build_tabulate(self) -> list[str]:
        if self._clear_empty_cols:
            self.clear_empty_columns()
        return tabulate(
            self._data,
            headers=self._headers,
            showindex=range(1, len(self._data) + 1) if self._is_indexed else 'never',
            tablefmt=self._layout.value,
            stralign=self._str_align,
            numalign=self._str_align
        ).split('\n')

    def display(self) -> None:
        """ 1) display table title if there is one
            2) apply color to the rows
            3) display table in console
        """
        if self._title is not None:
            print(f'\n{self._title}')
        self._rows = [self._text_color.color_text(content) for content in self._rows]
        print('\n'.join(self._rows))

    def clear_empty_columns(self):
        """ 1) create a set which contains the indexes of the headers
            2) identify columns which have all table data values equal to '-' and save their index to the set
            2) delete the matching columns from headers and data
        """
        columns_to_remove = set(range(len(self._headers)))
        for row in self._data:
            columns_to_remove.intersection_update(
                {i for i, val in enumerate(row) if val == '-'}
            )
        for col in sorted(columns_to_remove, reverse=True):
            del self._headers[col]
            for row in self._data:
                del row[col]
