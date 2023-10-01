import datetime
from flask import Flask, request, jsonify
import sqlite3
import collections

app = Flask(__name__)

def db_connection():
    """
    Establishes a connection to the SQLite database.

    :return: connection object if successful, None otherwise
    """
    conn = None
    try:
        conn = sqlite3.connect('pointsTracker.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn    

def validate_input(data, route):
    """
    Helps validate data that will be added to db

    :return: if data and format is of acceptable nature
    """
    if route == 'add':
        if not all(key in data for key in ["payer", "points", "timestamp"]):
            return False, "Missing required field(s)."

        payer = data["payer"]
        if not payer or not isinstance(payer, str) or len(payer.strip()) == 0:
            return False, "Invalid payer value."

        points = data["points"]
        try:
            int(points)
        except (ValueError, TypeError):
            return False, "Points must be an integer."

        timestamp = data["timestamp"]
        try:
            datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return False, "Invalid timestamp format."

        return True, ""

    elif route == 'spend':
        if "points" not in data:
            return False, "Missing required field(s)."
        points = data["points"]
        try:
            int(points)
        except (ValueError, TypeError):
            return False, "Points must be an integer."
        return True, ""



@app.route('/add', methods=['POST'])
def addPoints():
    """
    Adds new transaction to database.
    """
    conn = db_connection()
    cursor = conn.cursor()
    valid, message = validate_input(request.form, 'add')
    if not valid:
        return jsonify({"error": message}), 400
    payer = request.form['payer']
    points = int(request.form['points'])
    timestamp = request.form['timestamp']

    try:
        sql = """INSERT INTO transactions (payer, points, timestamp)
                VALUES (?,?,?)"""
        cursor.execute(sql, (payer, points, timestamp))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        return jsonify({"error": "Database error occurred."}), 500
    finally:
        conn.close()

    return "", 200

@app.route('/spend', methods= ['POST'])
def spendPoints():
    """
    Manages spend request following the specified rules.
    Creates a new transaction of negative value when points are spent.

    :return: json of amount of points detected and from which payer
    """
    conn = db_connection()
    cursor = conn.cursor()

    valid, message = validate_input(request.form, 'spend')
    if not valid:
        return jsonify({"error": message}), 400

    try:
        points = int(request.form['points'])
        transactions = cursor.execute("""
            SELECT payer, points, timestamp, transaction_id
            FROM transactions
            ORDER BY timestamp ASC, transaction_id ASC
        """).fetchall()

        total_points_by_payer = collections.defaultdict(int)
        ret_val = collections.defaultdict(int)

        for transaction in transactions:
            total_points_by_payer[transaction[0]] += transaction[1]

        # First, check if the user has enough points
        if sum(total_points_by_payer.values()) < points:
            return jsonify({"error": "user does not have enough points"}), 400

        for transaction in transactions:
            payer = transaction[0]
            current_points = transaction[1]
            transaction_id = transaction[3]

            if current_points <= points:
                ret_val[payer] -= current_points
                total_points_by_payer[payer] -= current_points
                points -= current_points
            else:
                ret_val[payer] -= points
                total_points_by_payer[payer] -= points
                points = 0

            if points == 0:
                break
        
        for key, value in ret_val.items():
            # Record spending transactions of payers
            cursor.execute("""INSERT INTO transactions (payer, points, timestamp)
                VALUES (?,?,?)""", (key, value, datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')))
        
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        return jsonify({"error": "Database error occurred."}), 500
    finally:
        conn.close()

    return jsonify(ret_val)

@app.route('/balance', methods= ['GET'])
def getBalance():
    """
    Gets balances of payers.

    :return: json of amount of points for every payer in system
    """
    conn = db_connection()
    cursor = conn.cursor()
    ret_val = collections.defaultdict(int)

    try:
        transactions = cursor.execute("""
            SELECT payer, points
            FROM transactions
        """).fetchall()
        for transaction in transactions:
            payer = transaction[0]
            points = transaction[1]
            ret_val[payer] += points
    except sqlite3.Error as e:
        print(e)
        return jsonify({"error": "Database error occurred."}), 500
    finally:
        conn.close()

    return jsonify(ret_val)

if __name__ == '__main__':
    app.run()
