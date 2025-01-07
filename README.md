# Distributed database project

## Setting up
To run this project you need to have the following installed:
- Python 3
- virtual environment (optional but Recommended)

Run this command to instsall this project's dependencies:
```bash
$ pip install -r requirements.txt
```

## How to run
In this project I plan to have four major python servers. Three for each databases and a central server. Currently there's only one server implemented, the agents server. To run this server, use any of these commands:
```bash
python3 agent.py 8080   # to run the server on port 8080
python3 agent.py        # defaults to 8081
```

# Tests
All test files are located in the `test` folder to keep test files away from the server code.

This project uses pytest for testing. So you need to use this command to run all the tests:
```bash
PYTHONPATH=. pytest
```

I also included an `initdb` file to make resetting the database files easier. To reset the database files, make `initdb` executable, and then run it in the terminal:
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