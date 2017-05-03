import mysql.connector as connector

from ares.config import get_config

print 'connecting to mysql'
cnx = connector.connect(user=get_config('user'), password=get_config('password'),
                        host=get_config('host'), database=get_config('database'))
print 'connected to mysql'


def get_cursor():
    return cnx.cursor()
