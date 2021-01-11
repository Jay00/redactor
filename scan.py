import os
from pathlib import Path
import logging
from datetime import datetime
import sqlite3

# Custom
from dbconfig import Create_Discovery_Table_SQL

log = logging.getLogger(__name__)


def scan(directory: Path, database: Path) -> int:
    '''Iterate through the files and Load to an SQLITE Db file'''

    assert directory.is_dir(
    ), f"Must be directory to walk.  Received: {directory}"

    log.info(f"Walking directory: {directory}")

    total_files_processed: int = 0

    # Open Connection to Database
    conn = sqlite3.connect(database)
    conn.execute(Create_Discovery_Table_SQL())
    c = conn.cursor()

    for dirName, _, fileList in os.walk(directory):

        dirPath = Path(dirName)
        relative_folder_path = str(dirPath.relative_to(
            directory))

        log.debug(f"Processing directory: {relative_folder_path}")

        for fname in fileList:
            full_path: str = os.path.join(
                dirName, fname)

            path_relative_to_master: str = full_path.replace(
                str(directory), '')

            log.debug(path_relative_to_master)

            # Load to SQLITE DB
            try:
                c.execute(
                    'INSERT INTO documents VALUES (?, ?, ?)', (fname[0:-4], path_relative_to_master, 0))

                total_files_processed += 1
            except sqlite3.IntegrityError as err:
                log.exception(f"SQL FAILED: 'INSERT INTO documents VALUES (?, ?, ?)', ({fname[0:-4]}, {path_relative_to_master}, {0})")
                log.exception(err)
            except UnicodeEncodeError as err:
                # Occurs for some files with problematic names
                log.exception(f"UnicodeEncodeError: 'INSERT INTO documents VALUES (?, ?, ?)', ({fname[0:-4]}, {path_relative_to_master}, {0})")
                log.exception(err)
                raise(err)

    # Close Database Connection
    conn.commit()
    c.close()

    log.info(
        f"Finished loading discovery.  Total New Files Loaded: {total_files_processed}")

    log.info(f"Last update completed at: {datetime.now().timestamp()}")

    return total_files_processed


if __name__ == '__main__':
    import sys
    import logging
    from pathlib import Path

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Can only call logging.basicConfig ONCE
    # Use to Save Logs to File
    logging.basicConfig(filename='scan.log', filemode='w',
                        format='%(levelname)s.%(name)s.%(lineno)d  - %(message)s')

    # Add Additional Handler to Output to STDOUT if you want
    stdout_handler = logging.StreamHandler(sys.stdout)  # Send to Console
    stdout_handler.setLevel(logging.INFO)
    stdout_formatter = logging.Formatter(
        '%(levelname)s - %(message)s')
    stdout_handler.setFormatter(stdout_formatter)
    root.addHandler(stdout_handler)

    scan(Path(r"sampledata\docs"), Path(r"SAMPLEDB.db"))
