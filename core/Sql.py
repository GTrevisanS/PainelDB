import mysql.connector as mysql # Biblioteca usada para conectar com o banco de dados

def carregar_sql(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def executar_query(config, query):
    conexao = mysql.connect(**config)
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(query)
    cursor.close()
    conexao.close()

def ajustar_query(query, oque, troca):
    query = str(query)
    return query.replace(oque, troca)