#!/usr/bin/env python3

import os
import sys
import pymysql
from flask import Flask, g, render_template, request, jsonify

# Define constants for configuration
DATABASE_HOST = "localhost"
DATABASE_USER = "root"
DATABASE_PASSWORD = "root"
DATABASE_NAME = "hw5_ex2"
DEFAULT_LIMIT = 100

# Define the Flask app and configuration
app = Flask(__name__)
app.config.from_mapping(
    DATABASE_HOST=DATABASE_HOST,
    DATABASE_USER=DATABASE_USER,
    DATABASE_PASSWORD=DATABASE_PASSWORD,
    DATABASE_NAME=DATABASE_NAME,
)

# Connect to the database when the app is started
def connect_db():
    if "db" not in g:
        g.db = pymysql.connect(
            host=app.config["DATABASE_HOST"],
            user=app.config["DATABASE_USER"],
            password=app.config["DATABASE_PASSWORD"],
            db=app.config["DATABASE_NAME"],
            cursorclass=pymysql.cursors.DictCursor,
        )
    return g.db

# Disconnect from the database when the app is stopped
@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Endpoint for retrieving messages
@app.route("/messages", methods=["GET", "POST"])
def messages():
    db = connect_db()

    with db.cursor() as cursor:
        # Create the base SQL query
        sql = "SELECT DISTINCT name, message FROM messages"

        if request.method == "POST":
            # Check if the name parameter is provided
            name = request.form.get("name")
            if not name:
                return "Invalid input", 500

            # Add the name to the query
            sql += " WHERE name = %s"
            cursor.execute(sql, name)
        else:
            # Make the query without any parameters
            cursor.execute(sql)

        # Get the results and return them as JSON
        rows = cursor.fetchall()
        return jsonify(rows)

# Endpoint for retrieving users
@app.route("/users")
def users():
    db = connect_db()

    with db.cursor() as cursor:
        # Create the base SQL query
        sql = "SELECT DISTINCT name FROM users"

        # Get the limit from the URL parameters
        limit = request.args.get("limit", DEFAULT_LIMIT)

        # Try to parse the limit as an integer
        try:
            limit = int(limit)
        except ValueError:
            return "Invalid input", 500

        if limit <= 0:
            return "Invalid input", 500

        # Add the LIMIT clause to the query
        sql += f" LIMIT {limit}"

        # Execute the query and get the results
        cursor.execute(sql)
        results = cursor.fetchall()

        # Extract the user names from the results and return them as JSON
        users = [result["name"] for result in results]
        return jsonify({"users": users})

# Populate the database and start the app
if __name__ == "__main__":
    seed = "randomseed"
    if len(sys.argv) == 2:
        seed = sys.argv[1]

    with app.app_context():
        db = connect_db()
        populate.populate_db(seed, db.cursor())
        db.commit()
        print("[+] database populated")

    app.run(host="0.0.0.0", port=80)
