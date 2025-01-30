import json
import os
from flask import *
from produtos import produtos

app = Flask(__name__)

# Caminho do arquivo onde os produtos serão salvos
ARQUIVO_PRODUTOS = "produtos.txt"

# Função para carregar produtos do arquivo ao iniciar o programa
def carregar_produtos():
    global produtos
    if os.path.exists(ARQUIVO_PRODUTOS):  # Verifica se o arquivo existe
        with open(ARQUIVO_PRODUTOS, "r") as f:
            try:
                produtos.extend(json.load(f))  # Carrega os produtos salvos
            except json.JSONDecodeError:
                produtos = []  # Se houver erro no arquivo, inicia com lista vazia
    else:
        with open(ARQUIVO_PRODUTOS, "w") as f:
            json.dump([], f)  # Cria o arquivo vazio se não existir

# Função para salvar os produtos no arquivo
def salvar_produtos():
    with open(ARQUIVO_PRODUTOS, "w") as f:
        json.dump(produtos, f, indent=4)

# Carregar produtos ao iniciar
carregar_produtos()

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
    salvar_produtos()  # Salvar após excluir
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
    salvar_produtos()  # Salvar após adicionar um novo produto
    return redirect(url_for('estoque'))

@app.route('/baixa/<int:produto_id>')
def baixa(produto_id):
    return render_template('baixa.html', id=produto_id)

@app.route('/baixa_estoque')
def baixa_estoque():
    global produtos
    id = int(request.args.get('id'))
    dim = int(request.args.get('venda'))
    for produto in produtos:
        if produto['id'] == id:
            produto['quantidade'] -= dim
            break
    salvar_produtos()  # Salvar após baixa no estoque
    return redirect(url_for('estoque'))

@app.route('/add/<int:produto_id>')
def add(produto_id):
    return render_template('add.html', id=produto_id)

@app.route('/add_estoque')
def add_estoque():
    global produtos
    id = int(request.args.get('id'))
    add = int(request.args.get('add'))
    for produto in produtos:
        if produto['id'] == id:
            produto['quantidade'] += add
            break
    salvar_produtos()  # Salvar após adicionar estoque
    return redirect(url_for('estoque'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
