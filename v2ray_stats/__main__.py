import argparse
import calendar
import sqlite3
import time
from datetime import datetime, timedelta

from v2ray_stats.collector import collect_traffic_stats
from v2ray_stats.scheduler import schedule
from v2ray_stats.utils import V2RayLogger
from v2ray_stats.output import pretty_print


def init_database(db: str):
    """
    Init database.
    :param db: Database file path.
    :return:
    """
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS outbound ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'email TEXT,'
                   'traffic INT,'
                   'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    cursor.execute('CREATE TABLE IF NOT EXISTS inbound ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'email TEXT,'
                   'traffic INT,'
                   'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    cursor.close()
    connection.commit()
    connection.close()


def query_database(year: int, month: int, db: str, table: str = 'outbound') -> list:
    """
    Query database with year and month
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
    return result


if __name__ == '__main__':
    now = datetime.now()
    date = datetime.strptime('{0}-{1}'.format(now.year, now.month), '%Y-%m')
    days = calendar.monthrange(date.year, date.month)[1]
    last_date = date - timedelta(days=days)

    parser = argparse.ArgumentParser(description='Collect V2Ray user traffic stats.')
    parser.add_argument('-d', dest='db', metavar='database', type=str, nargs='?', default='v2ray_stats.sqlite3',
                        help='Database file path.')
    parser.add_argument('-s', dest='server', metavar='server', type=str, nargs='?', help='V2Ray API server address.')
    parser.add_argument('-e', dest='email', action='store_true', default=False,
                        help='Send traffic email to user every month.')
    parser.add_argument('-c', dest='config_path', metavar='config_path', default='config.json',
                        help='Config file path.')
    parser.add_argument('-q', dest='query', action='store_true', default=False,
                        help='Query mode, with -y and -m to specific month.')
    parser.add_argument('-y', dest='year', type=int, nargs='?', default=last_date.year, help='Query year.')
    parser.add_argument('-m', dest='month', type=int, nargs='?', default=last_date.month, help='Query month.')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='Debug mode.')
    parser.add_argument('--interval', dest='interval', type=int, default=5, help='Collector interval.')
    args = parser.parse_args()

    V2RayLogger.init_logger(debug=args.debug)

    init_database(args.db)

    if args.query:
        pretty_print(query_database(args.year, args.month, args.db))
        pretty_print(query_database(args.year, args.month, args.db, table='inbound'), table='inbound')

    elif args.email:
        pass
    else:
        V2RayLogger.info('Running in background.')
        schedule.every(args.interval).minutes.do(collect_traffic_stats, args.db, args.server)
        while True:
            schedule.run_pending()
            time.sleep(1)
