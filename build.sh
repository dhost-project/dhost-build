#!/bin/bash

# Create virtual environement if not set
if [[ -d "venv" ]]
then
	echo "========================"
	echo "virtualenv already exist"
	echo "========================"
else
	echo "=================="
	echo "virtualenv created"
	echo "=================="
	virtualenv venv
fi

# Source the virtual environnement
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

