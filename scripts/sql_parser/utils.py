import re
from enums import AggregateFunctions


def get_int_or_zero(x):
    try:
        return int(x)
    except (ValueError, TypeError):
        return 0


def get_list_or_zero(x):
    return x if isinstance(x, list) and len(x) > 0 else 0


def str_val(x):
    words = len(x.split(' '))
    return f'"{x}"' if words > 1 else x


def and_or_operator(x):
    if x.startswith('&'):
        return 'AND'
    elif x.startswith('|'):
        return 'OR'
    else:
        raise ValueError(f'Issue with {x}, and {x[0]}')


def format_cols_query(cols):
    form_cols = []
    for col in cols:
        if '=' in col and ':' in col:
            agg, col_name, col_alias = re.split(r'[:=]', col)
            col_name = str_val(col_name)
            agg_func = AggregateFunctions[agg.upper()].value.format(col_name)
            form_cols.append(f'{agg_func} AS "{col_alias}"')
        elif '=' in col:
            agg, col_name = col.split('=')
            col_name = str_val(col_name)
            agg_func = AggregateFunctions[agg.upper()].value.format(col_name)
            form_cols.append(f'{agg_func}')
        elif ':' in col:
            col_name, col_alias = col.split(':')
            col_name = str_val(col_name)
            form_cols.append(f'{col_name} AS "{col_alias}"')
        else:
            col = str_val(col)
            form_cols.append(f'{col}')

    return ',\n\t'.join(form_cols)


def get_between_agg(expression):
    is_valid = False
    res = None

    number_pattern = r'\b\d+(?:\.\d+)?\b'
    letter_pattern = r'[A-Za-z_]+'

    numbers = re.findall(number_pattern, expression)
    letters = re.findall(letter_pattern, expression)

    if len(numbers) > 0 and len(letters) == 1:
        numbers_with_letters = numbers.copy()
        numbers_with_letters.insert(1, letters[0])

        if len(numbers_with_letters) > 2:
            is_valid = True
            res = numbers_with_letters

    return is_valid, res
