import sqlite3


class TodoProjects:
    def __init__(self, db_file):
        """ create a database connection to the SQLite database
               specified by db_file
           :param db_file: database file
           :return: Connection object or None
           """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)

    def create_project(self, data):
        """
        Create a new project into the projects table
        :param data:
        :return: project id
        """
        sql = '''INSERT INTO projects(nazwa, start_date, end_date, status)
                 VALUES(?,?,?,?)'''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid

    def all_projects(self):
        self.cur.execute(f"SELECT * FROM projects")
        rows = self.cur.fetchall()
        return rows

    def get_projects(self, id):

        self.cur.execute(f"SELECT * FROM projects WHERE id = ?", id)
        rows = self.cur.fetchall()
        return rows


class TodoTasks:
    def __init__(self, db_file):
        """ create a database connection to the SQLite database
        specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()

        except sqlite3.Error as e:
            print(e)

    def create_task(self, data):
        """
        Create a new zadanie into the tasks table
        :param zadanie:
        :return: zadanie id
        """

        sql = '''INSERT INTO tasks(projekt_id, nazwa, opis, start_date, end_date)
                     VALUES(?,?,?,?,?)'''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid

    def all_tasks(self):
        self.cur.execute(f"SELECT * FROM tasks")

        return self.cur.fetchall()

    def get_tasks(self, id):

        self.cur.execute(f"SELECT * FROM tasks WHERE id = ?", id)
        rows = self.cur.fetchall()
        return rows


db_file = "database.db"
projects = TodoProjects(db_file)
tasks = TodoTasks(db_file)
