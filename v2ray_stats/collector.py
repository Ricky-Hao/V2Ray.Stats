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
    outbound_list = list()
    for stats in stats_list:
        if stats['bound'] == 'outbound':
            temp_tuple = (stats['email'], int(stats['value']))
            outbound_list.append(temp_tuple)

    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.executemany('INSERT INTO outbound(email, traffic) VALUES (?, ?)', outbound_list)
    cursor.close()
    connection.commit()
    connection.close()
    print('[Stats] Collect every 5 minutes.')
