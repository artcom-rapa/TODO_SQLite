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
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)

    def all_projects(self):
        self.cur.execute(f"SELECT * FROM projects")
        return self.cur.fetchall()

    def create_project(self, data):
        """
        Create a new project into the projects table
        :param data:
        :return: project id
        """
        sql = '''INSERT INTO projects(name, start_date, end_date, status)
                 VALUES(?,?,?,?)'''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid

    def get_projects(self, id):

        self.cur.execute(f"SELECT * FROM projects WHERE id = {id}")
        return self.cur.fetchone()

    def get_tasks(self, id):

        self.cur.execute(f"SELECT * FROM tasks WHERE project_id = {id}")
        return self.cur.fetchall()

    def update(self, id, data):
        sql = f''' UPDATE projects
                    SET name = ?, start_date = ?, end_date = ?, status = ?
                    WHERE id = {id}'''
        print(sql)

        try:
            self.cur.execute(sql, data)
            self.conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)


class TodoTasks:
    def __init__(self, db_file):
        """ create a database connection to the SQLite database
        specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
            self.cur = self.conn.cursor()

        except sqlite3.Error as e:
            print(e)

    def all_tasks(self):
        self.cur.execute(f"SELECT * FROM tasks")
        return self.cur.fetchall()

    def create_task(self, data):
        """
        Create a new zadanie into the tasks table
        :param zadanie:
        :return: zadanie id
        """

        sql = '''INSERT INTO tasks(project_id, name, description, start_date, end_date)
                     VALUES(?,?,?,?,?)'''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid

    def get_tasks(self, id):

        self.cur.execute(f"SELECT * FROM tasks WHERE id = {id} ")
        return self.cur.fetchone()

    def update(self, id, data):
        sql = f''' UPDATE tasks
                    SET project_id = ?, name = ?, description = ?, start_date = ?, end_date = ?
                    WHERE id = {id} '''
        try:
            self.cur.execute(sql, data)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(e)


db_file = "database.db"
projects = TodoProjects(db_file)
tasks = TodoTasks(db_file)
