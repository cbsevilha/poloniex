import os
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    host = '0.0.0.0'
    port = int(os.environ['PORT'])
    app.run(host=host, port=port, debug=True)
