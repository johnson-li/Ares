from flask import Blueprint

from ares.db.mysql_db import get_app_connection
from base import restful_request, login_required

company_like_api = Blueprint('company_like', __name__)


@company_like_api.route('/company_like/query')
@restful_request
@login_required
def company_like_query(user_id, company_id):
    connection = get_app_connection()
    cursor = connection.cursor()
    sql = u'select * from CompanyLike where UserID = {} and CompanyID = {}'.format(user_id, company_id)
    cursor.execute(sql)
    liked = True if cursor.fetchall() else False
    sql = u'select count(*) from CompanyLike where CompanyID = {}'.format(company_id)
    cursor.execute(sql)
    number = cursor.fetchone()
    cursor.close()
    connection.close()
    return {'liked': liked, 'number': number}


@company_like_api.route('/company_like/like')
@restful_request
@login_required
def company_like_like(user_id, company_id):
    connection = get_app_connection()
    cursor = connection.cursor()
    sql = u'insert into `CompanyLike` (`UserID`, `CompanyID`) values ({}, {})'.format(user_id, company_id)
    cursor.execute(sql)
    cursor.close()
    connection.commit()
    connection.close()
    return ''


@company_like_api.route('/company_like/unlike')
@restful_request
@login_required
def company_like_unlike(user_id, company_id):
    connection = get_app_connection()
    cursor = connection.cursor()
    sql = u'DELETE FROM `CompanyLike` WHERE `UserID`= {} and `CompanyID` = {}'.format(user_id, company_id)
    cursor.execute(sql)
    cursor.close()
    connection.commit()
    connection.close()
    return ''
