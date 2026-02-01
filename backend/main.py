from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- Configuração de Segurança (CORS) ---
# Permite que seu site na Vercel converse com este backend
origins = [
    "https://site-consultoria-pd8r.vercel.app",  # Seu link Vercel
    "https://henriqueoliver.adm.br",             # Seu domínio oficial
    "http://localhost:1313"                      # Para testes locais
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Por enquanto liberado geral para facilitar o setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "API do Agente de IA operante."}

@app.post("/contato")
def receber_contato(nome: str = Form(...), email: str = Form(...), mensagem: str = Form(...)):
    # Aqui é onde a IA vai entrar depois.
    # Por enquanto, apenas recebemos e confirmamos.
    print(f"Nova mensagem de: {nome} <{email}>")
    print(f"Conteúdo: {mensagem}")
    return {"status": "recebido", "message": "Obrigado! Recebi sua mensagem."}
