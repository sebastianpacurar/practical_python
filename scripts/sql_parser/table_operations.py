from scripts.sql_parser.enums import FilterCondition
from scripts.sql_parser.utils import *


# covers LIMIT and OFFSET clauses
def get_limit_sql(limit_param, offset_param, order_by_param):
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


# covers ORDER BY clause
# TODO Update to handle table aliasing
def get_order_by_sql(order_by_param):
    sql = ''
    if order_by_param:
        col, direction = order_by_param
        sql = f'ORDER BY {col} {"ASC" if int(direction) >= 0 else "DESC"}\n'
    return sql


# covers WHERE clause
# TODO Update to handle table aliasing
def get_where_sql(query, where_param):
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
                    sql += f'{start} {AggregateFunctions.BETWEEN.value.format(col, low, high)}\n'
                else:
                    sql += f'{start} {cond[1:]}\n'
    return sql


# covers LIKE clause
def get_like_sql(c, sw, ew):
    sql = ''
    if c or sw or ew:
        cond = 'contains' if c else 'starts_with' if sw else 'ends_with'
        col, col_val = c if c else sw if sw else ew
        formatted_like = FilterCondition[cond.upper()].value.format(col_val)
        sql = f'WHERE {col} {formatted_like}\n'
    return sql


# covers JOIN clause
def get_join_sql(tables, distinct, j_type):
    parsed_names, parsed_titles = [], []
    formatted_cols = []

    for t in tables:
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
            cols = map(lambda x: str_val(x), t['cols'])
            for col in cols:
                if table_alias is not None:
                    formatted_cols.append(f'\n\t{table_alias}.{col}')
                else:
                    formatted_cols.append(f'\n\t{str_val(name)}.{col}')
        else:
            if table_alias is not None:
                formatted_cols.append(f'\n\t{table_alias}.*')
            else:
                formatted_cols.append(f'\n\t{str_val(name)}.*')

        parsed_names.append(t_name)
        parsed_titles.append(t_title)

    # add "" (quotation marks) to 2 word based title names
    for i, title in enumerate(parsed_titles):
        group = title.split(' ')
        if len(group) > 2:

            for g in group[:-2]:
                title = f'"{g} '
            title += f'{group[-2]}" '

            title += group[-1]
            parsed_titles[i] = title

    # start of query creation here:
    sql = f'SELECT {distinct}'

    sql += ','.join(formatted_cols)
    for i, t in enumerate(tables):
        val = i if i == 0 else i - 1

        if i == 0:
            sql += f'\nFROM {parsed_titles[0]}\n'
            continue

        # TODO: need to treat issue with the parsed_name vs alias for table names, otherwise -> ambiguous column name: c.CompanyName

        sql += f'{format_join_type(j_type)} JOIN {parsed_titles[i]} ON {parsed_names[val]}.{t["shared"]} = {parsed_names[i]}.{t["shared"]}\n'

    return sql


# covers DISTINCT clause
def get_distinct_sql(distinct_param):
    return 'DISTINCT ' if distinct_param is True else ''
