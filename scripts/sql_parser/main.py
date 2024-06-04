import os

from scripts.sql_parser.SqlParser import SqlParser
from scripts.sql_parser.constants import *

if __name__ == '__main__':
    NC_PATH = os.path.join('..', '..', 'data_sets', 'db', 'northwind.db')
    SC_PATH = os.path.join('..', '..', 'data_sets', 'db', 'sakila.db')
    CC_PATH = os.path.join('..', '..', 'data_sets', 'db', 'covid19.db')

    nc, sc, cc = SqlParser(NC_PATH), SqlParser(SC_PATH), SqlParser(CC_PATH)
    nct, sct, cct = nc.table, sc.table, cc.table

    print(nc.join(table_left={NAME: 'Customers', COLS: ['CompanyName:ID', 'Phone:My Phone', 'Fax:My Fax']},
                  table_right={NAME: 'Orders:o', COLS: ['ShipRegion:Region', 'ShipCountry']},
                  shared_col='CustomerID',
                  starts_with=('Phone', '3'),
                  order_by=('ShipRegion', 1),
                  distinct=True,
                  join=INNER))

    print(nct(name='Order Details',
              cols=['ProductId:Id', 'UnitPrice'], distinct=True,
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

    print(nct(name='Orders',
              cols=['ShipCountry', 'count=*:OrderCount'],
              group_by='ShipCountry',
              order_by=('OrderCount', -1)))

    # total sales amount for each category and supplier
    print(nc.multi_join(
        tables=[{NAME: 'Categories:C', COLS: ['CategoryName']},
                {NAME: 'Products:P', SHARED: 'Categories.CategoryId = Products.CategoryId', JOIN: INNER},
                {NAME: 'Suppliers:S', SHARED: 'Products.SupplierID = Suppliers.SupplierID', COLS: ['CompanyName'], JOIN: INNER},
                {NAME: 'Order Details:OD', SHARED: 'Products.ProductID = Order Details.ProductID', COLS: [], JOIN: INNER}],
        col_agg={AGG_FUNC: 'sum:TotalSales', COLS: ['Products.UnitPrice', 'Order Details.Quantity'], COLS_OP: '*'},
        group_by=['Categories.CategoryName', 'Suppliers.CompanyName']
    ))

    # Average Order Amount by Employee
    print(nc.multi_join(
        tables=[{NAME: 'Employees:E', COLS: ['LastName']},
                {NAME: 'Orders:O', COLS: [], SHARED: 'Employees.EmployeeID = Orders.EmployeeID', JOIN: LEFT},
                {NAME: 'Order Details:OD', COLS: [], SHARED: 'Orders.OrderID = Order Details.OrderID', JOIN: LEFT}],
        col_agg={AGG_FUNC: 'avg:AvgOrderAmount', COLS: ['Order Details.UnitPrice', 'Order Details.Quantity'], COLS_OP: '*'},
        group_by=['Employees.LastName'],
        order_by=('AvgOrderAmount', -1)
    ))
