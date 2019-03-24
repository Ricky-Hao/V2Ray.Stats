from texttable import Texttable


def pretty_print(data, table: str = 'outbound'):
    """
    Print data pretty.
    :param data: Data list.
    :param table: table
    :return:
    """

    print('Table: {0}'.format(table))
    table = Texttable()
    table.set_cols_align(["l", "r"])
    table.set_cols_dtype(['t', 'f'])
    table.header(['Email', 'Usage'])
    table.add_rows(data, header=False)
    print(table.draw() + '\n')
