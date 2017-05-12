from flask import Blueprint

from ares.db.mysql_db import get_cursor, get_data_connection
from base import restful_request, login_required

company_api = Blueprint('company', __name__)


@company_api.route('/company/all', methods=['GET'])
@restful_request
@login_required
def company_all(user_id, offset=0, page_size=10):
    offset = int(offset)
    page_size = int(page_size)
    cursor = get_cursor()
    cursor.execute('select * from CompanyInfo limit {} offset {}'.format(page_size, offset))

    results = []
    for data in cursor:
        results.append(dict(zip(cursor.column_names, data)))

    cursor.close()
    return results


def transform(val):
    if val == 'name':
        return 'CompanyName'
    if val == 'address':
        return 'RegisterLocation'
    return val


@company_api.route('/company/query', methods=['GET'])
@restful_request
@login_required
def company_query(user_id, offset=0, page_size=10, orders='', name='', people='', address='', constructor='',
                  executive='', manager='', supervisor='', type='', level='', location='', funding=''):
    where = []
    if name:
        where.append(u"CompanyName like '%{}%'".format(name))
    if people:
        where.append(u"LegalRepresentative like '%{}%'".format(people))
    if address:
        where.append(u"OperatingLocation like '%{}%'".format(address))
    if type:
        where.append(u"CompanyType like '%{}%'".format(type))
    if location:
        where.append(u"RegisterLocation like '%{}%'".format(location))

    where = u'where {}'.format(' and '.join(where)) if where else ''
    order = [transform(o[1:]) + " desc" if o.startswith('~') else transform(o) for o in
             orders.split(',')] if orders else None
    order = 'order by {}'.format(', '.join(order)) if order else ''
    offset = int(offset)
    page_size = int(page_size)
    connection = get_data_connection()
    cursor = connection.cursor()
    sql = u'select * from CompanyInfo {} {} limit {} offset {}'.format(where, order, page_size, offset)
    print sql
    cursor.execute(sql)

    results = []
    for data in cursor:
        results.append(dict(zip(cursor.column_names, data)))

    for company in results:
        sql = u'select * from CompanyCert where CompanyID = {}'.format(company['ID']);
        print sql
        cursor.execute(sql)
        company['CompanyCerts'] = []
        for cert in cursor.fetchall():
            company['CompanyCerts'].append(dict(zip(cursor.column_names, cert)))
        sql = u'select * from RegisteredStaff where CompanyId = {}'.format(company['ID'])
        print sql
        cursor.execute(sql)
        company['Staffs'] = []
        for data in cursor.fetchall():
            company['Staffs'].append(dict(zip(cursor.column_names, data)))
    cursor.close()
    connection.close()
    return results
