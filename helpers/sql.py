"""
MIT License

Copyright (c) 2021 Tinura Dinith

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import threading
from sqlalchemy import create_engine, Column, Numeric, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from config import SQL_DB

def start() -> scoped_session:
    engine = create_engine(SQL_DB, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

BASE = declarative_base()
SESSION = start()
INSERTION_LOCK = threading.RLock()

class Users(BASE):
    __tablename__ = "uptodate"
    id = Column(Numeric, primary_key=True)
    user_name = Column(TEXT)

    def __init__(self, id, user_name):
        self.id = id
        self.user_name = user_name

Users.__table__.create(checkfirst=True)

def add_user(id, user_name):
    with INSERTION_LOCK:
        user = SESSION.query(Users).get(id)
        if not user:
            usr = Users(id, user_name)
            SESSION.add(usr)
            SESSION.commit()
        else:
            pass

def remove_user(id):
    with INSERTION_LOCK:
        user = SESSION.query(Users).get(id)
        if user:
            SESSION.delete(user)
            SESSION.commit()
        else:
            SESSION.close()

def count_users():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()

def user_list():
    try:
        query = SESSION.query(Users.id).order_by(Users.id)
        return query
    finally:
        SESSION.close()