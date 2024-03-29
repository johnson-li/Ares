from flask import Flask
from flask_compress import Compress

from api.company import company_api
from api.company_like import company_like_api
from api.project import project_api
from api.staff import staff_api
from api.user import user_api

app = Flask(__name__)
Compress(app)

app.register_blueprint(company_api)
app.register_blueprint(user_api)
app.register_blueprint(staff_api)
app.register_blueprint(project_api)
app.register_blueprint(company_like_api)


def main():
    app.run(host='0.0.0.0', port=5123)


if __name__ == '__main__':
    main()
