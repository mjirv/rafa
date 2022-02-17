def date_trunc(datepart, date):
    date_periods = {
        'day': '%Y-%m-%d',
        'week': '%Y-%W',
        'month': '%Y-%m',
        'year': '%Y'
    }

    return f"strftime('{ date_periods[datepart] }', {date})"