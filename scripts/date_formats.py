from datetime import datetime

from utils_global.ConsoleTable import ConsoleTable

now: datetime = datetime.now()
headers: list[str] = ['Notation', 'Example', 'Description']


def weekday_and_week_number_formatting() -> None:
    print('\nWeekday and Week Number Formatting')
    data: list[list[str]] = [
        ['%A', f'{now:%A}', 'full weekday name'],
        ['%a', f'{now:%a}', 'abbreviated weekday name'],
        ['%w', f'{now:%w}', 'weekday as number (0=sunday, 6=saturday)'],
        ['%U', f'{now:%U}', 'week number of the year (sunday is first)'],
        ['%W', f'{now:%W}', 'week number of the year (monday is first)'],
        ['%V', f'{now:%V}', 'ISO 8601 week number'],
    ]
    ConsoleTable(data, headers=headers).display()


def month_formatting() -> None:
    print('\nMonth Formatting:')
    data: list[list[str]] = [
        ['%B', f'{now:%B}', 'full month name'],
        ['%b', f'{now:%b}', 'abbreviated month name'],
        ['%m', f'{now:%m}', 'month as zero-padded (01-12)'],
    ]
    ConsoleTable(data, headers=headers).display()


def day_year_formatting() -> None:
    print('\nDay and Year Formatting:')
    data: list[list[str]] = [
        ['%d', f'{now:%d}', 'day of the month (01-31)'],
        ['%j', f'{now:%j}', 'day of the year (001-366)'],
        ['%Y', f'{now:%Y}', 'year with all digits'],
        ['%y', f'{now:%y}', 'year with last 2 digits'],
        ['%G', f'{now:%G}', 'ISO 8601 year with century'],
        ['%g', f'{now:%g}', 'ISO 8601 year without century']
    ]
    ConsoleTable(data, headers=headers).display()


def time_formatting() -> None:
    print('\nTime Formatting:')
    data: list[list[str]] = [
        ['%X', f'{now:%X}', 'locale appropriate time representation'],
        ['%H', f'{now:%H}', 'hour (00-23)'],
        ['%I', f'{now:%I}', 'hour (01-12)'],
        ['%M', f'{now:%M}', 'minute (00-59)'],
        ['%S', f'{now:%S}', 'second (00-59)'],
        ['%f', f'{now:%f}', 'microsecond (000000-999999)'],
        ['%p', f'{now:%p}', 'AM or PM'],
        ['%T', f'{now:%T}', 'time as HH:MM:SS']
    ]
    ConsoleTable(data, headers=headers).display()


def date_formatting() -> None:
    print('\nDate Formatting:')
    data: list[list[str]] = [
        ['%x', f'{now:%x}', 'locale appropriate date representation'],
        ['%D', f'{now:%D}', 'date as MM/DD/YY'],
        ['%F', f'{now:%F}', 'date as YYYY-MM-DD']
    ]
    ConsoleTable(data, headers=headers).display()


def various_combinations() -> None:
    print('\nVarious Combinations:')
    data: list[list[str]] = [
        ['ISO 8601 format', '%Y-%m-%dT%H:%M:%S', f'{now:%Y-%m-%dT%H:%M:%S}'],
        ['RFC 2822 format', '%a, %d %b %Y %H:%M:%S %z', f'{now:%a, %d %b %Y %H:%M:%S %z}'],
        ['ISO 8601 with TZ', '%Y-%m-%dT%H:%M:%S%z', f'{now:%Y-%m-%dT%H:%M:%S%z}'],
        ['RFC 3339', '%Y-%m-%dT%H:%M:%S%z', f'{now:%Y-%m-%dT%H:%M:%S%z}'],
        ['Year-month-day', '%Y-%m-%d', f'{now:%Y-%m-%d}'],
        ['day-month-Year', '%d-%m-%Y', f'{now:%d-%m-%Y}'],
        ['mm/dd/YYYY HH:MM:SS', '%m/%d/%Y %H:%M:%S', f'{now:%m/%d/%Y %H:%M:%S}'],
        ['HTTP-date', '%a, %d %b %Y %H:%M:%S GMT', f'{now:%a, %d %b %Y %H:%M:%S GMT}'],
        ['log format', '%Y-%m-%d %H:%M:%S,%f', f'{now:%Y-%m-%d %H:%M:%S,%f}'],
        ['human-readable', '%A, %B %d, %Y %I:%M %p', f'{now:%A, %B %d, %Y %I:%M %p}'],
        ['sortable', '%Y%m%dT%H%M%S', f'{now:%Y%m%dT%H%M%S}'],
        ['weekday, day, month, year', '%A, %d %B %Y', f'{now:%A, %d %B %Y}'],
        ['short date time', '%m/%d/%y %I:%M %p', f'{now:%m/%d/%y %I:%M %p}'],
        ['date time with fractional seconds', '%Y-%m-%d %H:%M:%S.%f', f'{now:%Y-%m-%d %H:%M:%S.%f}'],
        ['24-hour clock time', '%H:%M', f'{now:%H:%M}'],
        ['12-hour clock time', '%I:%M %p', f'{now:%I:%M %p}'],
        ['file-safe', '%Y-%m-%d_%H-%M-%S', f'{now:%Y-%m-%d_%H-%M-%S}'],
        ['week number', '%Y-W%V', f'{now:%Y-W%V}'],
        ['compact date', '%Y%m%d', f'{now:%Y%m%d}'],
        ['extended date and time', '%A, %B %d, %Y at %I:%M %p', f'{now:%A, %B %d, %Y at %I:%M %p}'],
        ['database timestamp', '%Y-%m-%d %H:%M:%S.%f', f'{now:%Y-%m-%d %H:%M:%S.%f}']
    ]
    ConsoleTable(data, headers=['Description', 'Format', 'Example']).display()


if __name__ == '__main__':
    weekday_and_week_number_formatting()
    month_formatting()
    day_year_formatting()
    time_formatting()
    date_formatting()
    various_combinations()
