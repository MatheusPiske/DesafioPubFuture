from flask import Flask, jsonify
from mysql import connector

# Funções

def conexao_banco_dados():
    con = connector.connect(
    host='localhost',
    database='FINANCAS_PESSOAIS',
    user='Inserir seu usuário aqui!',
    password='Inserir a sua senha aqui!'
    )
    if con.is_connected():
        cursor = con.cursor()
        return con, cursor
    else:
        return False, False

def encerramento_conexao(con, cursor):
    cursor.close()
    con.close()

# Inicio API

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

@app.route("/", methods=["GET"])
def home():
    return "HELLO WORLD FROM FLASK"

@app.route("/conta", methods=["GET"])
def conta():
    con, cursor = conexao_banco_dados()
    try:
        if con != False:
            sql_query = "SELECT * FROM CONTA;"
            cursor.execute(sql_query)
            conta = cursor.fetchall()
            final_conta = {}
            for i in conta:
                final_conta[str(i[0])] = {"tipo": i[1], "instituicao_financeira" : i[2], "saldo" : i[3]}
            encerramento_conexao(con, cursor)
            return jsonify(final_conta)
        else: 
            encerramento_conexao(con, cursor)
            return "Nao foi possível fazer conexao com o MySQL"
    except Exception as e:
        encerramento_conexao(con, cursor)
        print(f"ERRO: {e}")
        return "Nao foi possivel fazer conexao com o MySQL"

@app.route("/receita/periodo", methods=["GET"])
def receita_periodo():
    con, cursor = conexao_banco_dados()
    try:
        if con != False:
            sql_query = "SELECT * FROM RECEITA ORDER BY DATA_RECEBIMENTO;"
            cursor.execute(sql_query)
            receita = cursor.fetchall()
            final_receita = {}
            for i in receita:
                final_receita[str(i[0])] = {"tipo": i[1], "valor_em_reais" : i[2], "data_recebimento_esperado" : i[3], "id_conta" : i[6], "descricao" : i[5], "data_recebimento" : i[4]}
            encerramento_conexao(con, cursor)
            return jsonify(final_receita)
        else: 
            encerramento_conexao(con, cursor)
            return "Nao foi possível fazer conexao com o MySQL"
    except Exception as e:
        encerramento_conexao(con, cursor)
        print(f"ERRO: {e}")
        return "Nao foi possivel fazer conexao com o MySQL"

@app.route("/receita/tipo", methods=["GET"])
def receita_tipo():
    con, cursor = conexao_banco_dados()
    try:
        if con != False:
            sql_query = "SELECT * FROM RECEITA ORDER BY TIPO;"
            cursor.execute(sql_query)
            receita = cursor.fetchall()
            final_receita = {}
            for i in receita:
                final_receita[str(i[0])] = {"data_recebimento": i[4], "valor_em_reais" : i[2], "data_recebimento_esperado" : i[3], "id_conta" : i[6], "descricao" : i[5], "tipo" : i[1]}
            encerramento_conexao(con, cursor)
            return jsonify(final_receita)
        else: 
            encerramento_conexao(con, cursor)
            return "Nao foi possível fazer conexao com o MySQL"
    except Exception as e:
        encerramento_conexao(con, cursor)
        print(f"ERRO: {e}")
        return "Nao foi possivel fazer conexao com o MySQL"

@app.route("/receita/tudo", methods=["GET"])
def receita_tudo():
    con, cursor = conexao_banco_dados()
    try:
        if con != False:
            sql_query = "SELECT * FROM RECEITA;"
            cursor.execute(sql_query)
            receita = cursor.fetchall()
            final_receita = {}
            for i in receita:
                final_receita[str(i[0])] = {"data_recebimento": i[4], "valor_em_reais" : i[2], "data_recebimento_esperado" : i[3], "id_conta" : i[6], "descricao" : i[5], "tipo" : i[1]}
            encerramento_conexao(con, cursor)
            return jsonify(final_receita)
        else: 
            encerramento_conexao(con, cursor)
            return "Nao foi possível fazer conexao com o MySQL"
    except Exception as e:
        encerramento_conexao(con, cursor)
        print(f"ERRO: {e}")
        return "Nao foi possivel fazer conexao com o MySQL"

@app.route("/despesa/periodo", methods=["GET"])
def despesa_periodo():
    con, cursor = conexao_banco_dados()
    try:
        if con != False:
            sql_query = "SELECT * FROM DESPESA ORDER BY DATA_PAGAMENTO;"
            cursor.execute(sql_query)
            despesa = cursor.fetchall()
            final_despesa = {}
            for i in despesa:
                final_despesa[str(i[0])] = {"tipo": i[1], "valor_em_reais" : i[2], "data_pagamento_esperado" : i[3], "data_pagamento" : i[4], "id_conta" : i[5]}
            encerramento_conexao(con, cursor)
            return jsonify(final_despesa)
        else: 
            encerramento_conexao(con, cursor)
            return "Nao foi possível fazer conexao com o MySQL"
    except Exception as e:
        encerramento_conexao(con, cursor)
        print(f"ERRO: {e}")
        return "Nao foi possivel fazer conexao com o MySQL"

@app.route("/despesa/tipo", methods=["GET"])
def despesa_tipo():
    con, cursor = conexao_banco_dados()
    try:
        if con != False:
            sql_query = "SELECT * FROM DESPESA ORDER BY TIPO;"
            cursor.execute(sql_query)
            despesa = cursor.fetchall()
            final_despesa = {}
            for i in despesa:
                final_despesa[str(i[0])] = {"data_pagamento": i[4], "valor_em_reais" : i[2], "data_pagamento_esperado" : i[3], "tipo" : i[1], "id_conta" : i[5]}
            encerramento_conexao(con, cursor)
            return jsonify(final_despesa)
        else: 
            encerramento_conexao(con, cursor)
            return "Nao foi possível fazer conexao com o MySQL"
    except Exception as e:
        encerramento_conexao(con, cursor)
        print(f"ERRO: {e}")
        return "Nao foi possivel fazer conexao com o MySQL"

@app.route("/despesa/tudo", methods=["GET"])
def despesa_tudo():
    con, cursor = conexao_banco_dados()
    try:
        if con != False:
            sql_query = "SELECT * FROM DESPESA;"
            cursor.execute(sql_query)
            despesa = cursor.fetchall()
            final_despesa = {}
            for i in despesa:
                final_despesa[str(i[0])] = {"data_pagamento": i[4], "valor_em_reais" : i[2], "data_pagamento_esperado" : i[3], "tipo" : i[1], "id_conta" : i[5]}
            encerramento_conexao(con, cursor)
            return jsonify(final_despesa)
        else: 
            encerramento_conexao(con, cursor)
            return "Nao foi possível fazer conexao com o MySQL"
    except Exception as e:
        encerramento_conexao(con, cursor)
        print(f"ERRO: {e}")
        return "Nao foi possivel fazer conexao com o MySQL"

@app.route("/saldo/soma", methods=["GET"])
def soma_saldo():
    con, cursor = conexao_banco_dados()
    try:
        if con != False:
            sql_query = "SELECT SUM(SALDO) AS 'SALDO TOTAL' FROM CONTA;"
            cursor.execute(sql_query)
            soma_saldo = cursor.fetchall()
            encerramento_conexao(con, cursor)
            return str(soma_saldo[0][0])
        else: 
            encerramento_conexao(con, cursor)
            return "Nao foi possível fazer conexao com o MySQL"
    except Exception as e:
        encerramento_conexao(con, cursor)
        print(f"ERRO: {e}")
        return "Nao foi possivel fazer conexao com o MySQL"

if __name__ == "__main__":
    app.run(port=5000, host="localhost", debug=True)