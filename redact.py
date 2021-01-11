import sqlite3
import os
import logging
import errno

from pathlib import Path

from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize


from dbconfig import ColumnNames

log = logging.getLogger(__name__)

PAGE_WIDTH = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]


def drawPlaceholderPage(destination, name):
    c = canvas.Canvas(str(destination))

    text = "REDACTED"
    c.setFont("Helvetica", 24)
    text_redacted = stringWidth(text, "Helvetica", 24)
    c.drawString((PAGE_WIDTH - text_redacted) / 2.0, 700, text)

    c.setFontSize(20)
    text_name = stringWidth(name[:-4], "Helvetica", 20)
    c.drawString((PAGE_WIDTH - text_name) / 2.0, 600, name[:-4])

    c.setFontSize(14)
    c.drawString(50, 100, f'{name} has been marked privileged.')
    c.drawString(50, 80, 'This is a placeholder document.')
    c.drawString(50, 60, 'The original document has been redacted from this production.')

    # c.showPage()
    c.save()


def redact(database, sourceDir: Path, destination: Path, retainDirStructure: bool = False):
    log.info("Redacting documents and creating placeholders.")
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Make the destination directory
    os.makedirs(destination, exist_ok=True)

    # Select all rows not subject to redaction
    c.execute(f'SELECT * FROM documents \
        WHERE {ColumnNames.REDACTED}=1 \
        ORDER BY {ColumnNames.DOCUMENT} DESC')
    rows = c.fetchall()

    for r in rows:
        t = tuple(r)

        # Create the file name i.e., 0123456.pdf
        name = f'{t[0]:07}.pdf'

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

        drawPlaceholderPage(destinationFull, name)

        # print(tuple(r))

    c.close()
    log.info("Redaction complete.")


if __name__ == '__main__':
    import sys
    import logging
    from pathlib import Path

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Can only call logging.basicConfig ONCE
    # Use to Save Logs to File
    logging.basicConfig(filename='redact.log', filemode='w',
                        format='%(levelname)s.%(name)s.%(lineno)d  - %(message)s')

    # Add Additional Handler to Output to STDOUT if you want
    stdout_handler = logging.StreamHandler(sys.stdout)  # Send to Console
    stdout_handler.setLevel(logging.INFO)
    stdout_formatter = logging.Formatter(
        '%(levelname)s - %(message)s')
    stdout_handler.setFormatter(stdout_formatter)
    root.addHandler(stdout_handler)

    redact(
        Path(r"SAMPLEDB.db"),
        Path(r"C:/Users/jason/projects/redactor/sampledata/docs"),
        Path(r"C:/Users/jason/projects/redactor/sampledata/out")
    )
