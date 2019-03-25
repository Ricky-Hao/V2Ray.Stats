import sqlite3

from v2ray_stats.scheduler import catch_exceptions
from v2ray_stats.utils import V2RayLogger
from v2ray_stats.v2ctl import V2Ctl


@catch_exceptions
def collect_traffic_stats(db: str, server: str, pattern: str = '', reset: bool = True):
    """
    Only collect outbound traffic.
    :return:
    """
    assert isinstance(db, str)
    assert isinstance(server, str)
    assert isinstance(reset, bool)

    v2ctl = V2Ctl(server=server)
    stats_list = v2ctl.query_stats(pattern=pattern, reset=reset)
    V2RayLogger.debug(stats_list)

    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    for stats in stats_list:
        if stats['type'] == 'user':
            if stats['bound'] == 'downlink':
                sql = 'INSERT INTO outbound(email, traffic) VALUES ("{0}", {1})'.format(stats['name'],
                                                                                        int(stats['value']))
                cursor.execute(sql)
                V2RayLogger.debug(sql)
            elif stats['bound'] == 'uplink':
                sql = 'INSERT INTO inbound(email, traffic) VALUES ("{0}", {1})'.format(stats['name'],
                                                                                       int(stats['value']))
                cursor.execute(sql)
                V2RayLogger.debug(sql)
        elif stats['type'] == 'system':
            pass
    cursor.close()
    connection.commit()
    connection.close()
    V2RayLogger.info('Collect {0} account.'.format(int(len(stats_list) / 2)))
