from flask import Blueprint

from ares.db.mysql_db import get_cursor
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
        where.append(u"name like '%{}%'".format(name))
    if id:
        where.append(u"identityId like '%{}%'".format(id))
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
    cursor = get_cursor()
    sql = u'select * from Staff inner join CompanyInfo on Staff.CompanyID = CompanyInfo.ID {} {} limit {} offset {}'.format(
        where, order, page_size, offset)
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

    cursor.close()
    return results
