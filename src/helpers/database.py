import sqlite3
from pathlib import Path
from src.config import DB_PATH

class Database: 
  def __init__(self):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    self.db_path = DB_PATH
  
  def get_connection(self): 
    return sqlite3.connect(self.db_path)
  
  def create_table_apps(self): 
    with self.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute('''
      CREATE TABLE IF NOT EXISTS apps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        value TEXT NOT NULL,
        callback TEXT NOT NULL DEFAULT ''
      )
      ''')
      conn.commit()
  
  def create_table_logs(self):
    with self.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          name TEXT NOT NULL,
          type TEXT NOT NULL, 
          value TEXT NOT NULL, 
          callback TEXT NOT NULL DEFAULT ''
          created_at DEFAULT CURRENT_TIMESTAMP
        )
      ''')
  
  def execute(self, query:str, params:tuple=None):
    with self.get_connection() as conn: 
      cursor = conn.cursor()
      if params: 
        cursor.execute(query, params)
      else:
        cursor.execute(query)
      conn.commit()
      return cursor.lastrowid
  
  def fetch_one(self, query:str, params:tuple=None): 
    with self.get_connection() as conn:
      conn.row_factory = sqlite3.Row
      cursor = conn.cursor()
      if params: 
        cursor.execute(query, params)
      else:
        cursor.execute(query)
      row = cursor.fetchone()
      return dict(row) if row else None

  def fetch_all(self, query:str, params:tuple=None): 
    with self.get_connection() as conn:
      conn.row_factory = sqlite3.Row
      cursor = conn.cursor()
      if params: 
        cursor.execute(query, params)
      else:
        cursor.execute(query)
      rows = cursor.fetchall()
      return [dict(row) for row in rows]
  
  def insert(self, table:str, data:dict[str, any]): 
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
    return self.execute(query, tuple(data.values()))
  
  def update(self, table:str, data:dict[str, any], where_clause:str, where_params: tuple):
    set_clause = ', '.join([f'{k} = ?' for k in data.keys()])
    query = f'UPDATE {table} SET {set_clause} WHERE {where_clause}'
    params = tuple(data.values()) + tuple(where_params)
    return self.execute(query, params)
  
  def delete(self, table:str, where_clause:str, where_params:tuple):
    query = f'DELETE FROM {table} WHERE {where_clause}'
    return self.execute(query, where_params)
  
  def get_table_info(self, table_name:str):
    query = f'PRAGMA table_info({table_name})'
    return self.fetch_all(query)
  
  def get_table_columns(self, table_name:str)-> list[str]:
    info = self.get_table_info(table_name)
    return [row[1] for row in info]
  
  def get_all_tables(self):
    query = "SELECT name from sqlite_master WHERE type='table'"
    tables = self.fetch_all(query)
    return [table[0] for table in tables]
  
  def get_table_schema(self, table_name:str):
    query = f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?"
    result = self.fetch_one(query, (table_name,))
    return result[0] if result else None
