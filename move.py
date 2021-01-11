import sqlite3
import os
import shutil
from pathlib import Path
import logging
import errno

from dbconfig import ColumnNames

log = logging.getLogger(__name__)


def move(database, sourceDir: Path, destination: Path, retainDirStructure: bool = False):
    log.info("Moving documents.")
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Make the destination directory
    os.makedirs(destination, exist_ok=True)

    # Select all rows not subject to redaction
    c.execute(f'SELECT * FROM documents \
        WHERE {ColumnNames.REDACTED}=0 \
        ORDER BY {ColumnNames.DOCUMENT} DESC')
    rows = c.fetchall()

    for r in rows:
        t = tuple(r)

        # Create the file name i.e., 0123456.pdf
        try:
            name = f'{t[0]:07}.pdf'
        except ValueError as err:
            log.exception(f"Unable to format {t[0]}")
            raise(err)
        # t[1] is the path, remove first character '\' to join paths correctly
        sourceFull = Path(sourceDir, t[1][1:])
        # print(sourceFull)

        # Get Absolute Path

        if retainDirStructure:
            # RETAIN directories
            destinationFull = Path(destination, t[1][1:])

            # Create the intermediate directories
            if not os.path.exists(os.path.dirname(destinationFull)):
                try:
                    os.makedirs(os.path.dirname(destinationFull))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
        else:
            # Do NOT retain directories
            destinationFull = Path(destination, name)

        try:
            shutil.copy(sourceFull, destinationFull)
        except FileExistsError:
            os.remove(destination)
            shutil.copy(sourceFull, destinationFull)

        # print(tuple(r))

    c.close()
    log.info("Move of documents completed.")


if __name__ == '__main__':
    import sys
    import logging
    from pathlib import Path

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Can only call logging.basicConfig ONCE
    # Use to Save Logs to File
    logging.basicConfig(filename='move.log', filemode='w',
                        format='%(levelname)s.%(name)s.%(lineno)d  - %(message)s')

    # Add Additional Handler to Output to STDOUT if you want
    stdout_handler = logging.StreamHandler(sys.stdout)  # Send to Console
    stdout_handler.setLevel(logging.INFO)
    stdout_formatter = logging.Formatter(
        '%(levelname)s - %(message)s')
    stdout_handler.setFormatter(stdout_formatter)
    root.addHandler(stdout_handler)

    move(
        Path(r"SAMPLEDB.db"),
        Path(r"C:/Users/jason/projects/redactor/sampledata/docs"),
        Path(r"C:/Users/jason/projects/redactor/sampledata/out")
    )
