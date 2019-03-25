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
            sql = 'INSERT INTO user_traffic(name, traffic, type) VALUES ("{0}", {1}, "{2}")'.format(stats['name'],
                                                                                                    int(stats['value']),
                                                                                                    stats['bound'])
            cursor.execute(sql)
            V2RayLogger.debug(sql)
        elif stats['type'] == 'system':
            sql = 'INSERT INTO system_traffic(name, traffic, type) VALUES ("{0}", {1}, "{2}")'.format(stats['name'],
                                                                                                      int(stats[
                                                                                                              'value']),
                                                                                                      stats['bound'])
            cursor.execute(sql)
            V2RayLogger.debug(sql)
    cursor.close()
    connection.commit()
    connection.close()
    V2RayLogger.info('Collect {0} account.'.format(int(len(stats_list) / 2)))
