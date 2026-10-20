from Style import alert, alterar_cor as atc
from core.Functions import Connection
import os, re, mysql.connector as mysql


def tem_permissao(grants, permissao):
    permissao = permissao.upper().strip()
    for grant in grants:
        grant = grant[0].upper()
        match = re.search(r"GRANT (.*?) ON ", grant)
        if not match:
            continue
        permissoes = match.group(1).split(",")
        permissoes = [p.strip() for p in permissoes]
        if permissao in permissoes:
            return True
    return False

def NaoTemPermissoes(permissoes_necessarias):
    conexao = mysql.connect(**Connection)
    cursor = conexao.cursor()
    try:
        cursor.execute("SHOW GRANTS FOR CURRENT_USER();")
        grants = cursor.fetchall()
        suas_permissoes = []
        faltantes = []
        for cada_permissao in permissoes_necessarias:
            if tem_permissao(grants, cada_permissao):
                suas_permissoes.append(str(cada_permissao))
            else:
                faltantes.append(str(cada_permissao))

        tem_todas = tem_permissao(grants, 'ALL PRIVILEGES')
        if suas_permissoes == permissoes_necessarias or tem_todas:
            print(atc("\n Confirmadas as permissões do usuário para realizar as ações.", "BLUE", "SIM"))
            return False
        else:
            alert("Erro no processo!, seu usuário não possui as permissões minimas.")
            # alert(f"PERMISSOES FALTANTES: {faltantes}")
            return True
    except Exception as erro:
        print("\nERRO:", erro)
        input()
        return True
    finally:
        cursor.close()
        conexao.close()

def ProcurarBanco(nome_banco):
    conexao = mysql.connect(**Connection)
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT SCHEMA_NAME
            FROM information_schema.SCHEMATA
            WHERE SCHEMA_NAME = %s
        """, (nome_banco,))

        resultado = cursor.fetchone()
        return resultado is not None
    finally:
        cursor.close()
        conexao.close()

def ProcurarTabela(nome_banco, nome_tabela):
    conexao = mysql.connect(**Connection)
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT TABLE_NAME
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = %s
              AND TABLE_NAME = %s
        """, (nome_banco, nome_tabela))

        resultado = cursor.fetchone()

        return resultado is not None

    finally:
        cursor.close()
        conexao.close()


def banco_nao_existe(nome_banco):
    if not ProcurarBanco(nome_banco):
        alert(
            f'O banco "{nome_banco}" não foi encontrado ou não existe!'
        )
        return True
    return False


def bancos_iguais(DB1, DB2):
    if DB1 == DB2:
        alert(
            "O banco origem e o banco destino precisam ser bancos diferentes!"
        )
        return True
    return False


def tabela_nao_existe(nome_banco, nome_tabela):
    if not ProcurarTabela(nome_banco, nome_tabela):
        alert(
            f'A tabela "{nome_tabela}" não foi encontrada '
            f'\n no banco "{nome_banco}" ou não existe!'
        )
        return True
    return False


def bancos_nao_digitados(DB1, DB2):
    if not DB1 and not DB2:
        alert(' Você precisa informar o nome dos dois bancos!')
        return True
    elif DB1 and not DB2:
        alert(' Você precisa informar o nome do segundo banco!')
        return True
    elif not DB1 and DB2:
        alert(' Você precisa informar o nome do primeiro banco!')
        return True
    return False

def banco_nao_digitado(DB):
    if not DB:
        alert(' Você precisa informar o nome banco!')
        return True
    return False


def pasta_invalida(PASTA):
    if not PASTA:
        alert(' Você precisa digitar o caminho da pasta!')
        return True
    elif not os.path.isdir(PASTA):
        alert(' Digite um caminho de pasta que seja valido!')
        return True
    return False

