from bisect import bisect_left
from decimal import InvalidOperation
from pathlib import Path
from pydoc import doc
from typing import Iterable
from .postings import Posting
from .index import Index
from .diskindexwriter import DiskIndexWriter
import struct
import sqlite3
from sqlite3 import Error

class DiskPositionalIndex(Index):
    def __init__(self, path):
        self.path = path

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn

    def select_all_tasks(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM TBP")

        rows = cur.fetchall()

        for row in rows:
            print(row)

    def select_task_by_term(self, conn, term):
        cur = conn.cursor()
        cur.execute("SELECT * FROM TBP WHERE term=?", (term,))

        rows = cur.fetchall()

        return rows

    def get_postings(self, term : str):
        p_list = []
        database = r"pythonsqlite.db"
        conn = self.create_connection(database)
        with conn:
            print(f"Get byte position for term {term}:")

            row = self.select_task_by_term(conn, term)
            byte_position = row[0][1]

            with open(self.path, 'rb') as file:
                file.seek(byte_position, 0)
                length = list(struct.unpack('i', file.read(4)))
                i = 0
                while i < length[0]:
                    doc_id = list(struct.unpack('i', file.read(4)))

                    if i > 0:
                        doc_id[0] = doc_id[0] + p_list[i - 1].doc_id
                    tftd = list(struct.unpack('i', file.read(4)))

                    j = 0
                    while j < tftd[0]:
                        position = list(struct.unpack('i', file.read(4)))
                        if j > 0:
                            position[0] = position[0] + p_list[i].position[j - 1]
                            p_list[i].position.append(position[0])
                        else:
                            p_list.append(Posting(doc_id[0], position[0]))
                        j += 1
                    i += 1
                file.close()
        
        return p_list
    
    def get_postings_skip(self, term : str):
        p_list = []
        database = r"pythonsqlite.db"
        conn = self.create_connection(database)
        with conn:
            print(f"Get byte position for term {term}:")

            row = self.select_task_by_term(conn, term)
            byte_position = row[0][2]

            with open(self.path, 'rb') as file:
                file.seek(byte_position, 0)
                print(file.tell())
                length = list(struct.unpack('i', file.read(4)))
                print(length)
                print(file.tell())
                i = 0
                while i < length[0]:
                    doc_id = list(struct.unpack('i', file.read(4)))
                    print(file.tell())

                    if i > 0:
                        doc_id[0] = doc_id[0] + p_list[i - 1].doc_id
                    tftd = list(struct.unpack('i', file.read(4)))
                    print(file.tell())

                    p_list.append(Posting(doc_id[0], 0))
                    file.seek(tftd[0], file.tell())
                    i += 1
                file.close()
        
        return p_list


        