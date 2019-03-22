from texttable import Texttable


def pretty_print(data, table: str = 'outband'):
    """
    Print data pretty.
    :param data: Data list.
    :param table: table
    :return:
    """

    row_list = list()
    for row in data:
        value = row[1]
        if value > 1073741824:
            value = '{0:6.2f}G'.format(value/1073741824)
        elif value > 1048576:
            value = '{0:6.2f}M'.format(value/1048576)
        elif value > 1024:
            value = '{0:6.2f}K'.format(value/1024)
        else:
            value = '{0:6.2f}B'.format(value)
        row_list.append([row[0], value])


    print('Table: {0}'.format(table))
    table = Texttable()
    table.set_cols_align(["l", "r"])
    table.set_cols_dtype(['t', 'f'])
    table.header(['Email', 'Usage'])
    table.add_rows(row_list, header=False)
    print(table.draw() + '\n')
