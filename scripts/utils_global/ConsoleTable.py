from tabulate import tabulate

from utils_global.ColorPalette import ColorPalette


class ConsoleTable:
    def __init__(self,
                 data: list[list],
                 headers: list[str],
                 text_color: ColorPalette = ColorPalette.GRAY_70
                 ) -> None:
        self._headers: list[str] = headers
        self._text_color: ColorPalette = text_color
        self._rows: list[str] = tabulate(data, headers=self._headers, tablefmt='fancy_grid', stralign='center').split('\n')
        self.process_table()

    def process_table(self) -> None:
        header: str = self._rows[1]
        self._rows[1] = header.replace('=', '-')
        self._rows = [self._text_color.color_text(content) for content in self._rows]

    def display(self) -> None:
        print('\n'.join(self._rows))
