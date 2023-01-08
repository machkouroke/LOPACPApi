import os
from sklearn.pipeline import Pipeline
from flask import Flask, request, jsonify, abort
from error import setup_error_template
from flask_cors import CORS
import numpy as np
import imageio.v2 as io
import shelve


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    setup_error_template(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    def upload():
        file = request.files['img']

        if file:
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file.save(os.path.join('uploads', file.filename))
            img_path = f"uploads/{file.filename}"
            return img_path
        else:
            raise ValueError('No file uploaded')

    def predict(img_path, type_model):
        img = io.imread(img_path)
        with shelve.open("variables") as variables:
            model: Pipeline = variables[type_model]
            result = model.predict(img.flatten().reshape(1, -1))
        return result[0]

    @app.route('/prediction', methods=['POST'])
    def get_prediction():
        try:
            img_path = upload()
            result = predict(img_path, request.form['modelType'])
            return jsonify({
                'success': True,
                'result': result
            })
        except ValueError as e:
            abort(400, e)
        except Exception as e:
            abort(500, e)

    @app.route('/test', methods=['POST'])
    def test():
        path = upload()
        return jsonify({
            'success': True,
            'path': path
        })

    @app.route('/', methods=['Get', 'POST'])
    def hello_world():  # put application's code here
        return jsonify({
            'success': True,
            'result': "Hello World 1.0"
        })

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
