from flask import Flask, render_template

from utils import socketio

import barrage.views as barrage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fun'

app.register_blueprint(barrage.blueprint, url_prefix='/barrage')

socketio.init_app(app)


@app.route('/')
def index_method():
	return render_template('index.html')


@app.route('/test')
def test_method():
	return render_template('test.html')


if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=8844)
