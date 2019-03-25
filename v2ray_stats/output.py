from texttable import Texttable


def pretty_print(data, table: str = 'user_traffic', traffic_type: str = 'downlink'):
    """
    Print data pretty.
    :param data: Data list.
    :param table: table
    :return:
    """

    print('Table: {0} Traffic type: {1}'.format(table, traffic_type))
    table = Texttable()
    table.set_cols_align(["l", "r"])
    table.set_cols_dtype(['t', 'f'])
    table.header(['Name', 'Usage'])
    table.add_rows(data, header=False)
    print(table.draw() + '\n')
