from colorama import init, Fore
import itertools
import time
import sys
import os

def cls():
    os.system('cls')

def alterar_cor(texto, cor, claro): # Função usada para deixar os caracteres coloridos ao printar no terminal 
    match claro.strip().lower():
        case "sim":
            nomecor = f"LIGHT{cor.upper()}_EX"
            coloracao = getattr(Fore, nomecor)
        case "nao":
            nomecor = f"{cor.upper()}"
            coloracao = getattr(Fore, nomecor)
    resultado = (coloracao + f'{texto}')
    return resultado


def loading(texto="Carregando", duracao=2): # Função usada para criar efeito de carregamento visual no terminal
    inicio = time.time()
    for simbolo in itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"):
        if time.time() - inicio >= duracao:
            break
        sys.stdout.write(alterar_cor(f"\r{texto} {simbolo}","white", "sim"))
        sys.stdout.flush()
        time.sleep(0.1)
    texto = (f"\r{texto} ✔")
    print(alterar_cor(texto, "green", "sim"))


def centraliza(texto, caractere):
    if not texto:
        texto = str(caractere)
    titulo = texto.center(90, caractere) 
    return titulo


def criar_faixa(caractere):
    caractere = str(caractere)
    faixa = caractere.center(90, caractere) 
    return faixa


def pause():  # Função para pausar processos
    input(alterar_cor("\n Pressione ENTER para continuar...", "black", "sim"))


def alert(texto): # Função para dar alerta / usada na tratativa de erro
    input(alterar_cor(f"\n {texto} \n","red","sim"))