from tabulate import tabulate

from utils_global.ColorPalette import ColorPalette


class ConsoleTable:
    def __init__(self, data, headers, text_color=ColorPalette.GRAY_70):
        self._headers = headers
        self._text_color = text_color
        self._rows = tabulate(data, headers=self._headers, tablefmt='fancy_grid', stralign='center').split('\n')
        self.process_table()

    def process_table(self):
        header = self._rows[1]
        self._rows[1] = header.replace('=', '-')
        self._rows = [self._text_color.color_text(content) for content in self._rows]

    def display(self):
        print('\n'.join(self._rows))
