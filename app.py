from flask import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/estoque')
def estoque():
    return render_template('estoque.html')


if __name__== '__main__':
    app.run(debug=True)