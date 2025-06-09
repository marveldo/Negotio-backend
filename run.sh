#!/bin/sh
python management.py makemigrations
python management.py runserver 0.0.0.0 8000