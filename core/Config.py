from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env') # CARREGA O ARQUIVO .ENV

Connection = { 
        "host": os.getenv("HOST"),
        "port": int(os.getenv("PORT")),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "charset": "utf8" # Formatação necessária no MySql antigo
} 

SENHAVT = os.getenv("SENHA_VOTACAO")
LINKPAGE = os.getenv("LINK_PAGEFLIP")