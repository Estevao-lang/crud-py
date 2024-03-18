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

        # Use SELECT para recuperar a senha e o salt do banco de dados
        cursor.execute("SELECT senha, salt FROM user WHERE nome = %s AND email = %s", (nome, email))
        user = cursor.fetchone()

        if user:
            hashed_password_from_db = user['senha'].encode('utf-8')
            salt_from_db = bytes(user['salt'])  # Convertendo bytearray para bytes
            hashed_password_input = bcrypt.hashpw(senha.encode('utf-8'), salt_from_db)

            if hashed_password_from_db == hashed_password_input:
                # As senhas coincidem, redireciona para a página inicial
                cursor.close()
                conn.close()
                return redirect(url_for('pagina_inicial'))
        
        # Se o usuário não existir ou as senhas não coincidirem, renderize a página de login com uma mensagem de erro
        cursor.close()
        conn.close()
        return render_template('login.html', error="Credenciais inválidas")

    # Para solicitações GET, renderize a página de login
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
