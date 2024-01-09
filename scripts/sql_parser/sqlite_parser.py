import io
import sqlite3
from typing import Optional, List, Tuple, Union
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image

from scripts.sql_parser.table_operations import *
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
            cols: Optional[List[str]] = '*',
            contains: Optional[Tuple[str, Union[str, int, float]]] = None,
            starts_with: Optional[Tuple[str, Union[str, int, float]]] = None,
            ends_with: Optional[Tuple[str, Union[str, int, float]]] = None,
            distinct: Optional[bool] = False,
            count: Optional[bool] = False,
            where: Optional[List[str]] = None,
            order_by: Optional[Tuple[str, int]] = None,
            limit: Optional[int] = 0,
            offset: Optional[int] = 0,
            subq: Optional[bool] = False
    ) -> Union[pd.DataFrame, str]:
        name = str_val(name)
        distinct = get_distinct_sql(distinct)
        count = 'COUNT(*) AS items_count' if count else ''  # TODO: change or remove!
        t_cols = '*'

        # handle cols=[] kwarg
        if cols is not None and '*' not in cols:
            t_cols = format_cols_query(cols)

        query = f'SELECT {distinct}{t_cols}\nFROM {name} \n'

        query += get_like_sql(contains, starts_with, ends_with)
        query += get_where_sql(query, where)
        query += get_order_by_sql(order_by)
        query += get_limit_sql(limit, offset, order_by)

        # handle count kwarg
        if count:
            query = f'SELECT {count} FROM ({query})'

        # return the query string if subq=True
        res = query if subq is True else self.exec_query(query)
        print(f'\n{query}\n')

        return res

    def join(
            self,
            table_left: Tuple[str, List[str]],
            table_right: Union[str, Tuple[str, List[str]]],
            shared_col: str,
            j_type: Optional[str] = 'i',
            contains: Optional[Tuple[str, Union[str, int, float]]] = None,
            starts_with: Optional[Tuple[str, Union[str, int, float]]] = None,
            ends_with: Optional[Tuple[str, Union[str, int, float]]] = None,
            distinct: Optional[bool] = False,
            where: Optional[List[str]] = None,
            order_by: Optional[Tuple[str, int]] = None,
            limit: Optional[int] = 0,
            subq: Optional[bool] = False
    ) -> Union[pd.DataFrame, str]:
        distinct = get_distinct_sql(distinct)

        query = get_join_sql(table_left, table_right, distinct, j_type, shared_col)
        query += get_like_sql(contains, starts_with, ends_with)
        query += get_where_sql(query, where)
        query += get_order_by_sql(order_by)
        query += get_limit_sql(limit, None, None)

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


if __name__ == '__main__':
    NC_PATH = '../../data_sets/db/northwind.db'
    SC_PATH = '../../data_sets/db/sakila.db'
    CC_PATH = '../../data_sets/db/covid19.db'

    nc, sc, cc = SqlParser(NC_PATH), SqlParser(SC_PATH), SqlParser(CC_PATH)
    nct, sct, cct = nc.table, sc.table, cc.table

    print(nct(name='Order Details',
              cols=['UnitPrice'], distinct=True,
              where=['&20.0 >= UnitPrice <= 70.0', '|UnitPrice > 20'],
              order_by=('UnitPrice', -1),
              limit=5, offset=2))

    print(nct(name='Order Details', cols=['UnitPrice'], distinct=True, where=['&20.0 >= UnitPrice <= 70.0'],
              order_by=('UnitPrice', -1), limit=5, offset=2))

    print(nct(name='Order Details',
              cols=['avg=UnitPrice:UP Avg',
                    'max=UnitPrice:UP Max',
                    'min=UnitPrice:UP Min',
                    'count=UnitPrice:UP Count']))

    print(nc.join(table_left=('Customers:C', ['CompanyName', 'Phone', 'Fax']),
                  table_right=('Orders', ['ShipRegion', 'ShipCountry']),
                  shared_col='CustomerID',
                  starts_with=('Phone', '3'),
                  order_by=('ShipRegion', 1),
                  limit=50,
                  distinct=True,
                  j_type='i'))

    print(cct(name='Cases', count=True, contains=('geoId', 'FR')))

    nc.categories_img(num_cols=3)
