from flask import Blueprint

from ares.db.mysql_db import get_cursor
from base import restful_request

company_api = Blueprint('company', __name__)


@company_api.route('/company/all', methods=['GET'])
@restful_request
def company_all():
    cursor = get_cursor()
    cursor.execute('select * from CompanyInfo')

    results = []
    for data in cursor:
        results.append(dict(zip(cursor.column_names, data)))
    return results
