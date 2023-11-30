from .positionalinvertedindex import PositionalInvertedIndex
from pathlib import Path
import struct
import sqlite3
from sqlite3 import Error

class DiskIndexWriter:
    def __init__(self):
        pass

    """
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn
    
    def create_table(self, conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_project(self, conn, project):
        sql = ''' INSERT INTO projects(name,begin_date,end_date) 
                  VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, project)
        conn.commit()
        return cur.lastrowid
    
    def create_task(self, conn, task):
        sql = ''' INSERT INTO tasks(term,byte_position,project_id)
                  VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid
    
    def delete_project(self, conn, id):
        sql = 'DELETE FROM projects WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()

    def delete_all_projects(self, conn):
        sql = 'DELETE FROM projects'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def delete_task(self, conn, id):
        sql = 'DELETE FROM tasks WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()

    def delete_all_tasks(self, conn):
        sql = 'DELETE FROM tasks'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    """

    def writeIndex(self, index : PositionalInvertedIndex, path : str):
        connection_obj = sqlite3.connect('pythonsqlite.db')

        cursor_obj = connection_obj.cursor()
        cursor_obj.execute("DROP TABLE IF EXISTS TBP")
        table = """ CREATE TABLE IF NOT EXISTS TBP (
                    term text NOT NULL,
                    byte_position integer NOT NULL
                    );"""
        cursor_obj.execute(table)

        sql = ''' INSERT INTO TBP(term,byte_position)
                  VALUES(?,?) '''

        with open(path, "wb") as file:
            for t in index.get_Vocabulary():
                p_list = index.get_postings(t)
                task = (t, file.tell())
                cursor_obj.execute(sql, task)
                file.write(struct.pack("i", len(p_list)))
                i = 0
                while i < len(p_list):
                    if i == 0:
                        file.write(struct.pack("i", p_list[i].doc_id))
                    else:
                        file.write(struct.pack("i", p_list[i].doc_id - p_list[i - 1].doc_id))
                    file.write(struct.pack("i", len(p_list[i].position)))
                    j = 0
                    while j < len(p_list[i].position):
                        if j == 0:
                            file.write(struct.pack("i", p_list[i].position[j]))
                        else:
                            file.write(struct.pack("i", p_list[i].position[j] - p_list[i].position[j - 1]))
                        j += 1
                    i += 1

            file.close()
        connection_obj.commit()

        connection_obj.close()
