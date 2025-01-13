from flask import Flask, request
from flask_cors import CORS
import sqlite3
import sys

app = Flask(__name__)
CORS(app)

# C [x]
# R [x]
# U [x]
# D [x]

# Get all customers
@app.get("/api/customers")
def allcustomers():
    try:
        conn = sqlite3.connect("databases/grp9customer.db")
        cursor = conn.execute("SELECT * FROM GRP9CUSTOMER")
        result = []
        for row in cursor:
            result.append({
                "code": row[0],
                "name": row[1],
                "city": row[2],
                "working_area": row[3],
                "country": row[4],
                "grade": row[5],
                "opening_amt": row[6],
                "receive_amt": row[7],
                "payment_amt": row[8],
                "outstanding_amt": row[9],
                "phone_no": row[10],
                "agent_code": row[11],
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
@app.get("/api/customers/<code>")
def customer(code):
    try:
        conn = sqlite3.connect("databases/grp9customer.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9CUSTOMER WHERE cust_code = ?", (code,))
        row = cursor.fetchone()

        result = {}
        if row == None:
            print(f'Customer with code "{code}" doesn\'t exist')

            return result, 404  # not found
        else:
            result["code"] = row[0]
            result["name"] = row[1]
            result["city"] = row[2]
            result["working_area"] = row[3]
            result["country"] = row[4]
            result["grade"] = row[5]
            result["opening_amt"] = row[6]
            result["receive_amt"] = row[7]
            result["payment_amt"] = row[8]
            result["outstanding_amt"] = row[9]
            result["phone_no"] = row[10]
            result["agent_code"] = row[11]
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
    id = str(id)
    count = len(id)
    if count < 5:
        return 'C' + ('0' * (5 - count)) + id
    
    return 'C' + id

def count_customers(conn):
    cursor = conn.execute("SELECT * FROM GRP9CUSTOMER")
    count = 0
    for _ in cursor:
        count += 1
    return count

# Route to create a new document
@app.post("/api/customers")
def create_customer():
    try:
        conn = sqlite3.connect("databases/grp9customer.db")
        count = count_customers(conn)
        
        json_data = request.get_json()
        if json_data:
            code = id_to_code(count + 1)
            conn.execute(
                "INSERT INTO GRP9CUSTOMER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    code, json_data["name"], json_data["city"], json_data["working_area"],
                    json_data["country"], json_data["grade"], json_data["opening_amt"], json_data["receive_amt"],
                    json_data["payment_amt"], json_data["outstanding_amt"], json_data["phone_no"], json_data["agent_code"]
                )
            )
            conn.commit()

            json_data["code"] = code
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
@app.delete("/api/customers/<code>")
def del_customer(code):
    try:
        conn = sqlite3.connect("databases/grp9customer.db")
        
        # Get item to be deleted
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9CUSTOMER WHERE cust_code = ?", (code,))
        row = cursor.fetchone()

        result = {}
        if row == None:
            print(f'Customer with code "{code}" doesn\'t exist')

            return result, 404  # not found
        else:
            result["code"] = row[0]
            result["name"] = row[1]
            result["city"] = row[2]
            result["working_area"] = row[3]
            result["country"] = row[4]
            result["grade"] = row[5]
            result["opening_amt"] = row[6]
            result["receive_amt"] = row[7]
            result["payment_amt"] = row[8]
            result["outstanding_amt"] = row[9]
            result["phone_no"] = row[10]
            result["agent_code"] = row[11]

            conn.execute("DELETE FROM GRP9CUSTOMER WHERE cust_code = ?", (code,))
            conn.commit()

            return result
    
    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        return {}, 500  # Internal server error
    
    finally:
        if conn:
            conn.close()

# Route to update a document
@app.put("/api/customers/<code>")
def update_customer(code):
    try:
        conn = sqlite3.connect("databases/grp9customer.db")
        
        # Get item to be update
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9CUSTOMER WHERE cust_code = ?", (code,))
        row = cursor.fetchone()

        json_data = request.get_json()
        if json_data:
            new_version = {}

            if row == None:
                print(f'Customer with code "{code}" doesn\'t exist')

                return new_version, 404  # not found
            else:
                new_version["code"] = row[0]
                new_version["name"] = row[1]
                new_version["city"] = row[2]
                new_version["working_area"] = row[3]
                new_version["country"] = row[4]
                new_version["grade"] = row[5]
                new_version["opening_amt"] = row[6]
                new_version["receive_amt"] = row[7]
                new_version["payment_amt"] = row[8]
                new_version["outstanding_amt"] = row[9]
                new_version["phone_no"] = row[10]
                new_version["agent_code"] = row[11]

                accepted = {
                    'name': 'cust_name',
                    'city': 'cust_city',
                    'working_area': 'working_area',
                    'country': 'cust_country',
                    'grade': 'grade',
                    'opening_amt': 'opening_amt',
                    'receive_amt': 'receive_amt',
                    'payment_amt': 'payment_amt',
                    'outstanding_amt': 'outstanding_amt',
                    'phone_no': 'phone_no',
                    'agent_code': 'agent_code'
                }

                for key in json_data.keys():
                    new_version[key] = json_data[key]

                    if key not in accepted:
                        return {}, 400      # Bad request
                    
                    sql_key = accepted[key]
                    conn.execute(f"UPDATE GRP9CUSTOMER set {sql_key} = ? WHERE cust_code = ?", (json_data[key], code))

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
        except IndexError:
            port = 8082

        app.run(port=port, debug=True)
    
    except KeyboardInterrupt:
        print("Exitting gracefully")
