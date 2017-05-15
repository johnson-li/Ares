import mysql.connector as connector

from ares.config import get_config

print 'connecting to mysql: app'
cnx_app = connector.connect(pool_name='app', user=get_config('user'), password=get_config('password'),
                            host=get_config('host_app'), database=get_config('database'),
                            pool_size=10)
print 'connected to mysql: app'

print 'connecting to mysql: data'
cnx_data = connector.connect(pool_name='data', user=get_config('user'), password=get_config('password'),
                             host=get_config('host_data'), database=get_config('database'),
                             pool_size=10)
print 'connected to mysql: data'


def get_app_connection():
    return connector.connect(pool_name='app')


def get_new_cursor():
    return connector.connect(pool_name='app').cursor()


def get_cursor():
    return cnx_app.cursor()


def get_data_connection():
    return connector.connect(pool_name='data')
