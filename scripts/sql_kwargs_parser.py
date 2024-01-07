import sys
import re
import sqlite3
import pandas as pd
from PIL import Image
import io
from matplotlib import pyplot as plt
from enum import Enum

print(sys.version)

NC = sqlite3.connect('../data_sets/db/northwind.db')
SC = sqlite3.connect('../data_sets/db/sakila.db')
CC = sqlite3.connect('../data_sets/db/covid19.db')
allTables = 'SELECT name FROM sqlite_master WHERE type="table";'


def q(db, query, count=None):
    df = pd.read_sql_query(query, db)
    if count is None or count == 0:
        return df
    elif count < 0:
        return df.tail(abs(count))
    elif count > 0:
        return df.head(count)


class FilterCondition(Enum):
    CONTAINS = 'LIKE "%{}%"'
    STARTS_WITH = 'LIKE "{}%"'
    ENDS_WITH = 'LIKE "%{}"'


class AggregateFunctions(Enum):
    AVG = 'AVG({})'
    SUM = 'SUM({})'
    MAX = 'MAX({})'
    MIN = 'MIN({})'
    COUNT = 'COUNT({})'


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


def verify_between_agg(expression):
    is_valid = False
    res = None
    number_pattern = r'\b\d+\.\d+?\b'
    letter_pattern = r'[A-Za-z]+'

    numbers = re.findall(number_pattern, expression)
    letters = re.findall(letter_pattern, expression)

    if len(numbers) > 0 and len(letters) == 1:
        is_valid = True
        numbers_with_letters = numbers.copy()
        numbers_with_letters.insert(1, letters[0])
        res = numbers_with_letters

    return is_valid, res


# Grab info about one table
def table(db, name, **kwargs):
    """
    Retrieve data from a specified table with optional filtering and ordering.

    Parameters:
        :param db: (str): The name of the db to retrieve data from.
        :param name: (str): The name of the table to retrieve data from.
        **kwargs: (dict): Additional keyword arguments for customization.

    Keyword Arguments:
        :keyword cols (list of str, optional): A list of column names to select (default is all columns).
        :keyword contains: (list of str, optional): A list specifying columns and values for 'contains' filtering.
        :keyword starts_with: (list of str, optional): A list specifying columns and values for 'starts_with' filtering.
        :keyword ends_with: (list of str, optional): A list specifying columns and values for 'ends_with' filtering.
        :keyword distinct: (bool, optional): Whether to retrieve distinct rows (default is False).
        :keyword count: (bool, optional): Whether to include a count of items in the result (default is False).
        :keyword where: (list of str, optional): A list specifying filtering conditions, e.g., ['AND', 'ColumnName > 10'].
        :keyword order_by: (tuple of str and int, optional): A tuple specifying column and sorting direction (0 for ASC, 1 for DESC).
        :keyword limit: (int, optional): The maximum number of rows to return. works with negative/positive numbers
        :keyword offset: (int, optional): Set offset of limit.
    """
    filtered = False
    name = f'"{name}"' if len(name.split(' ')) > 1 else name
    distinct = 'DISTINCT ' if kwargs.get('distinct', False) else ''
    count = 'COUNT(*) AS items_count' if kwargs.get('count', False) else ''
    filter_conditions = [condition.name.lower() for condition in FilterCondition if condition.name.lower() in kwargs]
    t_cols = '*'

    # handle cols=[] kwarg
    if '*' not in kwargs.get('cols', ['*']):
        t_cols = format_cols_query(kwargs.get('cols'))

    query = f'SELECT {distinct}{t_cols}\nFROM {name} \n'

    # handle contains=[] / starts_with=[] / ends_with=[] kwargs
    if filter_conditions:
        filtered = True
        condition = filter_conditions[0]
        col, col_val = kwargs.get(condition)
        formatted_like = FilterCondition[condition.upper()].value.format(col_val)
        query += f'WHERE {col} {formatted_like} \n'

    # handle where=[] arg
    # TODO: fix for included AND (&) OR (|) operators in each condition (change whole logic)
    if 'where' in kwargs:
        choice, *options = kwargs.get('where', [])
        if get_list_or_zero(options) != 0:
            is_first_valid, first_cond = verify_between_agg(options[0])
            if is_first_valid:
                sql = f'{"WHERE" if not filtered else ""} {first_cond[1]} BETWEEN {first_cond[0]} AND {first_cond[2]}\n'
            else:
                sql = f'{choice.upper()} ' if filtered else 'WHERE '
            for condition in options[1:]:
                is_valid, cond = verify_between_agg(condition)
                if is_valid:
                    sql += f'{cond[1]} BETWEEN {cond[0]} AND {cond[2]}\n'
                else:
                    sql += f'\t{choice} {condition}\n'
            query += sql

    # handle order_by kwarg
    if 'order_by' in kwargs:
        col, direction = kwargs.get('order_by')
        query += f'ORDER BY {col} {"ASC" if direction >= 0 else "DESC"}\n'

    # handle limit kwarg
    if 'limit' in kwargs:
        lim = get_int_or_zero(kwargs.get('limit', '0'))
        if lim != 0:
            if 'order_by' not in kwargs and lim < 0:
                query += 'ORDER BY 1 DESC\n'
            query += f'LIMIT {abs(lim)}'

            if 'offset' in kwargs:
                off_val = get_int_or_zero(kwargs.get('offset', '0'))
                if off_val > 0:
                    query += f' OFFSET {off_val}'

    # handle count kwarg
    if count:
        query = f'SELECT {count} FROM ({query})'

    # return the query string if subq=True
    res = query if kwargs.get('subq', False) is True else pd.read_sql(query, db)
    print(f'\n{query}\n\n')

    return res


# Works only on NorthWind DB
def category_img(db, category_name):
    query = f'SELECT Picture FROM Categories WHERE CategoryName="{category_name}"'
    df = q(db, query)

    if not df.empty:
        image_data = df['Picture'].iloc[0]
        image = Image.open(io.BytesIO(image_data))
        plt.imshow(image)
        plt.title(category_name)
        plt.axis('off')
        plt.show()
    else:
        print(f"No image found for category: {category_name}")


# Works only on NorthWind DB
def categories_img(db, num_cols):
    query = 'SELECT CategoryName, Picture FROM Categories'
    df = q(db, query)

    if not df.empty:
        num_images = len(df)
        num_rows = (num_images + num_cols - 1) // num_cols

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
        plt.subplots_adjust(wspace=0.2, hspace=0.3)

        for idx, row in enumerate(df.itertuples()):
            category_name = row.CategoryName
            image_data = row.Picture

            if image_data is not None:
                image = Image.open(io.BytesIO(image_data))
                ax = axes[idx // num_cols, idx % num_cols]
                ax.imshow(image)
                ax.set_title(category_name)
                ax.axis('off')
            else:
                print(f"No image found for category: {category_name}")

        # Hide any empty subplots
        for i in range(len(df), num_rows * num_cols):
            fig.delaxes(axes[i // num_cols, i % num_cols])

        plt.show()
    else:
        print("No categories found.")


# for testing queries
if __name__ == '__main__':
    t = table(db=NC, name='Order Details',
              cols=['UnitPrice'], distinct=True,
              where=['AND', '20.0 >= UnitPrice <= 70.0'],
              order_by=['UnitPrice', -1],
              limit=5, offset=2)
    print(t)

    t = table(db=NC, name='Order Details',
              cols=['avg=UnitPrice:UP Avg',
                    'max=UnitPrice:UP Max',
                    'min=UnitPrice:UP Min',
                    'count=UnitPrice:UP Count'])
    print(t)

    t = table(db=SC, name='Country', limit=-3)
    print(t)

    t = table(db=CC, name='Cases', count=True, contains=['geoId', 'FR'])
    print(t)

    categories_img(db=NC, num_cols=3)
