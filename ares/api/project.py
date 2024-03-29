from flask import Blueprint

from ares.db.mysql_db import get_data_connection
from base import restful_request, login_required

project_api = Blueprint('project', __name__)


def transform(val):
    if val == 'name':
        return 'Name'
    return val


@project_api.route('/project/query', methods=['GET'])
@restful_request
@login_required
def project_query(user_id, offset=0, page_size=10, orders='', name='', company='', staff='', location='', price='',
                  projectType='', projectTime='', source='', judge=''):
    where = []
    if name:
        where.append(u"Name like '%{}%'".format(name))
    if projectType:
        where.append(u"ProjectType like '%{}%'".format(projectType))
    if location:
        where.append(u"Location like '%{}%'".format(location))
    if company:
        where.append(u"CompanyName like '%{}%'".format(company))
    if price:
        where.append(u"BinddingPrice = {}".format(price))
    if projectTime:
        where.append(u"BiddingFinishDate like '%{}%'".format(projectTime))

    where = u'where {}'.format(' and '.join(where)) if where else ''
    order = [transform(o[1:]) + " desc" if o.startswith('~') else transform(o) for o in
             orders.split(',')] if orders else None
    order = 'order by {}'.format(', '.join(order)) if order else ''
    offset = int(offset)
    page_size = int(page_size)
    connection = get_data_connection()
    cursor = connection.cursor()
    sql = u'select * from Project inner join CompanyInfo on Project.CompanyID = CompanyInfo.ID {} {} ' \
          u'limit {} offset {}'.format(where, order, page_size, offset)
    print sql
    cursor.execute(sql)

    results = []
    for data in cursor:
        results.append(dict(zip(cursor.column_names, data)))
    for project in results:
        sql = u'select * from CompanyInfo where ID = {}'.format(project['CompanyID'])
        print sql
        cursor.execute(sql)
        companies = cursor.fetchall()
        project['Company'] = dict(zip(cursor.column_names, companies[0])) if companies else None
    cursor.close()
    connection.close()
    return results
