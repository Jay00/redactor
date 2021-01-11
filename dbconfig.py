from typing import NamedTuple
from collections import namedtuple


class ColumnNames(object):
    DOCUMENT = 'document'
    FILE_PATH = 'file_path'
    REDACTED = 'redacted'


DocumentRecord: NamedTuple = namedtuple('DocumentRecord',
                                        f'{ColumnNames.DOCUMENT}, {ColumnNames.FILE_PATH}')


def Create_Discovery_Table_SQL(TableName="documents") -> str:

    SQL_TABLE = f'''CREATE TABLE if not exists {TableName}(
        {ColumnNames.DOCUMENT} INTEGER PRIMARY KEY,
        {ColumnNames.FILE_PATH} TEXT,
        {ColumnNames.REDACTED} INTEGER DEFAULT 0) WITHOUT ROWID;'''

    # SQLite does not have a separate Boolean storage class.
    # Instead, Boolean values are stored as integers 0 (false) and 1 (true).
    return SQL_TABLE
