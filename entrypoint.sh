#!/bin/sh

alembic upgrade heads
python3 ./src/app/main.py