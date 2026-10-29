
from psycopg.rows import dict_row
from dotenv import load_dotenv
import psycopg
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection() -> psycopg.Connection:
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)
