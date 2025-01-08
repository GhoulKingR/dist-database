# Distributed database project
This is a group project on building a distributed database server. Currently the project's architecture is as follows:
- Three servers that each host a table of a database
- A central server where the client application will be

The three servers in the project serve as REST APIs for the order, agents, and customer databases, allowing the central server to interact with with the databases.

## Setting up
Before running the servers in this project you need to have the following installed on your system:
- Python 3
- virtual environment (optional but Recommended)

Run this command to instsall the project's dependencies:
```bash
pip install -r requirements.txt
```

## Running
To run the servers, run these commands:
* Agents
```bash
python3 agent.py 8080   # to run the server on port 8080, or
python3 agent.py        # defaults to 8081
```
* Customers
```bash
python3 customer.py 8080   # to run the server on port 8080, or
python3 customer.py        # defaults to 8080
```
* Orders
```bash
python3 orders.py 8080   # to run the server on port 8080, or
python3 orders.py        # defaults to 8080
```

## Testing
All test files are located in the `test` folder to keep test files away from the server code.

This project uses pytest for testing. So you need to use this command to run all the tests:
```bash
PYTHONPATH=. pytest
```

I included an `initdb` file to make resetting the database files easier. To reset the database files, make `initdb` executable, and then run it in the terminal:
```bash
chmod +x initdb
./initdb
```

I also included a `test` file to make running tests easier. If you take a look at its contents:
```bash
#!/usr/bin/env bash
./initdb
PYTHONPATH=. pytest
```
, you'll notice that it calls the initdb file and then runs the tests. To run it, you also need to make the file executable and run it in the terminal:
```bash
chmod +x test
./test
```
