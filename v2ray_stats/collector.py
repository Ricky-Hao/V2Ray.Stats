import sqlite3

from v2ray_stats.scheduler import catch_exceptions
from v2ray_stats.v2ctl import V2Ctl


@catch_exceptions
def collect_traffic_stats(db: str, server: str, reset: bool = True):
    """
    Only collect outbound traffic.
    :return:
    """
    assert isinstance(db, str)
    assert isinstance(server, str)
    assert isinstance(reset, bool)

    v2ctl = V2Ctl(server=server)
    stats_list = v2ctl.query_stats(reset=reset)

    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    for stats in stats_list:
        if stats['bound'] == 'outbound':
            cursor.execute('INSERT INTO outbound(email, traffic) VALUES (?, ?)', (stats[0], int(stats[1])))
    cursor.close()
    connection.commit()
    connection.close()
    print('[Stats] Collect every 5 minutes.')
