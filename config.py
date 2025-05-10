"""
HOST='localhost'
USER='root'
NAME='ev5'
PASSWORD=''
REDIS='redis://localhost:6379/0'
"""

#? Liara DB:
# HOST='evaam-database'
# USER='root'
# NAME='nice_borg'
# PASSWORD='2N1UYN7tvG3bWhayTuWUyHM2' 
# REDIS="r"

"""
JIBIT_API_KEY="cvYDi4nzvP"
JIBIT_SECRET_KEY="5Ioyhh9MDbjA19_JQi16CJWI9"

"""
#? e-vaam test db:
# HOST='localhost'
# USER=''
# NAME=''
# PASSWORD=''
# # REDIS="redis://:4yYeWoUuVc8Gyn7QaL6RotfQ@redis:6379/0"
# CELERY_BACKEND = ''
# CELERY_BROKER_URL = ''
# CELERY_RESULT_BACKEND = ''


import os

HOST = os.getenv("DB_HOST", "localhost")
USER = os.getenv("DB_USER", "epaal_user")
NAME = os.getenv("DB_NAME", "epaal_db")
PASSWORD = os.getenv("DB_PASSWORD", "")
PORT = os.getenv("DB_PORT", "5432")

REDIS = os.getenv("REDIS_URL", "redis://localhost:6379/0")

JIBIT_API_KEY = os.getenv("JIBIT_API_KEY", "")
JIBIT_SECRET_KEY = os.getenv("JIBIT_SECRET_KEY", "")
