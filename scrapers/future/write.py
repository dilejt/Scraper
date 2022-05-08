import csv

from consts import WRITING_MODE, NEWLINE, DELIMITER, OFFICE_PROPERTY
from helpers import getFileName


def write_to_file(result_arr):
    with open(getFileName(OFFICE_PROPERTY['future']), WRITING_MODE, newline=NEWLINE) as f:
        writer = csv.writer(f, delimiter=DELIMITER)
        for row in result_arr:
            writer.writerow(row)
