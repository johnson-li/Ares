from flask import Blueprint

from ares.db.mysql_db import get_data_connection
from base import restful_request, login_required

staff_api = Blueprint('staff', __name__)


def transform(val):
    if val == 'name':
        return 'Name'
    return val


@staff_api.route('/staff/query', methods=['GET'])
@restful_request
@login_required
def staff_query(user_id, offset=0, page_size=10, orders='', name='', company='', registrationId='', id='',
                gender='', type=''):
    where = []
    if name:
        where.append(u"Name like '%{}%'".format(name))
    if id:
        where.append(u"IdentityID like '%{}%'".format(id))
    if gender:
        where.append(u"Gender like '%{}%'".format(gender))
    if type:
        where.append(u"RegisterType like '%{}%'".format(type))
    if registrationId:
        where.append(u"SealID like '%{}%'".format(registrationId))
    if company:
        where.append(u"CompanyName like '%{}%'".format(company))
    where = u'where {}'.format(' and '.join(where)) if where else ''
    order = [transform(o[1:]) + " desc" if o.startswith('~') else transform(o) for o in
             orders.split(',')] if orders else None
    order = 'order by {}'.format(', '.join(order)) if order else ''
    offset = int(offset)
    page_size = int(page_size)
    connection = get_data_connection()
    cursor = connection.cursor()
    sql = u'select * from RegisteredStaff inner join CompanyInfo on RegisteredStaff.CompanyID = CompanyInfo.ID {} {} ' \
          u'limit {} offset {}'.format(where, order, page_size, offset)
    print sql
    cursor.execute(sql)

    results = []
    for data in cursor:
        staff = dict(zip(cursor.column_names, data))
        results.append(staff)
    for staff in results:
        company_sql = "select * from CompanyInfo where id = '{}'".format(staff['CompanyID'])
        cursor.execute(company_sql)
        companies = cursor.fetchall()
        staff['Company'] = dict(zip(cursor.column_names, companies[0])) if companies else None
        certs_sql = u'select * from StaffCert where StaffID = {}'.format(staff['ID'])
        cursor.execute(certs_sql)
        certs = cursor.fetchall()
        staff['StaffCerts'] = [dict(zip(cursor.column_names, cert)) for cert in certs] if certs else []
        achievement_sql = u'select * from StaffAchievement where StaffID = {}'.format(staff['ID'])
        cursor.execute(achievement_sql)
        achievements = cursor.fetchall()
        staff['StaffAchievements'] = [dict(zip(cursor.column_names, achievement)) for achievement in
                                      achievements] if achievements else []

    cursor.close()
    connection.close()
    return results
