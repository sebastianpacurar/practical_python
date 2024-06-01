import sqlite3
import pandas as pd
from scripts.sql_parser.table_operations import *

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
            cols: list[str] = '*',
            contains: tuple[str, str | int | float] = None,
            starts_with: tuple[str, str | int | float] = None,
            ends_with: tuple[str, str | int | float] = None,
            distinct: bool = False,
            where: list[str] = None,
            group_by: str | list[str] = None,
            order_by: str | tuple[str, int] = None,
            limit: int = 0,
            offset: int = 0,
            subq: bool = False
    ) -> pd.DataFrame | str:
        name = str_val(name)
        distinct = get_distinct_sql(distinct)
        t_cols = '*'

        # handle cols=[] kwarg
        if cols and '*' not in cols:
            t_cols = format_cols_query(cols)

        t_cols = ',\n\t'.join(t_cols)

        query = f'SELECT {distinct}\n\t{t_cols}\nFROM {name} \n'

        query += get_like_sql(contains, starts_with, ends_with)
        query += get_where_sql(query, where)
        query += get_group_by_sql(group_by)
        query += get_order_by_sql(order_by)
        query += get_limit_sql(limit, offset, order_by)

        # return the query string if subq=True
        res = query if subq is True else self.exec_query(query)
        print(f'\n{query}\n')

        return res

    # join 2 tables only
    def join(
            self,
            table_left: dict[str, str | list[str]],
            table_right: dict[str, str | list[str]],
            shared_col: str,
            join: str = 'i',
            contains: tuple[str, str | int | float] = None,
            starts_with: tuple[str, str | int | float] = None,
            ends_with: tuple[str, str | int | float] = None,
            distinct: bool = False,
            where: list[str] = None,
            group_by: str = None,
            order_by: str | tuple[str, int] = None,
            offset: int = 0,
            limit: int = 0,
            subq: bool = False
    ) -> pd.DataFrame | str:
        distinct = get_distinct_sql(distinct)

        query = get_join_two_table_sql(table_left, table_right, distinct, join, shared_col)
        query += get_like_sql(contains, starts_with, ends_with)
        query += get_where_sql(query, where)
        query += get_group_by_sql(group_by)
        query += get_order_by_sql(order_by)
        query += get_limit_sql(limit, offset, order_by)

        res = query if subq is True else self.exec_query(query)
        print(f'\n{query}\n')

        return res

    # join more than 2 tables
    def multi_join(
            self,
            tables: list[dict[str, str | list[str]]],
            contains: tuple[str, str | int | float] = None,
            starts_with: tuple[str, str | int | float] = None,
            ends_with: tuple[str, str | int | float] = None,
            distinct: bool = False,
            where: list[str] = None,
            group_by: str | list[str] = None,
            order_by: str | tuple[str, int] = None,
            offset: int = 0,
            limit: int = 0,
            col_agg: dict[str, list[str] | str] = None,
            subq: bool = False
    ) -> pd.DataFrame | str:
        distinct = get_distinct_sql(distinct)

        # grab the formatted tables, and all the columns
        tables_data, formatted_cols = process_multi_table_join(tables, col_agg)

        query = get_join_multi_table_sql(tables_data, formatted_cols, distinct)
        query += get_like_sql(contains, starts_with, ends_with)
        query += get_where_sql(query, where)
        query += get_group_by_sql(group_by, tables_data)
        query += get_order_by_sql(order_by)
        query += get_limit_sql(limit, offset, order_by)

        res = query if subq is True else self.exec_query(query)
        print(f'\n{query}\n')

        return res
