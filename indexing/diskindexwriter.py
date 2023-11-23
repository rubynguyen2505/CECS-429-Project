from .positionalinvertedindex import PositionalInvertedIndex
from pathlib import Path
import struct
import sqlite3
from sqlite3 import Error

class DiskIndexWriter:
    def __init__(self):
        pass

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
    
    def writeIndex(self, index : PositionalInvertedIndex, path : str):
        database = r"pythonsqlite.db"

        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    term text NOT NULL,
                                    byte_position integer NOT NULL,
                                    project_id integer NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""
        

        conn = self.create_connection(database)

        if conn is not None:
            # create projects table
            self.create_table(conn, sql_create_projects_table)

            # create tasks table
            self.create_table(conn, sql_create_tasks_table)
        else:
            print("Error! cannot create the database connection.")

        with conn:
            project = ('Search Engine Index', '2023-11-22', '2023-11-30')
            project_id = self.create_project(conn, project)

            with open(path, "wb") as file:
                for t in index.get_Vocabulary():
                    p_list = index.get_postings(t)
                    file.write(struct.pack("i", len(p_list)))
                    task = (t, file.tell(), project_id)
                    self.create_task(conn, task)
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
