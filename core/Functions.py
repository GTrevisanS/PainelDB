from core.Sql import carregar_sql, executar_query, ajustar_query
from core.Config import Connection, SENHAVT, LINKPAGE
import subprocess
import os
import Style

atc = Style.alterar_cor
pause = Style.pause


def AjustarLinkPageFlip(ODB=None):
    UPDATE = str(carregar_sql('sql/UPDATE-LINK-PAGEFLIP.sql'))
    QUERY = ajustar_query(UPDATE, "{DB}", ODB)
    QUERY = ajustar_query(QUERY, "{pageflip}", LINKPAGE)
    executar_query(Connection, QUERY)

def AlterarStatusSessao(ODB=None):
    UPDATE = str(carregar_sql('sql/UPDATE-SESSAO-STATUS.sql'))
    QUERY = ajustar_query(UPDATE, "{DB}", ODB)
    executar_query(Connection, QUERY)

def AlterarSenhasVotacao(ODB=None):
    UPDATE = str(carregar_sql('sql/UPDATE-SENHA-POLITICOS.sql'))
    QUERY2 = ajustar_query(UPDATE, "{DB}", ODB)
    QUERY2 = ajustar_query(QUERY2, "{senhacriptografada}", SENHAVT)
    executar_query(Connection, QUERY2)

def ClonarTabela(BANCO_ORIGEM, BANCO_DESTINO, NOME_TABELA):
    query = str(carregar_sql('sql/CLONE-TABLE.SQL'))
    query = ajustar_query(query,"{BANCO_ORIGEM}", BANCO_ORIGEM)
    query = ajustar_query(query,"{BANCO_DESTINO}", BANCO_DESTINO)
    query = ajustar_query(query,"{NOME_TABELA}", NOME_TABELA)
    executar_query(Connection, query)
    print(atc(f'\n Sucesso!, a tabela "{NOME_TABELA}" foi clonada no banco "{BANCO_DESTINO}"',"GREEN","SIM"))
    pause()


def GerarDump(banco, local_destino):
    host = Connection["host"]
    port = Connection["port"]
    user = Connection["user"]
    password = Connection["password"]

    # Cria a pasta caso ela não exista
    os.makedirs(
        os.path.dirname(local_destino),
        exist_ok=True
    )
    arquivo_dump = local_destino +"\\"+ f"{banco}.sql"

    with open(
        arquivo_dump,
        "w",
        encoding="utf-8"
    ) as arquivo_dump:

        subprocess.run(
            [
                "mysqldump",
                f"-h{host}",
                f"-P{port}",
                f"-u{user}",
                f"-p{password}",
                "--routines",
                "--events",
                "--triggers",
                banco
            ],
            stdout=arquivo_dump,
            check=True
        )

    print(atc(
        f'\n Dump do banco "{banco}" gerado com sucesso!',
        "GREEN",
        "SIM"
    ))
    pause()


def ClonarBanco(banco_origem, banco_destino):
    host = Connection["host"]
    port = Connection["port"]
    user = Connection["user"]
    password = Connection["password"]
    MAX_PACKET = "1G" # espaço máximo permitido para clonagem
    # Apaga e recria o banco destino
    try:
        subprocess.run(
        [
            "mysql",
            f"-h{host}",
            f"-P{port}",
            f"-u{user}",
            f"-p{password}",
            "--max_allowed_packet=1G",
            "-e",
            f"DROP DATABASE IF EXISTS `{banco_destino}`; "
            f"CREATE DATABASE `{banco_destino}`"
        ],
            capture_output=False,
            text=True
        )
        # Gera o dump apenas em memória
        dump = subprocess.Popen(
            [
                "mysqldump",
                f"-h{host}",
                f"-P{port}",
                f"-u{user}",
                f"-p{password}",
                f"--max_allowed_packet={MAX_PACKET}",
                "--routines",
                "--events",
                "--triggers",
                banco_origem
            ],
            stdout=subprocess.PIPE
        )

        # Restaura diretamente no banco destino
        restore = subprocess.Popen(
            [
                "mysql",
                f"-h{host}",
                f"-P{port}",
                f"-u{user}",
                f"-p{password}",
                f"--max_allowed_packet={MAX_PACKET}",
                banco_destino
            ],
            stdin=dump.stdout
        )
    except Exception as erro:
        print("Erro durante clonagem!")
        print("Cheque se o seu usuário possui permissão e se seus dados estão corretos no .env")
        print(f"Erro encontrado: {erro}")

    dump.stdout.close()
    restore.communicate()

    print(atc(
        f'\n O banco "{banco_destino}" foi restaurado com sucesso!',
        "GREEN",
        "SIM"
    ))
    pause()
