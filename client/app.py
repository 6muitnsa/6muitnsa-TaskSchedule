from flask import Flask
from flask_cors import CORS
from .api import sync

app = Flask(__name__)
CORS(app)

# 注册蓝图
app.register_blueprint(sync.bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=3000) 