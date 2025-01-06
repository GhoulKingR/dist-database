from flask import Flask
import sqlite3

app = Flask(__name__)

# C
# R [x]
# U
# D

@app.get("/api/agents")
def allagents():
    result = []
    try:
        conn = sqlite3.connect("databases/grp9agents.db")
        cursor = conn.execute("SELECT * FROM GRP9AGENTS")
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
        return err_return, 500
    
    finally:
        if conn:
            conn.close()
            print("Sqlite3 connection closed")

@app.get("/api/agents/<code>")
def agent(code):
    result = {}
    try:
        conn = sqlite3.connect("databases/grp9agents.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRP9AGENTS WHERE agent_code = ?", (code,))
        row = cursor.fetchone()

        if row == None:
            print(f'Agent with code "{code}" doesn\'t exist')

            return result, 404
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
        return {}, 500
    
    finally:
        if conn:
            conn.close()
            print("Sqlite3 connection closed")

def create_app():
    global app
    return app

if __name__ == "__main__":
    try:
        app.run(port=8081, debug=True)
    
    except KeyboardInterrupt:
        print("Exitting gracefully")