import sqlite3
import calendar
from datetime import datetime, timedelta


def query_traffic_stats(year: int, month: int, db: str, table: str = 'outbound') -> list:
    """
    Query traffic stats with year and month
    :param year: Year
    :param month: Month
    :param db: Database file path.
    :return: Result row list.
    """
    begin_date = datetime.strptime('{0}-{1}-{2}'.format(year, month, 1), '%Y-%m-%d')
    days = calendar.monthrange(year, month)[1]
    end_date = begin_date + timedelta(days=days)
    begin = begin_date.strftime('%Y-%m-%d')
    end = end_date.strftime('%Y-%m-%d')

    sql = 'SELECT email, SUM(traffic) FROM {table} WHERE timestamp BETWEEN "{begin}" AND "{end}" GROUP BY email'.format(
        begin=begin, end=end, table=table)
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    result = cursor.execute(sql).fetchall()
    cursor.close()
    connection.close()

    row_list = list()
    for row in result:
        value = row[1]
        if value > 1073741824:
            value = '{0:6.2f}G'.format(value / 1073741824)
        elif value > 1048576:
            value = '{0:6.2f}M'.format(value / 1048576)
        elif value > 1024:
            value = '{0:6.2f}K'.format(value / 1024)
        else:
            value = '{0:6.2f}B'.format(value)
        row_list.append([row[0], value])

    return row_list

