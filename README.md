# BAKERY MANAGEMENT SYSTEM

## Prerequisite
Your system must have installed python3.

If not, please [Install Python](https://www.python.org/downloads/).


## Installation

It is best to use the python `virtualenv` tool to build locally:

```sh
$ sudo apt install python3-pip
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```
