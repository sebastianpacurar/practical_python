from scripts.sql_parser.enums import FilterCondition
from scripts.sql_parser.utils import *


# covers LIMIT and OFFSET clauses
def get_limit_sql(limit_param: str | int | None, offset_param: str | int | None, order_by_param: str | None) -> str:
    sql = ''
    if limit_param:
        lim = get_int_or_zero(limit_param)
        if lim != 0:
            if not order_by_param and lim < 0:
                sql += 'ORDER BY 1 DESC\n'
            sql += f'LIMIT {abs(lim)}'

            if offset_param:
                off_val = get_int_or_zero(offset_param)
                if off_val > 0:
                    sql += f' OFFSET {off_val}'

    return sql


# covers GROUP BY clause
def get_group_by_sql(
        group_by_param: list[str] | str,
        tables_data: list[dict[str, str]] = None
) -> str:
    sql = ''
    if group_by_param:
        if get_list_or_zero(group_by_param):
            formatted = []
            for item in group_by_param:
                table, col = str_val(*item.split('.'))

                # set name to alias if present, else keep name
                for td in tables_data:
                    if 'alias' in td and td['name'] == table:
                        table = td['alias']
                        break

                formatted.append(f'{table}.{col}')
            sql += f'Group By {", ".join(formatted)}\n'
        else:
            sql += f'GROUP BY {group_by_param}\n'
    return sql


# covers ORDER BY clause
def get_order_by_sql(
        order_by_param: str,
        tables_data: list[dict[str, str]] = None
) -> str:
    sql = ''
    if order_by_param:
        pair, direction = order_by_param
        if '.' in pair:
            pair = pair.split('')
            # set name to alias if present, else keep name
            for td in tables_data:
                if 'alias' in td and td['name'] == pair[0]:
                    pair[0] = td['alias']
                    break

            pair = '.'.join(pair)

        sql = f'ORDER BY {pair} {"ASC" if int(direction) >= 0 else "DESC"}\n'
    return sql


# covers WHERE clause
# TODO Update to handle table aliasing
def get_where_sql(query: str, where_param: list[str] | None) -> str:
    sql = ''
    if where_param:
        if get_list_or_zero(where_param):
            checked = False
            for i, cond in enumerate(where_param):
                or_and_choice = and_or_operator(cond)
                if "WHERE" not in query and not checked:
                    checked = True
                    start = "WHERE"
                else:
                    start = f'\t{or_and_choice}' if i > 0 else f'\t{or_and_choice}'
                is_between_agg, agg_vals = get_between_agg(cond[1:])
                if is_between_agg:
                    low, col, high = agg_vals
                    sql += f'{start} {SqlFunctions.BETWEEN.value.format(col, low, high)}\n'
                else:
                    sql += f'{start} {cond[1:]}\n'
    return sql


# covers LIKE clause
def get_like_sql(c: tuple[str, str] | None, sw: tuple[str, str] | None, ew: tuple[str, str] | None) -> str:
    sql = ''
    if c or sw or ew:
        cond = 'contains' if c else 'starts_with' if sw else 'ends_with'
        col, col_val = c if c else sw if sw else ew

        formatted_like = FilterCondition[cond.upper()].value.format(col_val)
        sql = f'WHERE {col} {formatted_like}\n'
    return sql


# covers JOIN clause for more than 2 tables
def get_join_multi_table_sql(tables_data: list[dict[str, str | list[str]]], formatted_cols: list[str], distinct: str) -> str:
    sql = f'SELECT {distinct}'
    sql += ','.join(formatted_cols)
    sql += f'\nFROM {tables_data[0].get("title")}\n'

    for t in tables_data[1:]:
        sql += f"{format_join_type(t.get('join'))} JOIN {t.get('title')} ON {t.get('shared')}\n"

    return sql


# covers JOIN clause for 2 tables only
def get_join_two_table_sql(
        table_left: dict[str, str | list[str]],
        table_right: dict[str, str | list[str]],
        distinct: str,
        join: str,
        shared_col: str
) -> str:
    l_table, l_cols = process_two_table_join(table_left)
    r_table, r_cols = process_two_table_join(table_right)
    cols = l_cols + r_cols
    sql = f'SELECT {distinct}'
    sql += ','.join(cols)

    sql += f'\nFROM {l_table.get("title")}\n'
    sql += f'{format_join_type(join)} JOIN {r_table.get("title")}\n'
    sql += f'ON {l_table.get("name")}.{shared_col} = {r_table.get("name")}.{shared_col}\n'
    return sql


# covers DISTINCT clause
def get_distinct_sql(distinct_param: bool) -> str:
    return 'DISTINCT ' if distinct_param is True else ''
