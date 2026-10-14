from core.Functions import AlterarSenhasVotacao, AjustarLinkPageFlip, AlterarStatusSessao, ClonarBanco, ClonarTabela, GerarDump
from core.Validations import banco_nao_existe, bancos_iguais, bancos_nao_digitados, tabela_nao_existe, pasta_invalida, NaoTemPermissoes
from core.Config import Connection
import Style

atc = Style.alterar_cor
loading = Style.loading
centraliza = Style.centraliza
pause = Style.pause
alert = Style.alert
cls = Style.cls

def ALTERAR_STATUS_SESSAO(ODB=None):
    if not ODB:
        while True:
            DB = input(atc("\n Informe o nome do banco: ", "YELLOW", "SIM"))
            if banco_nao_existe(DB):
                painel()
            else:
                AlterarStatusSessao(DB)
                print(atc('\n Query executada com sucesso!, Status da sessão alterado!',"GREEN","SIM"))
                pause()
                break
    else:
        AlterarStatusSessao(ODB)

def REDEFINIR_SENHA_VOTACAO(ODB=None):
    if not ODB:
        while True:
            DB = input(atc("\n Informe o nome do banco: ", "YELLOW", "SIM"))
            if banco_nao_existe(DB):
                painel()
            else:
                AlterarSenhasVotacao(DB)
                print(atc('\n Query executada com sucesso!, "Senhas alteradas para 123"!',"GREEN","SIM"))
                pause()
                break
    else:
        AlterarSenhasVotacao(ODB)


def RESETAR_PAGEFLIP(ODB=None):
    if not ODB:
        while True:
            DB = input(atc("\n Informe o nome do banco: ", "YELLOW", "SIM"))
            if banco_nao_existe(str(DB)):
                painel()
            else:
                AjustarLinkPageFlip(DB)
                print(atc('\n Query executada com sucesso!, "Senhas alteradas para 123"!',"GREEN","SIM"))
                pause()
                break
    else:
        AjustarLinkPageFlip(ODB)


def PAINEL_VOTACAO(servidor):
    while True:
        cls()
        print(atc("", "CYAN", "SIM"))
        print()
        print(centraliza(" PAINEL VOTAÇÃO (DEFINA OQUE DESEJA) ", "="))
        print()
        print(atc("", "CYAN", "SIM"))
        print(centraliza("Redefinir senhas dos vereadores       DIGITE...           [1]", " "))
        print(centraliza("Redefinir Config PageFlip             DIGITE...           [2]", " "))
        print(centraliza("Ajustar por completo para sessão      DIGITE...           [3]", " "))
        print(atc("", "BLACK", "SIM"))
        print(centraliza("Voltar ao painel                      DIGITE...           [X]", " "))
        print(atc("", "CYAN", "SIM"))
        print(centraliza(f" [{servidor}] ", "="))
        print()
        resposta = input("> ")
        match str(resposta).strip().lower():
            case "1":
                REDEFINIR_SENHA_VOTACAO()
            case "2":
                RESETAR_PAGEFLIP()
            case "3":
                ODB = input(atc("\n Digite o nome do banco: ", "YELLOW", "SIM"))
                if banco_nao_existe(str(ODB)):
                    pass
                else:
                    REDEFINIR_SENHA_VOTACAO(ODB)
                    RESETAR_PAGEFLIP(ODB)
                    ALTERAR_STATUS_SESSAO(ODB)
                    print(atc('\n Todas as queries foram executadas com sucesso!, a sessão esta pronta para teste.',"GREEN","SIM"))
                    pause()
            case "x":
                break
            case _:
                pass


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
        print(centraliza("Acessar painel Votação                   DIGITE...           [4]", " "))
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
                PAINEL_VOTACAO(servidor=str(Connection["host"]))
            case _:
                pass
painel()


