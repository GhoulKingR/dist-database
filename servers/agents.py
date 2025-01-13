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

# Get all agents
@app.get("/api/agents")
def allagents():
    try:
        conn = sqlite3.connect("databases/grp9agents.db")
        cursor = conn.execute("SELECT * FROM GRP9AGENTS")
        result = []
        for row in cursor:
            result.append({
                "code": row[0],
                "name": row[1],
                "working_area": row[2],
                "commission": row[3],
                "phone_no": row[4],
                "country": row[5]
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
            print("Sqlite3 connection closed")

# Get a single agent
@app.get("/api/agents/<code>")
def agent(code):
    try:
        conn = sqlite3.connect("databases/grp9agents.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9AGENTS WHERE agent_code = ?", (code,))
        row = cursor.fetchone()

        result = {}
        if row == None:
            print(f'Agent with code "{code}" doesn\'t exist')

            return result, 404  # not found
        else:
            result["code"] = row[0]
            result["name"] = row[1]
            result["working_area"] = row[2]
            result["commission"] = row[3]
            result["phone_no"] = row[4]
            result["country"] = row[5]
            return result
    
    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        return {}, 500  # Internal server error
    
    finally:
        if conn:
            conn.close()
            print("Sqlite3 connection closed")

# Converting a number to agent code
# For example: '3' -> 'A003' or '3124' -> 'A3124'
def id_to_code(id):
    id = str(id)
    count = len(id)
    if count < 3:
        return 'A' + ('0' * (3 - count)) + id
    
    return 'A' + id

def count_agents(conn):
    cursor = conn.execute("SELECT * FROM GRP9AGENTS")
    count = 0
    for _ in cursor:
        count += 1
    return count

# Route to create a new document
@app.post("/api/agents")
def create_agent():
    try:
        conn = sqlite3.connect("databases/grp9agents.db")
        count = count_agents(conn)
        
        json_data = request.get_json()
        if json_data:
            code = id_to_code(count + 1)
            conn.execute(
                "INSERT INTO GRP9AGENTS VALUES (?, ?, ?, ?, ?, ?)",
                (code, json_data["name"], json_data["working_area"], json_data["commission"], json_data["phone_no"], json_data["country"])
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
            print("Sqlite3 connection closed")

# Route to delete a document
@app.delete("/api/agents/<code>")
def del_agent(code):
    try:
        conn = sqlite3.connect("databases/grp9agents.db")
        
        # Get item to be deleted
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9AGENTS WHERE agent_code = ?", (code,))
        row = cursor.fetchone()

        result = {}
        if row == None:
            print(f'Agent with code "{code}" doesn\'t exist')

            return result, 404  # not found
        else:
            result["code"] = row[0]
            result["name"] = row[1]
            result["working_area"] = row[2]
            result["commission"] = row[3]
            result["phone_no"] = row[4]
            result["country"] = row[5]

            conn.execute("DELETE FROM GRP9AGENTS WHERE agent_code = ?", (code,))
            conn.commit()

            return result
    
    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        return {}, 500  # Internal server error
    
    finally:
        if conn:
            conn.close()
            print("Sqlite3 connection closed")

# Route to update a document
@app.put("/api/agents/<code>")
def update_agent(code):
    try:
        conn = sqlite3.connect("databases/grp9agents.db")
        
        # Get item to be update
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9AGENTS WHERE agent_code = ?", (code,))
        row = cursor.fetchone()

        json_data = request.get_json()
        if json_data:
            new_version = {}

            if row == None:
                print(f'Agent with code "{code}" doesn\'t exist')

                return new_version, 404  # not found
            else:
                new_version["code"] = row[0]
                new_version["name"] = row[1]
                new_version["working_area"] = row[2]
                new_version["commission"] = row[3]
                new_version["phone_no"] = row[4]
                new_version["country"] = row[5]

                for key in json_data.keys():
                    new_version[key] = json_data[key]

                    if key not in ['name', 'working_area', 'commission', 'phone_no', 'country']:
                        return {}, 400      # Bad request
                    
                    sql_key = 'agent_name' if key == 'name' else key
                    
                    conn.execute(f"UPDATE GRP9AGENTS set {sql_key} = ? WHERE agent_code = ?", (json_data[key], code))

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
            print("Sqlite3 connection closed")

def create_app():
    return app

if __name__ == "__main__":
    try:
        try:
            port = int(sys.argv[1])
        except IndexError:
            port = 8081

        app.run(port=port, debug=True)
    
    except KeyboardInterrupt:
        print("Exitting gracefully")
