import sqlite3
from typing import Any, Optional
from .db_manager import DatabaseManager

class SQlite(DatabaseManager):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

    def execute(self, query: str, params: tuple = ()) -> None:
        self.connect()
        with self.connection:
            self.connection.execute(query, params)
    
    def fetch_all(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        return result
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None