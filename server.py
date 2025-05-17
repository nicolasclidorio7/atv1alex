from flask import *

app = Flask(__name__)
app.secret_key = 'segredo'

users = {}

home_template = """
<h2>Bem-vindo!</h2>
<ul>
    <li><a href="/cadastro">Cadastrar novo usuário</a></li>
    <li><a href="/login">Login</a></li>
    <li><a href="/listar">Listar usuários</a></li>
    <li><a href="/buscar">Buscar usuário</a></li>
    <li><a href="/recuperar">Recuperar senha</a></li>
</ul>
"""

@app.route("/")
def home():
    return home_template

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]
        descricao = request.form["descricao"]
        senha_recuperacao = request.form["senha_recuperacao"]
        if nome in users:
            return "Usuário já existe!"
        users[nome] = {"senha": senha, "descricao": descricao, "senha_recuperacao": senha_recuperacao}
        return redirect(url_for("home"))
    return '''
        <form method="post">
            Nome: <input name="nome"><br>
            Senha: <input name="senha" type="password"><br>
            Descrição: <input name="descricao"><br>
            Palavra secreta para recuperação de senha: <input name="senha_recuperacao"><br>
            <input type="submit" value="Cadastrar">
        </form>
    '''

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]
        if nome in users and users[nome]["senha"] == senha:
            session["usuario"] = nome
            return redirect(url_for("perfil"))
        return "Usuário ou senha incorretos."
    return '''
        <form method="post">
            Nome: <input name="nome"><br>
            Senha: <input name="senha" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route("/perfil")
def perfil():
    if "usuario" not in session:
        return redirect(url_for("login"))
    nome = session["usuario"]
    return f'''
        <h3>Bem-vindo, {nome}</h3>
        <p>Descrição: {users[nome]["descricao"]}</p>
        <a href="/alterar">Alterar senha</a><br>
        <a href="/remover">Remover usuário</a><br>
        <a href="/logout">Logout</a>
    '''

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("home"))

@app.route("/remover")
def remover():
    if "usuario" in session:
        nome = session.pop("usuario")
        users.pop(nome, None)
    return redirect(url_for("home"))

@app.route("/listar")
def listar():
    return "<br>".join(users.keys())

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    if request.method == "POST":
        nome = request.form["nome"]
        resultados = [user for user in users if nome.lower() in user.lower()]
        return "<br>".join(resultados)
    return '''
        <form method="post">
            Nome para buscar: <input name="nome"><br>
            <input type="submit" value="Buscar">
        </form>
    '''

@app.route("/alterar", methods=["GET", "POST"])
def alterar():
    if "usuario" not in session:
        return redirect(url_for("login"))
    nome = session["usuario"]
    if request.method == "POST":
        nova_senha = request.form["nova_senha"]
        users[nome]["senha"] = nova_senha
        return "Senha alterada com sucesso!"
    return '''
        <form method="post">
            Nova senha: <input name="nova_senha" type="password"><br>
            <input type="submit" value="Alterar">
        </form>
    '''

@app.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    if request.method == "POST":
        nome = request.form["nome"]
        resposta = request.form["resposta"]
        if nome in users and users[nome]["senha_recuperacao"] == resposta:
            return f"Senha do usuário {nome}: {users[nome]['senha']}"
        return "Informações incorretas."
    return '''
        <form method="post">
            Nome: <input name="nome"><br>
            Palavra secreta: <input name="resposta"><br>
            <input type="submit" value="Recuperar Senha">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)