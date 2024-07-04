#!/usr/bin/env python3
"""filtered_logger module"""

import logging
import re
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector import Error
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscate specified fields in a log message."""
    for field in fields:
        message = re.sub(rf"{field}=(.*?)\{separator}",
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Init """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum."""
        original_message = super().format(record)
        return filter_datum(self.fields,
                            self.REDACTION,
                            original_message,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Create and configure a logger."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to a secure database."""
    try:
        db = os.getenv('PERSONAL_DATA_DB_NAME')
        user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
        password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
        host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')

        connection = mysql.connector.connect(host=host, user=user,
                                             password=password, db=db)
        if connection.is_connected():
            print("Db access Granted!")
        return connection
    except Error as e:
        print(f"Error While connecting to the db: {e}")


def main() -> None:
    """Main function to read and filter data."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()

    for row in cursor.fetchall():
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        log_record = logging.LogRecord(
            "user_data", logging.INFO, None, None, message, None, None)
        print(logger.format(log_record))

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
