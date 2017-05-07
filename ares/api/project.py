from flask import Blueprint

from ares.db.mysql_db import get_cursor
from base import restful_request, login_required

project_api = Blueprint('project', __name__)


def transform(val):
    if val == 'name':
        return 'Name'
    return val


@project_api.route('/project/query', methods=['GET'])
@restful_request
@login_required
def staff_query(user_id, offset=0, page_size=10, orders='', name='', company='', staff='', title=''):
    where = []
    if name:
        where.append("name like '%{}%'".format(name))
    where = 'where {}'.format(' and '.join(where)) if where else ''
    order = [transform(o[1:]) + " desc" if o.startswith('~') else transform(o) for o in
             orders.split(',')] if orders else None
    order = 'order by {}'.format(', '.join(order)) if order else ''
    offset = int(offset)
    page_size = int(page_size)
    cursor = get_cursor()
    sql = 'select * from Project {} {} limit {} offset {}'.format(where, order, page_size, offset)
    print sql
    cursor.execute(sql)

    results = []
    for data in cursor:
        results.append(dict(zip(cursor.column_names, data)))
    cursor.close()
    return results
