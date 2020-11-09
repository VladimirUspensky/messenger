import os
import psycopg2
from typing import Dict, List, Tuple


conn = psycopg2.connect(dbname='messengerdb',  password=os.getenv('PASSWORDDATABASE'),
                        user=os.getenv('USERDATABASE'), host='localhost')
cursor = conn.cursor()


def insert(table: str, column_values: Dict) -> None:
    """Wrapper for INSERT postgresql"""
    columns = ' ,'.join(column_values.keys())
    values = ' ,'.join(column_values.values()).split(',')

    placeholders = []
    for column in column_values.keys():
        placeholders.append('%s')

    placeholders = ', '.join(placeholders)

    cursor.execute(f'INSERT INTO {table} ({columns}) VALUES ({placeholders})', values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    """Wrapper for SELECT postgresql"""
    result = []
    columns = ' ,'.join(columns)
    cursor.execute(f'SELECT {columns} FROM {table}')
    raws = cursor.fetchall()
    for raw in raws:
        result.append(raw)
    return result


def delete(table: str, raw_id: int) -> None:
    """Wrapper for DELETE postgresql"""
    cursor.execute(f'DELETE FROM {table} WHERE {table}.id=%s', (raw_id,))
    conn.commit()


#insert('clients', {'name': 'Jack', 'addr': 'xzxcxcx'})
#print(fetchall('clients', ['id', 'name', 'addr']))
