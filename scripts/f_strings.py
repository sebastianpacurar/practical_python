import locale


def thousands_separator():
    print('\nSeparator can be _ or , :')
    n = 10000000000  # thousands separator formatting
    print(f'{n:_}')
    print(f'{n:,}')


def spacer_insertion():
    print('\nAppend or Prepend any character except some symbols')
    c = 'test'  # c has 4 characters
    print(f':{c:_>12}:')  # insert 8 _ before c
    print(f':{c:>12}:')  # insert 8 space chars before c
    print(f':{c:-<12}:')  # insert 8 _ after c
    print(f':{c:0^12}:')  # insert 4 zeroes around c
    print(f':{c:^12}:')  # insert 4 space chars around c
    print(f':{c:~<12}:')  # insert 8 ~ after c


def mantissa_handler():
    print('\nFloating value formatting:')
    n = 1234.5678
    print(f'initial = {n}')
    print(f'{n:.2f} adds 2 vals')  # similar to round(n, 2)
    print(f'{n:,.1f} adds 1 val')  # combine with a thousand separator
    print(f'{n:.0f} trims all mantissa vals')  # similar to int(n)


def explicit_string_values():
    print('\nExplicit String Values')
    x = 7
    y = 5
    equation = x + y
    print(f'{x + y = }')
    print(f'{equation = }')


def number_base_formatting():
    n = 255
    print(f'\nNumber Base Formatting:')
    print(f'binary: {n:b}')
    print(f'octal: {n:o}')
    print(f'hexadecimal: {n:x}')
    print(f'hexadecimal (uppercase): {n:X}')


def padding_and_alignment():
    print('\nPadding and Alignment:')
    print('"align" example:')
    s = 'align'  # s has 5 characters
    print(f'{s:_<10}')  # left align with _
    print(f'{s:*>10}')  # right align with *
    print(f'{s:+^10}')  # center align with +

    print('\n"test" example:')
    c = 'test'  # c has 4 characters
    print(f':{c:_>12}:')  # insert 8 _ before c
    print(f':{c:>12}:')  # insert 8 space chars before c
    print(f':{c:-<12}:')  # insert 8 _ after c
    print(f':{c:0^12}:')  # insert 4 zeroes around c
    print(f':{c:^12}:')  # insert 4 space chars around c
    print(f':{c:~<12}:')  # insert 8 ~ after c

    print('\nNested example')
    width = 10
    fill_char = '*'
    s = 'nested'
    print(f'{s:{fill_char}^{width}}')
    print(f'{s:{fill_char}>{width}}')
    print(f'{s:{fill_char}<{width}}')

    print('\nCustom Formatting with str.format():')
    s = 'custom'
    print('custom: {:-^10}'.format(s))
    n = 42
    print('number: {:*^10}'.format(n))


def percentage_formatting():
    print('\nPercentage Formatting:')
    n = 0.75
    print(f'{n:.0%}')
    print(f'{n:.2%}')


def locale_sensitive_formatting():
    locale.setlocale(locale.LC_ALL, '')  # Use user's default locale settings
    n = 1234567.89
    print('\nLocale-Sensitive Formatting:')
    print(locale.format_string('%d', n, grouping=True))
    print(locale.format_string('%.2f', n, grouping=True))


if __name__ == '__main__':
    thousands_separator()
    spacer_insertion()
    mantissa_handler()
    explicit_string_values()
    number_base_formatting()
    padding_and_alignment()
    percentage_formatting()
    locale_sensitive_formatting()
