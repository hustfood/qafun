from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index_method():
	return render_template('index.html')


@app.route('/test')
def test_method():
	return render_template('test.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port='8421')
