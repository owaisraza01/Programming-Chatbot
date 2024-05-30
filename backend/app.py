from flask import Flask
from api_v1 import blueprint as api_v1
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.register_blueprint(api_v1)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')