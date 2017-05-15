import hashlib
import uuid
from random import randint

from flask import Blueprint

from ares.db.mysql_db import get_app_connection
from ares.utils import send_verification_code
from base import restful_request

user_api = Blueprint('user', __name__)


@user_api.route('/user/login', methods=['GET'])
@restful_request
def user_login(email, password):
    m = hashlib.md5()
    m.update(password)
    hashed = m.hexdigest()
    connection = get_app_connection()
    cursor = connection.cursor()
    cursor.execute("select * from User where email = '{}' and password = '{}'".format(email, hashed))
    users = cursor.fetchall()
    user = dict(zip(cursor.column_names, users[0])) if len(users) > 0 else None
    if user:
        token = '{}:{}'.format(user['Email'], uuid.uuid4())
        user['Token'] = token
        cursor.execute("update User set Token = '{}' where ID = {}".format(token, user['ID']))
        connection.commit()
    cursor.close()
    connection.close()
    if user:
        user.pop('Password', None)
    return user


@user_api.route('/user/verify_email', methods=['GET'])
@restful_request
def verify_email(email):
    connection = get_app_connection()
    cursor = connection.cursor()
    sql = u"select * from Verification where `email` = '{}'".format(email)
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        code = res[2]
    else:
        code = randint(0, 999999)
        code = str(code)
        code = '0' * (6 - len(code)) + code
        sql = u"insert into Verification (`Email`, `Code`) values ('{}', '{}')".format(email, code)
        cursor.execute(sql)
        connection.commit()
    send_verification_code(email, code)
    cursor.close()
    connection.close()
    return ''


@user_api.route('/user/verify_phone', methods=['GET'])
@restful_request
def verify_phone(phone):
    raise NotImplementedError()


@user_api.route('/user/signup', methods=['GET'])
@restful_request
def signup(email, password, verification):
    connection = get_app_connection()
    cursor = connection.cursor()
    sql = u"select * from Verification where `Email` = '{}' and `Code` = '{}'".format(email, verification)
    print sql
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        pass
    else:
        raise Exception('Incorrect verification code')
    token = '{}:{}'.format(email, uuid.uuid4())
    md5 = hashlib.md5()
    md5.update(password)
    sql = u"insert into User (`Email`, `Name`, `Gender`, `Type`, `Password`, `Token`) " \
          u"VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(email, email, 'Male', 1, md5.hexdigest(), token)
    cursor.execute(sql)
    connection.commit()
    cursor.execute("select * from User where email = '{}'".format(email))
    users = cursor.fetchall()
    user = dict(zip(cursor.column_names, users[0])) if len(users) > 0 else None
    cursor.close()
    connection.close()
    return user
