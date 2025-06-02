import sqlite3
from flask import flash

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    def addUser(self, username, email, password):
        try:
            self.__cur.execute(f"SELECT COUNT(email) as count FROM users WHERE email LIKE {email}")
            res = self.__cur.fetchone()
            if res[0] > 0:
                flash("User with this email already exists")
                return False
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (username, email, password))
            self.__db.commit()
        except sqlite3.Error as e:
            flash("Error adding user to database:\n" + str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                flash("User not found")
                return False
            return res
        except sqlite3.Error as e:
            flash("Error getting data from database:\n" + str(e))
        return False

    def getUserByUsername(self, username):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE username = {username} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                flash("User not found")
                return False
            return res
        except sqlite3.Error as e:
            flash("Error getting data from database:\n" + str(e))
        return False
