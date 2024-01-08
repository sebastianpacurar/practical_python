from enum import Enum


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
    BETWEEN = '{} BETWEEN {} and {}'
