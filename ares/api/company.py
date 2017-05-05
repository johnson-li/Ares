from flask import Blueprint

from ares.db.mysql_db import get_cursor
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


@company_api.route('/company/query', methods=['GET'])
@restful_request
@login_required
def company_query(user_id, offset=0, page_size=10, name='', people='', address='', constructor='', executive='',
                  manager='', supervisor=''):
    where = []
    if name:
        where.append("CompanyName like '%{}%'".format(name))
    where = 'where {}'.format(' and '.join(where)) if where else ''
    offset = int(offset)
    page_size = int(page_size)
    cursor = get_cursor()
    sql = 'select * from CompanyInfo {} limit {} offset {}'.format(where, page_size, offset)
    print sql
    cursor.execute(sql)

    results = []
    for data in cursor:
        results.append(dict(zip(cursor.column_names, data)))
    cursor.close()
    return results
