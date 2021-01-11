from pathlib import Path
import logging

from scan import scan
from markForRedaction import mark
from redact import redact
from move import move

log = logging.getLogger(__name__)


def run():

    log.info("Preparing to copy and redact documents")

    directory = Path(r"C:\Users\jason\Dropbox\civil\Bebler-Anybill-SuperiorCourt-Appeal\Boxes\Anybill_docs")
    destinationFlat = Path(r"C:\Users\jason\Desktop\Bepler\Flat")
    destinationOrganized = Path(r"C:\Users\jason\Desktop\Bepler\Organized")
    db = Path(r"Bepler.db")

    scan(directory, db)
    mark(db)

    redact(db, directory, destinationFlat, retainDirStructure=False)
    move(db, directory, destinationFlat, retainDirStructure=False)

    redact(db, directory, destinationOrganized, retainDirStructure=True)
    move(db, directory, destinationOrganized, retainDirStructure=True)


if __name__ == '__main__':

    import sys
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Can only call logging.basicConfig ONCE
    # Use to Save Logs to File
    logging.basicConfig(filename='main.log', filemode='w',
                        format='%(levelname)s.%(name)s.%(lineno)d  - %(message)s')

    # Add Additional Handler to Output to STDOUT if you want
    stdout_handler = logging.StreamHandler(sys.stdout)  # Send to Console
    stdout_handler.setLevel(logging.INFO)
    stdout_formatter = logging.Formatter(
        '%(levelname)s - %(message)s')
    stdout_handler.setFormatter(stdout_formatter)
    root.addHandler(stdout_handler)

    # move_logger = logging.getLogger('move')
    # move_logger.setLevel(logging.INFO)
    # move_formatter = logging.Formatter(
    #     '%(levelname)s - %(message)s')
    # move_logger.setFormatter(move_formatter)

    # # move_logger.addHandler(move_handler)

    run()
