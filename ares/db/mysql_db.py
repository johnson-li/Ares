import mysql.connector as connector

from ares.config import get_config

print 'connecting to mysql'
cnx = connector.connect(pool_name='pool1', user=get_config('user'), password=get_config('password'),
                        host=get_config('host'), database=get_config('database'),
                        pool_size=5)
print 'connected to mysql'


def get_connection():
    return connector.connect(pool_name='pool1')


def get_new_cursor():
    return connector.connect(pool_name='pool1').cursor()


def get_cursor():
    return cnx.cursor()
