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

@app.route('/cadastro')
def cadastrar():
    return render_template('form.html')

@app.route('/save')
def save():
    global produtos
    id = len(produtos) + 1
    nome = request.args.get('nome')
    quant = int(request.args.get('quant'))
    produto = {'id': id, 'nome': nome, 'quantidade': quant}
    produtos.append(produto)

    return redirect(url_for('estoque'))

@app.route('/baixa/<int:produto_id>')
def baixa(produto_id):
    return render_template('baixa.html', id = produto_id)

@app.route('/baixa_estoque')
def baixa_estoque():
    global produtos
    id = int(request.args.get('id'))
    dim = int(request.args.get('venda'))
    for produto in produtos:
        if produto['id'] == id:
            produto['quantidade'] -= dim
            break
    return redirect(url_for('estoque'))

@app.route('/add/<int:produto_id>')
def add(produto_id):
    return render_template('add.html', id = produto_id)

@app.route('/add_estoque')
def add_estoque():
    global produtos
    id = int(request.args.get('id'))
    add = int(request.args.get('add'))
    for produto in produtos:
        if produto['id'] == id:
            produto['quantidade'] += add
            break
    return redirect(url_for('estoque'))



if __name__== '__main__':
    app.run(debug=True)