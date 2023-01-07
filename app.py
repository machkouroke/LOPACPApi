import os

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
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
        img = request.files["img"]
        img_path = "static/images/" + img.filename
        img.save(img_path)
        return "static\\images\\" + img.filename, img_path

    def predict(img_path):
        img = cv2.imread(img_path)
        result = model.predict(img)
        return np.argmax(result)

    @app.route('/prediction', methods=['POST'])
    def get_prediction():
        path, img_path = upload()
        result = predict(path)
        return jsonify({
            'success': True,
            'result': result
        })

    @app.route('/')
    def hello_world():  # put application's code here
        return 'Hello World!'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
