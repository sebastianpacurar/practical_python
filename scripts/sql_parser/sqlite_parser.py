import io
import sqlite3
from typing import Optional, List, Tuple
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image

from utils import *
from enums import FilterCondition

ALL_TABLES = 'SELECT name FROM sqlite_master WHERE type="table";'


class SqlParser:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def exec_query(self, query: str) -> pd.DataFrame:
        return pd.read_sql_query(query, self.conn)

    def q(self, query: str, count: int = None) -> pd.DataFrame:
        df = self.exec_query(query)
        if count is None or count == 0:
            return df
        elif count < 0:
            return df.tail(abs(count))
        elif count > 0:
            return df.head(count)

    def table(
            self,
            name: str,
            cols: [List[str]] = '*',
            contains: Optional[Tuple[str, str]] = None,
            starts_with: Optional[Tuple[str, str]] = None,
            ends_with: Optional[Tuple[str, str]] = None,
            distinct: bool = False,
            count: bool = False,
            where: Optional[List[str]] = None,
            order_by: Optional[Tuple[str, int]] = None,
            limit: int = 0,
            offset: int = 0,
            subq: bool = False,
    ) -> pd.DataFrame:
        name = f'"{name}"' if len(name.split(' ')) > 1 else name
        distinct = 'DISTINCT ' if distinct else ''
        count = 'COUNT(*) AS items_count' if count else ''
        t_cols = '*'

        # handle cols=[] kwarg
        if cols is not None and '*' not in cols:
            t_cols = format_cols_query(cols)

        query = f'SELECT {distinct}{t_cols}\nFROM {name} \n'

        # handle contains=[] / starts_with=[] / ends_with=[] kwargs
        if contains or starts_with or ends_with:
            cond = 'contains' if contains else 'starts_with' if starts_with else 'ends_with'
            col, col_val = contains if contains else starts_with if starts_with else ends_with
            formatted_like = FilterCondition[cond.upper()].value.format(col_val)
            query += f'WHERE {col} {formatted_like}\n'

        # handle where=[] arg
        if where:
            if get_list_or_zero(where):
                for i, cond in enumerate(where):
                    or_and_choice = and_or_operator(cond)
                    if "WHERE" not in query:
                        start = "WHERE"
                    else:
                        start = f'\t{or_and_choice}' if i > 0 else f'\t{or_and_choice}'
                    is_between_agg, agg_vals = get_between_agg(cond[1:])
                    if is_between_agg:
                        low, col, high = agg_vals
                        query += f'{start} {AggregateFunctions.BETWEEN.value.format(col, low, high)}\n'
                    else:
                        query += f'{start} {cond[1:]}\n'

        # handle order_by kwarg
        if order_by:
            col, direction = order_by
            query += f'ORDER BY {col} {"ASC" if int(direction) >= 0 else "DESC"}\n'

        # handle limit kwarg
        if limit:
            lim = get_int_or_zero(limit)
            if lim != 0:
                if not order_by and lim < 0:
                    query += 'ORDER BY 1 DESC\n'
                query += f'LIMIT {abs(lim)}'

                if offset:
                    off_val = get_int_or_zero(offset)
                    if off_val > 0:
                        query += f' OFFSET {off_val}'

        # handle count kwarg
        if count:
            query = f'SELECT {count} FROM ({query})'

        # return the query string if subq=True
        res = query if subq is True else self.exec_query(query)
        print(f'\n{query}\n')

        return res

    def category_img(self, category_name: str) -> None:
        query = f'SELECT Picture FROM Categories WHERE CategoryName="{category_name}"'
        df = self.q(query)

        if not df.empty:
            image_data = df['Picture'].iloc[0]
            image = Image.open(io.BytesIO(image_data))
            plt.imshow(image)
            plt.title(category_name)
            plt.axis('off')
            plt.show()
        else:
            print(f"No image found for category: {category_name}")

    def categories_img(self, num_cols: int) -> None:
        query = 'SELECT CategoryName, Picture FROM Categories'
        df = self.q(query)

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

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    NC_PATH = '../../data_sets/db/northwind.db'
    SC_PATH = '../../data_sets/db/sakila.db'
    CC_PATH = '../../data_sets/db/covid19.db'

    nc, sc, cc = SqlParser(NC_PATH), SqlParser(SC_PATH), SqlParser(CC_PATH)
    nct, sct, cct = nc.table, sc.table, cc.table

    # print(nct(name='Order Details',
    #           cols=['UnitPrice'], distinct=True,
    #           where=['&20.0 >= UnitPrice <= 70.0', '|UnitPrice > 20'],
    #           order_by=('UnitPrice', -1),
    #           limit=5, offset=2))
    #
    # print(nct(name='Order Details', cols=['UnitPrice'], distinct=True, where=['&20.0 >= UnitPrice <= 70.0'],
    #           order_by=('UnitPrice', -1), limit=5, offset=2))
    #
    # print(nct(name='Order Details',
    #           cols=['avg=UnitPrice:UP Avg',
    #                 'max=UnitPrice:UP Max',
    #                 'min=UnitPrice:UP Min',
    #                 'count=UnitPrice:UP Count']))

    print(sct(name='Country', limit=-3))

    # print(cct(name='Cases', count=True, contains=('geoId', 'FR')))
    #
    # nc.categories_img(num_cols=3)
