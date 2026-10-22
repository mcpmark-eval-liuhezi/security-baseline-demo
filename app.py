"""Deliberately insecure demo application.

WARNING: this file exists on purpose so that CodeQL code scanning has
something realistic to find. Do NOT copy any of these patterns into
production code.
"""

import sqlite3


# Hardcoded credentials -- a classic finding.
DB_PASSWORD = "hunter2-prod-password"
API_KEY = "sk-live-4f9c1d2e8b7a6f5e4d3c2b1a"


def get_user_by_email(conn, email):
    """Look up a user by email address.

    The caller-supplied value is concatenated straight into the SQL
    string, so a hostile value like `' OR '1'='1` changes the query.
    """
    query = "SELECT id, name, email FROM users WHERE email = '" + email + "'"
    return conn.execute(query).fetchall()


def login(conn, username, password):
    """Same bug, different construction: f-string interpolation."""
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return conn.execute(query).fetchone()


def delete_user(conn, user_id):
    """Same bug again, using %-formatting."""
    sql = "DELETE FROM users WHERE id = %s" % user_id
    conn.execute(sql)
    conn.commit()


def search_users(conn, name):
    """Same bug, built with str.format()."""
    sql = "SELECT * FROM users WHERE name = '{}'".format(name)
    return conn.execute(sql).fetchall()


def run_admin_expression(conn, expression):
    """Evaluates an arbitrary expression supplied by the caller."""
    return eval(expression)


def connect(db_path):
    """Opens the SQLite database (used by the demo app above)."""
    return sqlite3.connect(db_path)
