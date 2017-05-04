import hashlib
import uuid

from flask import Blueprint

from ares.db.mysql_db import get_connection
from base import restful_request

user_api = Blueprint('user', __name__)


@user_api.route('/user/login', methods=['GET'])
@restful_request
def user_login(email, password):
    m = hashlib.md5()
    m.update(password)
    hashed = m.hexdigest()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select * from User where email = '{}' and password = '{}'".format(email, hashed))
    users = cursor.fetchall()
    user = dict(zip(cursor.column_names, users[0])) if len(users) > 0 else None
    if user:
        token = '{}:{}'.format(user['ID'], uuid.uuid4())
        user['Token'] = token
        cursor.execute("update User set Token = '{}' where ID = {}".format(token, user['ID']))
        connection.commit()
    cursor.close()
    connection.close()
    if user:
        user.pop('Password', None)
    return {'user': user}
