from enum import Enum


class TextColor(Enum):
    @property
    def ansi_code(self):
        """generate the ANSI escape code for the text color represented by the enum value
        Returns:
            str: string containing the setup request and the applied color value, formatted
        Explanation:
            - "\033" initiates control sequences for controlling terminal behavior
            - "38;5;" indicates the use of the extended 256-color mode
            - {self.value} represents the enum value
        """
        return f'\033[38;5;{self.value}m'

    def color_text(self, text_content):
        """apply the text color represented by the enum value to the provided text content
        Args:
            text_content (str): the text content to which the color will be applied
        Returns:
            str: text content with applied color
        Explanation:
            - "\033": initiates control sequences for controlling terminal behavior
            - "[0m": resets text color to default
        """
        return f'{self.ansi_code}{text_content}\033[0m'


# tested on windows 11
# TODO: these might appear different on linux/mac
class ColorPalette(TextColor):
    BLACK = 0
    RED = 1
    LIGHT_RED = 9
    MAGENTA = 5
    LIGHT_MAGENTA = 13
    GREEN = 2
    LIGHT_SEA_GREEN = 78
    DARK_GREEN = 64
    YELLOW = 3
    LIGHT_YELLOW = 11
    GOLD = 220
    BLUE = 4
    LIGHT_BLUE = 12
    CORNFLOWER = 111
    CYAN = 6
    GRAY_30 = 239
    GRAY_40 = 241
    GRAY_50 = 243
    GRAY_60 = 245
    GRAY_70 = 247
    GRAY_80 = 249
    WHITE = 255


def display_colors():
    print('Text Colors:')
    for color in ColorPalette:
        print(color.color_text(color.name.replace('_', ' ').title()))


if __name__ == '__main__':
    display_colors()
