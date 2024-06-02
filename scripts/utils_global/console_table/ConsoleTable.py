from tabulate import tabulate

from utils_global.ColorPalette import ColorPalette
from utils_global.console_table.Layout import Layout


class ConsoleTable:
    def __init__(
            self,
            data: list[list],
            headers: list[str],
            text_color: ColorPalette = ColorPalette.GRAY_70,
            layout: Layout = Layout.FANCY_GRID,
            is_indexed: bool = False,
            str_align: str = 'center'
    ) -> None:
        self._data = data
        self._headers = headers
        self._text_color = text_color
        self._layout = layout
        self._is_indexed = is_indexed
        self._str_align = str_align
        self._rows = self.build_tabulate()

    def build_tabulate(self) -> list[str]:
        return tabulate(
            self._data,
            headers=self._headers,
            showindex=range(1, len(self._data) + 1) if self._is_indexed else 'never',
            tablefmt=self._layout.value,
            stralign=self._str_align
        ).split('\n')

    def process_table(self) -> None:
        header: str = self._rows[1]
        self._rows[1] = header.replace('=', '-')
        self._rows = [self._text_color.color_text(content) for content in self._rows]

    def display(self) -> None:
        self.process_table()
        print('\n'.join(self._rows))
