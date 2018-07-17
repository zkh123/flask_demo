from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from os import path
from flask.ext.script import Manager


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

maneger = Manager(app)


@app.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'User %s' % user_id


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def index():
    # request.cookies['']

    return render_template('index.html', title='上海', name='ppd')


@app.route('/service')
def service():
    return 'Service'


@app.route('/about')
def about():
    return 'About'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    elif request.method == 'GET':
        username = request.args['username']
        password = request.args['password']
    return render_template('login.html', method=request.method)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath, 'static/uploads')
        f.save(upload_path, secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    maneger.run()
    # app.run(debug=True)
