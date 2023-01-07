from flask import Flask
from flask_cors import CORS
import shelve

model = shelve.open('model.h5')


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    def upload():
        pass

    @app.route('/')
    def hello_world():  # put application's code here
        return 'Hello World!'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
