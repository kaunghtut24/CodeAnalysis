
from flask import Flask
from api_routes import api

app = Flask(__name__)
app.register_blueprint(api)

@app.route('/')
def index():
    return "Code Analysis Service Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
