from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import bcrypt
app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'registro'
}

# Rota para adicionar registro
@app.route('/adicionar_registro', methods=['GET', 'POST'])
def adicionar_registro():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO registros (nome, idade) VALUES (%s, %s)", (nome, idade))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('exibir_registros'))

    return render_template('adicionar_registro.html')

# Rota para exibir registros
@app.route('/exibir_registros')
def exibir_registros():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM registros")
    registros = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('exibir_registros.html', registros=registros)

@app.route('/registro_de_login.html', methods= ['GET','POST'])
def registro_de_login():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        #Encode a senha antes de aplicar hash
        senha_encoded = senha.encode('utf-8')
        
        salt = bcrypt.gensalt(8)
        hashed_password  = bcrypt.hashpw(senha_encoded,salt)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO user (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, hashed_password))
        conn.commit()

        cursor.close()
        conn.close()
    return render_template('registro_de_login.html')

@app.route('/login')
def login_page():
     return render_template('login.html')

@app.route('/')
def login():
    return render_template('login.html', registros=[])

@app.route('/login.html', methods=['POST', 'GET'])
def verifica_login():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Use SELECT para verificar os dados de login
        cursor.execute("SELECT * FROM user WHERE nome = %s AND email = %s", (nome, email))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
            # Senha correta, redirecione para a página inicial
            return render_template('pagina_inicial.html')
        else:
            # Senha incorreta, renderize a página de login novamente
            return render_template('login.html')

    # Se for um método GET, renderize a página de login novamente
    return render_template('login.html')

# ... (restante do seu código)

if __name__ == '__main__':
    app.run(debug=True)
