# HOST='localhost'
# USER='root'
# NAME='my_test3'
# PASSWORD=''
# REDIS='redis://localhost:6379/0'

#? Liara DB:
# HOST='kheilisabz-db'
# USER='root'
# NAME='naughty_ride'
# PASSWORD='IVGoiaRa2PXbQTw5atoMwGBK'
# REDIS="redis://:4yYeWoUuVc8Gyn7QaL6RotfQ@redis:6379/0"

#? kheilisabz test db:
HOST='localhost'
USER='my_test3'
NAME='my_test3'
PASSWORD='@Mp13811381'
# REDIS="redis://:4yYeWoUuVc8Gyn7QaL6RotfQ@redis:6379/0"
CELERY_BACKEND = 'redis://localhost:6379/3'
CELERY_BROKER_URL = 'redis://localhost:6379/4'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/5'