# Importando a função FLask da biblioteca flask
from flask import Flask, render_template, request, redirect, session, flash


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

# Começamos com a variável onde iremos colocar nossa aplicação
## A variável se chama app e contém como valor a chamada da função Flask com o valor __name__, esse valor referencia esse próprio arquivo.
app = Flask(__name__)
app.secret_key = 'alura'

# Essas listas foram criadas fora para que pudessem ser usadas em quaisquer funções
jogo1 = Jogo('God Of War', 'RPG', 'PS4')
jogo2 = Jogo('The Last Of Us', 'Aventura', 'PS3')
lista = ['GTA V', 'Rainbow Six Siege', 'The Crew 2']
lista2 = [jogo1, jogo2]

# Criando uma rota para colocar informações no site
@app.route('/inicio')
def ola(): #Sempre que criarmos uma rota precisamos definir uma função que vai definir o que existe dentro da rota
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=inicio')
    else:
        return render_template('lista.html', titulo='Jogos', jogos=lista, jogosobt=lista2) # Conteúdo que irá retornar na aplicaçao web

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=novo')
    else:
        return render_template('novo.html', titulo='Cadastrar Novo Jogo')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome'] # Busca o input de name "nome" no HTML novo.html
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console) # Cria um objeto Jogo com os valores dos inputs acima
    lista2.append(jogo) # Adiciona o Jogo na lista2
    return redirect('/inicio')# Redireciona para o inicio

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima is None:
        return redirect('/inicio')
    else:
        return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    session['usuario_logado'] = request.form['usuario']
    if request.form['senha'] == 'senha':
        flash(session['usuario_logado'] + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(f'/{proxima_pagina}')
    else:
        flash('Senha incorreta')
        return redirect('/login')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/login')

# Para a nossa aplicação rodar temos que chamar, sempre no final do arquivo, a nossa variável que contem a aplicação e chamar a função run()
app.run(port=8000, debug=True)