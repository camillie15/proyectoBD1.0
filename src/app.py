from flask import Flask, render_template

from conf import config

app = Flask(__name__, static_folder='static', template_folder='template')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tusEventosPage')
def tusEventosPage():
    return render_template('index1.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
