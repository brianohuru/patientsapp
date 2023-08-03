import sqlite3


class DbConnection:
    @staticmethod
    def insertQuery(query):
        conn = sqlite3.connect("db.db")
        cursor = conn.execute(query)
        conn.commit()
        lastrowid = cursor.lastrowid
        conn.close()
        return lastrowid

    @staticmethod
    def selectQuery(query):
        conn = sqlite3.connect("db.db")
        cursor = conn.execute(query)
        response = []
        for row in cursor:
            response.append(row)
        conn.close()
        return response
