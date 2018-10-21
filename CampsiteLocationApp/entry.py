from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_map')
def get_map():
    return render_template('testGoogleAPI.html')

@app.route('/layout/<name>')
def profile(name):

    return render_template("layout.html", name=name)
if __name__ == '__main__':
    app.run()