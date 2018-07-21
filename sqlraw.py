#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

con = sqlite3.connect('weight_saver.db')

con.row_factory = sqlite3.Row

cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS users;")

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY autoincrement,
        name text NOT NULL,
        height float NOT NULL,
        weight float NOT NULL
    )""")

cur.executescript("""
    DROP TABLE IF EXISTS user_weight_data;
    CREATE TABLE IF NOT EXISTS user_weight_data (
        id INTEGER PRIMARY KEY autoincrement,
        date datetime NOT NULL,
        value float NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
