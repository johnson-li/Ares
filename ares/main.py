from flask import Flask
from flask_compress import Compress

from api.company import company_api

app = Flask(__name__)
Compress(app)

app.register_blueprint(company_api)


def main():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()