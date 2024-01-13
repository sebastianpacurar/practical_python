import re
from typing import Optional, Dict, List

from enums import SqlFunctions


def get_int_or_zero(x):
    try:
        return int(x)
    except (ValueError, TypeError):
        return 0


def get_list_or_zero(x):
    return x if isinstance(x, list) and len(x) > 0 else 0


def str_val(*args):
    if len(args) == 1:
        return args[0] if args[0].isalpha() else f'"{args[0]}"'
    else:
        return tuple(x if x.isalpha() else f'"{x}"' for x in args)


def and_or_operator(x):
    if x.startswith('&'):
        return 'AND'
    elif x.startswith('|'):
        return 'OR'
    else:
        raise ValueError(f'Issue with {x}, and {x[0]}')


# apply aggregation and alias to column name. eg: "count=UnitPrice:UP" translated to: COUNT(UnitPrice) AS UP
def format_cols_query(cols):
    form_cols = []
    for col in cols:
        if '=' in col and ':' in col:
            agg, col_name, col_alias = re.split(r'[:=]', col)
            col_name, col_alias = str_val(col_name, col_alias)
            agg_func = SqlFunctions[agg.upper()].value.format(col_name)
            form_cols.append(f'{agg_func} AS {col_alias}')
        elif '=' in col:
            agg, col_name = col.split('=')
            col_name = str_val(col_name)
            agg_func = SqlFunctions[agg.upper()].value.format(col_name)
            form_cols.append(f'{agg_func}')
        elif ':' in col:
            split = col.split(':')
            col_name, col_alias = split[0], str_val(split[1].strip())
            form_cols.append(f'{col_name} AS {col_alias}')
        else:
            col = str_val(col)
            form_cols.append(f'{col}')

    return form_cols


# parse tables in dictionaries, in a list. parse all displayed columns in a single list
def process_multi_table_join(tables):
    tables_data = []
    formatted_cols = []

    for i, t in enumerate(tables):
        t_data = {}
        name, shared_col = t['name'], str_val(t['shared'])
        t_title = name
        t_name = name
        table_alias = None

        #  split table name into name and alias, if ':' is present
        if ':' in name:
            t_title = name.replace(':', ' ')
            elements = name.split(':')
            t_name, table_alias = str_val(elements[0]), elements[1]

        # format the target columns (these are the ones between SELECT and FROM
        #  use table alias where necessary
        if 'cols' in t:
            cols = format_cols_query(t['cols'])
            for col in cols:
                formatted_cols.append(f'\n\t{table_alias if table_alias is not None else name}.{col}')
        else:
            formatted_cols.append(f'\n\t{table_alias if table_alias is not None else str_val(name)}.*')

        t_data.update({'name': t_name, 'title': t_title, 'shared': shared_col})
        if table_alias is not None:
            t_data.update({'alias': table_alias})
        if 'join' in t:
            t_data.update({'join': t.get('join')})

        tables_data.append(t_data)

    # add "" (quotation marks) to 2 word based title names
    for t in tables_data:
        group = t.get('title').split(' ')
        if len(group) > 2:

            for g in group[:-2]:
                t['title'] = f'"{g} '
            t['title'] += f'{group[-2]}" '
            t['title'] += group[-1]

    return tables_data, formatted_cols


def process_two_table_join(table_format):
    # if is_group, then query contains named columns to display
    is_group = isinstance(table_format, tuple)
    full_name = table_format[0] if is_group else table_format
    t_title = full_name
    formatted_cols = []
    t_alias = None

    # perform naming operations and set table alias
    if ':' in full_name:
        t_title = full_name.replace(':', ' ')
        t_name, t_alias = full_name.split(':')

    t_name = t_alias if t_alias is not None else full_name
    cols = format_cols_query(table_format[1])
    for item in cols:
        formatted_cols.append(f'\n\t{t_alias if t_alias is not None else full_name}.{item if is_group else "*"}')

    tables_data = {'name': t_name, 'title': t_title}

    return tables_data, formatted_cols


def format_join_type(join_type):
    joins = {
        'i': 'INNER',
        'l': 'LEFT',
        'r': 'RIGHT',
        'f': 'FULL',
        'c': 'CROSS'
    }

    return joins.get(join_type.lower(), 'INNER')


# check if string is BETWEEN aggregation. eg: "10<UnitPrice<20" translated to: UnitPrice BETWEEN 10 AND 20
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


# format a table for multi_join readability
def get_table(
        name: str,
        shared: str,
        cols: Optional[List[str]] = None,
        join: Optional[str] = None
) -> Dict[str, str]:
    res = {'name': name, 'shared': shared, 'cols': cols}
    if join is not None:
        res.update({'join': join})
    return res
