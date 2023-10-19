from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'exemplo'
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

@app.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html', registros=[])

if __name__ == '__main__':
    app.run(debug=True)
