# The servers
Database servers for this project.

## Preprequisites
To be able to run the servers in this folder, you need to have Python 3 installed on your system.

## Setting up
There are three servers in this folder: `order`, `customer`, and `agents`, in the `order.py`, `customer.py`, and `agents.py` files respectively.

For the whole project to work you need to run these three servers, and before you can do that, you need to set up the environment for them to run in. This can either be your system, or in a virtual environment (the recommended way).

In your environment, install the project's dependencies with this command in your terminal: 
```bash
pip install -r requirements.txt
```

After successfully installing the dependencies, follow the next section to run the servers.

## Running
To run the servers, run these commands:
* Agents
```bash
python3 agents.py 8080   # to run the server on port 8080, or
python3 agents.py        # defaults to 8081
```
* Customer
```bash
python3 customer.py 8080   # to run the server on port 8080, or
python3 customer.py        # defaults to 8080
```
* Order
```bash
python3 order.py 8080   # to run the server on port 8080, or
python3 order.py        # defaults to 8080
```

## Testing
I also added tests to for the servers in this folder. The tests are in `tests/` directory. 

If you want to run the tests, you can run this command.
```bash
PYTHONPATH=. python -m pytest
```
> Note: This project uses Pytest for testing.

I included an `initdb` file to make resetting the database files easier, and a `test` file to make running the tests as straightforward as a single command. To run either files, you need to make them executable on your system, with these command:
```bash
chmod +x initdb
chmod +x test
```

When they're executable, you can run them in the terminal with the `./<file>` systax. For example:
- `./initdb` to execute `initdb`
- `./test` to execute `test`

