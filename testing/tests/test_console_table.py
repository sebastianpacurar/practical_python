import pytest
from tabulate import tabulate

from utils_global.console_table.ConsoleTable import ConsoleTable
from utils_global.console_table.Layout import Layout


@pytest.mark.parametrize('layout', list(Layout))
def test_table_layouts(layout):
    data = [
        ['Person One', 24, 3.5],
        ['Person Two', 19, 3.8],
        ['Person Three', 22, 3.1]
    ]
    headers = ['Name', 'Age', 'GPA']
    table = ConsoleTable(data, headers, layout=layout)

    expected_table = tabulate(
        data,
        headers=headers,
        tablefmt=layout.value,
        showindex='never',
        stralign='center'
    ).split('\n')
    print('\n')
    table.display()
    print('\n')
    assert table.build_tabulate() == expected_table, 'Built table does not match expected table'


def test_display(capsys):
    data = [
        ['Person One', 24, 3.5],
        ['Person Two', 19, 3.8],
        ['Person Three', 22, 3.1]
    ]
    headers = ['Name', 'Age', 'GPA']
    table = ConsoleTable(data, headers)
    table._rows = table.build_tabulate()

    table.display()

    captured = capsys.readouterr()
    output = captured.out.strip()
    assert "Person One" in output
    assert "Person Two" in output
    assert "Person Three" in output
