# backend

## Environment Setup

### Virtual Environment

We recommend using [virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) to manage our environment and dependencies.

To create a virtual environment, run `python3 -m venv env`. This will create the virtual environment in the `./env` directory.

To activate the virtual environment, run `source env/bin/activate`. You can confirm you’re in the virtual environment by checking the location of your Python interpreter, `which python`, which should point to the `./env` directory.

If you want to leave your virtual environment, run `deactivate`.

### Installing Dependencies

To install all the dependencies, run `python3 -m pip install -r requirements.txt`.

Make sure to update this everytime a new package is installed. You can do this by doing `pip freeze > requirements.txt`
