from enum import Enum


class FilterCondition(Enum):
    CONTAINS = "LIKE '%{}%'"
    STARTS_WITH = "LIKE '{}%'"
    ENDS_WITH = "LIKE '%{}'"


class SqlFunctions(Enum):
    AVG = 'AVG({})'
    SUM = 'SUM({})'
    MAX = 'MAX({})'
    MIN = 'MIN({})'
    COUNT = 'COUNT({})'
    BETWEEN = '{} BETWEEN {} and {}'

    # # math functions
    # ABS = 'ABS({})'
    # ROUND = 'ROUND{}'
    #
    # # string functions
    # LENGTH = 'LENGTH({})'
    # UPPER = 'UPPER({})'
    # LOWER = 'LOWER({})'
    # SUBSTR = 'SUBSTR({}, {}, {})'
    # TRIM = 'TRIM({})'
    #
    # # date time functions
    # DATE = 'DATE({})'
    # TIME = 'TIME({})'
    # STRFTIME = 'STRFTIME({}, {})'
    # JULAINDAY = 'JULAINDAY({})'
