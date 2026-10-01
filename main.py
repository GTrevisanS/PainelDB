from core.Functions import AlterarSenhasVotacao, AjustarLinkPageFlip, ClonarBanco, ClonarTabela, GerarDump
from core.Validations import banco_nao_existe, bancos_iguais, bancos_nao_digitados, tabela_nao_existe, pasta_invalida, NaoTemPermissoes
from core.Config import Connection
import Style

atc = Style.alterar_cor
loading = Style.loading
centraliza = Style.centraliza
pause = Style.pause
alert = Style.alert
cls = Style.cls

def REDEFINIR_SENHA_VOTACAO():
    while True:
        DB = input(atc("\n Informe o nome do banco: ", "YELLOW", "SIM"))
        if banco_nao_existe(DB):
            painel()
        else:
            AlterarSenhasVotacao(DB)
            break


def RESETAR_PAGEFLIP():
    while True:
        DB = input(atc("\n Informe o nome do banco: ", "YELLOW", "SIM"))
        if banco_nao_existe(str(DB)):
            painel()
        else:
            AjustarLinkPageFlip(DB)
            break


def CLONAR_DB():
    while True:
        cls()
        print()
        print(centraliza(" CLONAGEM / RESTAURAÇÃO DE BANCO ", "="))
        print(atc("", "BLACK", "SIM"))
        print(centraliza(" Esse processo deleta e recria um banco novo do zero", " "))
        print(centraliza(" baseado na formatação e estrutura do banco destino ", " "))
        print(atc(centraliza(" ORIGEM = Banco base      DESTINO = Banco restaurado", " "), "GREEN", "NAO"))
        print()
        BANCO_ORIGEM = input(atc("\n Nome do banco [ORIGEM]: ", "YELLOW", "SIM")).strip().lower()
        BANCO_DESTINO = input(atc(" Nome do banco [DESTINO]: ", "YELLOW", "SIM")).strip().lower()
        if bancos_nao_digitados(BANCO_ORIGEM, BANCO_DESTINO):
            painel()     
        elif bancos_iguais(BANCO_ORIGEM, BANCO_DESTINO):
            painel()
        elif banco_nao_existe(BANCO_ORIGEM):
            painel()
        elif NaoTemPermissoes([
            'DROP',
            'CREATE',
            'SELECT',
            'INSERT',
            'ALTER',
            'INDEX',
            'TRIGGER',
            'EVENT',
            'CREATE VIEW',
            'SHOW VIEW']):
            painel()
        else:
            print()
            loading(" Iniciando clonagem e restauração do banco")
            ClonarBanco(BANCO_ORIGEM, BANCO_DESTINO)
            break



def CLONAR_TABELA():
    while True:
        cls()
        print(atc("", "BLUE", "SIM"))
        print(centraliza(" CLONAGEM DE TABELA DE BANCO ", "="))
        print(atc("", "BLACK", "SIM"))
        print(centraliza(" Esse processo cria uma nova tabela com os dados e ", " "))
        print(centraliza(" formatação do banco selecionado. (No caso da tabela ", " "))
        print(centraliza(" já existir, ela será deletada e depois recriada) ", " "))
        print(atc(centraliza(" ORIGEM = Banco base      DESTINO = Banco restaurado", " "), "GREEN", "NAO"))
        print("\n")
        BANCO_ORIGEM  = input(atc(" Nome do banco [ORIGEM]: ", "BLUE", "SIM")).strip().lower()
        BANCO_DESTINO = input(atc(" Nome do banco [DESTINO]: ", "BLUE", "SIM")).strip().lower()
        NOME_TABELA   = input(atc(" Nome da tabela do banco [ORIGEM]: ", "GREEN", "SIM")).strip().lower()
        if bancos_nao_digitados(BANCO_ORIGEM, BANCO_DESTINO):
            painel()
        if bancos_iguais(BANCO_ORIGEM, BANCO_DESTINO):
            painel()
        elif banco_nao_existe(BANCO_ORIGEM) or banco_nao_existe(BANCO_DESTINO):
            painel()
        elif tabela_nao_existe(BANCO_ORIGEM, NOME_TABELA):
            painel()    
        elif NaoTemPermissoes(['DROP', 'CREATE', 'INSERT', 'SELECT']):
            painel()
        else:
            print()
            loading(" Iniciando clonagem da tabela do banco origem")
            ClonarTabela(BANCO_ORIGEM, BANCO_DESTINO, NOME_TABELA)
            break


def GERAR_ARQUIVO_DUMP():
    while True:
        cls()
        print(atc("", "BLUE", "SIM"))
        print(centraliza(" GERAÇÃO DE ARQUIVO .SQL COM BANCO D SERVIDOR ", "="))
        print(atc("", "BLACK", "SIM"))
        print(centraliza(" Informe o nome do banco que deseja gerar o dump e o ", " "))
        print(centraliza(" local que deseja gerar o dump", " "))
        # print(centraliza(" já existir, ela será deletada e depois recriada) ", " "))
        print("\n")
        BANCO = input(atc(" Nome do banco [DUMP]: ", "BLUE", "SIM")).strip().lower()
        # print("")
        PASTA = input(atc(" Caminho da pasta: ", "YELLOW", "SIM")).strip().lower()
        if bancos_nao_digitados(BANCO, 1):
            painel()
        elif pasta_invalida(PASTA):
            painel()
        elif banco_nao_existe(BANCO):
            painel()
        elif NaoTemPermissoes(['SELECT','SHOW VIEW','TRIGGER','EVENT']):
            painel()
        else:
            print()
            loading(" Iniciando geração do arquivo dump na pasta")
            GerarDump(BANCO, PASTA)
            break


def painel(servidor=str(Connection["host"])):
    while True:
        cls()
        print(atc("", "BLUE", "SIM"))
        print()
        print(centraliza(" PAINEL DB (DEFINA OQUE DESEJA) ", "="))
        print()
        print(atc("", "BLUE", "SIM"))
        print(centraliza("Clonar um banco a partir de outro        DIGITE...           [1]", " "))
        print(centraliza("Clonar uma tabela de outro banco         DIGITE...           [2]", " "))
        print(atc(centraliza("Gerar um arquivo dump de um banco        DIGITE...           [3]", " "), "BLACK", "SIM"))
        print(atc("", "YELLOW", "NAO"))
        print(centraliza("[Votação] Redefinir Senhas politicos     DIGITE...           [4]", " "))
        print(centraliza("[Votação] Redefinir Config PageFlip      DIGITE...           [5]", " "))
        print(atc("", "BLUE", "SIM"))
        print()
        print(centraliza(f" [{servidor}] ", "="))
        print()
        resposta = input("> ")
        match str(resposta).strip().lower():
            case "1":
                CLONAR_DB()
            case "2":
                CLONAR_TABELA()
            case "3":
                GERAR_ARQUIVO_DUMP()
            case "4":
                REDEFINIR_SENHA_VOTACAO()
            case "5":
                RESETAR_PAGEFLIP()
painel()


