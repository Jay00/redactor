import sqlite3
import logging

from dbconfig import ColumnNames

log = logging.getLogger(__name__)


def mark(database):
    conn = sqlite3.connect(database)

    c = conn.cursor()

    # Mark Rows for Redaction
    c.execute(f"UPDATE documents \
            SET {ColumnNames.REDACTED} = 1 \
            WHERE {ColumnNames.FILE_PATH} LIKE '%sonnenschein%' OR \
            {ColumnNames.FILE_PATH} LIKE '%denton%' OR \
                {ColumnNames.FILE_PATH} LIKE '%ivins-philips-barker%' OR \
            {ColumnNames.FILE_PATH} LIKE '%fortney-scott%'")

    log.info(f"Total Documents marked for redaction: {conn.total_changes}")

    conn.commit()
    c.close()


if __name__ == '__main__':
    from pathlib import Path

    mark(
        Path(r"SAMPLEDB.db"),
    )
