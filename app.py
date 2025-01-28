from flask import *
from produtos import produtos

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/produtos')
def estoque():
    return render_template('produtos.html', produtos=produtos)

@app.route('/excluir/<int:produto_id>')
def excluir_produto(produto_id):
    global produtos
    produtos = [produto for produto in produtos if produto['id'] != produto_id]

    return redirect(url_for('estoque'))


if __name__== '__main__':
    app.run(debug=True)