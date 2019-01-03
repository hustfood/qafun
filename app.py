from flask import Flask, render_template

from utils import socketio

import barrage.views as barrage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fun'

app.register_blueprint(barrage.blueprint, url_prefix='/barrage')

socketio.init_app(app, async_mode='eventlet')


@app.route('/')
def index_method():
	# return render_template('index.html')
	return render_template('qafun.html')


if __name__ == '__main__':
	socketio.run(app, port=8421)
