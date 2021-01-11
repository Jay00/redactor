import sqlite3
from pathlib import Path
import logging

from dbconfig import ColumnNames

log = logging.getLogger(__name__)


def writeToCSV(database: str, csvfile: str) -> None:
    log.info("Redacting documents and creating placeholders.")
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute(f'SELECT * FROM documents \
        WHERE {ColumnNames.REDACTED}=1 \
        ORDER BY {ColumnNames.DOCUMENT}')

    FETCH_SIZE = 5

    # Print CSV Headers
    # with open('discovery.csv', 'a+') as f:
    #     f.write(
    #         f"MD5,File\n")

    rows = c.fetchmany(size=FETCH_SIZE)
    while len(rows) > 0:
        # print(f"{len(rows)} rows found.")
        for r in rows:
            # print(tuple(r))
            document = r[ColumnNames.DOCUMENT]
            path = r[ColumnNames.FILE_PATH]

            with open(csvfile, 'a+') as f:
                print(f"{document:09},{path}\n")
                f.write(
                    f"{document:09},{path}\n")
        rows = c.fetchmany(size=FETCH_SIZE)

    c.close()
    print("CSV file Successfully Created.")


if __name__ == '__main__':

    database = Path(r"Bepler.db")
    csvFile = Path(r"C:/Users/jason/projects/redactor/sampledata/privilege.log")

    writeToCSV(database, csvFile)
