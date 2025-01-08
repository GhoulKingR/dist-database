from flask import Flask, request
import sqlite3
import sys

app = Flask(__name__)

# C []
# R []
# U []
# D []

# Get all orders
@app.get("/api/orders")
def allorders():
    conn = None
    try:
        conn = sqlite3.connect("databases/grp9order.db")
        cursor = conn.execute("SELECT * FROM GRP9ORDERS")
        result = []
        for row in cursor:
            result.append({
                "num": row[0],
                "amount": row[1],
                "advance_amount": row[2],
                "ord_date": row[3],
                "cust_code": row[4],
                "agent_code": row[5],
                "description": row[6],
            })
        return result
    
    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        err_return = {
            "error": err
        }
        return err_return, 500  # internal server error
    
    finally:
        if conn:
            conn.close()

# Get a single customer
@app.get("/api/orders/<num>")
def order(num):
    conn = None
    try:
        conn = sqlite3.connect("databases/grp9order.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9ORDERS WHERE ord_num = ?", (num,))
        row = cursor.fetchone()

        result = {}
        if row == None:
            print(f'Order {num} does not exist')

            return result, 404  # not found
        else:
            result["num"] = row[0]
            result["amount"] = row[1]
            result["advance_amount"] = row[2]
            result["ord_date"] = row[3]
            result["cust_code"] = row[4]
            result["agent_code"] = row[5]
            result["description"] = row[6]

            return result
    
    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        return {}, 500  # Internal server error
    
    finally:
        if conn:
            conn.close()

# Converting a number to agent code
# For example: '3' -> 'A003' or '3124' -> 'A3124'
def id_to_code(id):
    id = 200100 + id
    return str(id)

def count_orders(conn):
    cursor = conn.execute("SELECT * FROM GRP9ORDERS")
    count = 0
    for _ in cursor:
        count += 1
    return count

# Route to create a new document
@app.post("/api/orders")
def create_orders():
    conn = None
    try:
        conn = sqlite3.connect("databases/grp9order.db")
        json_data = request.get_json()

        if json_data:
            num = id_to_code(count_orders(conn))
            conn.execute(
                "INSERT INTO GRP9ORDERS VALUES (?, ?, ?, ?, ?, ?, ?)",
                (num, json_data["amount"], json_data["advance_amount"], json_data["ord_date"], json_data["cust_code"], json_data["agent_code"], json_data["description"])
            )
            conn.commit()
            json_data["num"] = num

            return json_data
        else:
            return json_data, 400   # Bad request
    
    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        return {}, 500  # internal server error

    except KeyError as err:
        print("Key error: err")
        return {}, 400  # Bad request
    
    finally:
        if conn:
            conn.close()

# Route to delete a document
@app.delete("/api/orders/<num>")
def del_orders(num):
    conn = None
    try:
        conn = sqlite3.connect("databases/grp9order.db")
        
        # Get item to be deleted
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9ORDERS WHERE ord_num = ?", (num,))
        row = cursor.fetchone()

        result = {}
        if row == None:
            print(f'Order {num} does not exist')

            return result, 404  # not found
        else:
            result["num"] = row[0]
            result["amount"] = row[1]
            result["advance_amount"] = row[2]
            result["ord_date"] = row[3]
            result["cust_code"] = row[4]
            result["agent_code"] = row[5]
            result["description"] = row[6]

            conn.execute("DELETE FROM GRP9ORDERS WHERE ord_num = ?", (num,))
            conn.commit()

            return result
    
    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        return {}, 500  # Internal server error
    
    finally:
        if conn:
            conn.close()

# Route to update a document
@app.put("/api/orders/<num>")
def update_customer(num):
    conn = None
    try:
        conn = sqlite3.connect("databases/grp9order.db")
        
        # Get item to be update
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9ORDERS WHERE ord_num = ?", (num,))
        row = cursor.fetchone()

        json_data = request.get_json()
        if json_data:
            new_version = {}

            if row == None:
                print(f'Order {num} does not exist')

                return new_version, 404  # not found
            else:
                new_version["num"] = row[0],
                new_version["amount"] = row[1],
                new_version["advance_amount"] = row[2],
                new_version["ord_date"] = row[3],
                new_version["cust_code"] = row[4],
                new_version["agent_code"] = row[5],
                new_version["description"] = row[6],

                accepted = {
                    'amount': 'ord_amount',
                    'advance_amount': 'advance_amount',
                    'ord_date': 'ord_date',
                    'cust_code': 'cust_code',
                    'agent_code': 'agent_code',
                    'description': 'description',
                }

                for key in json_data.keys():
                    new_version[key] = json_data[key]

                    if key not in accepted:
                        return {}, 400      # Bad request
                    
                    sql_key = accepted[key]
                    conn.execute(f"UPDATE GRP9ORDERS set {sql_key} = ? WHERE ord_num = ?", (json_data[key], num))

                conn.commit()
                return new_version
            
        else:
            return json_data, 400   # Bad request
    
    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        return {}, 500  # Internal server error
    
    finally:
        if conn:
            conn.close()

def create_app():
    return app

if __name__ == "__main__":
    try:
        try:
            port = int(sys.argv[1])
        except KeyError:
            port = 8080

        app.run(port=port, debug=True)
    
    except KeyboardInterrupt:
        print("Exitting gracefully")
