import os
import uvicorn
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CONFIGURAÇÃO DE SEGURANÇA (CORS) ---
# Isso permite que o seu site na Vercel fale com este Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, idealmente coloque o domínio do seu site aqui
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados
class Contato(BaseModel):
    nome: str
    email: str
    mensagem: str

# Conexão com Banco de Dados (Neon)
def get_db_connection():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise Exception("A variável DATABASE_URL não está configurada no Render.")
    return psycopg2.connect(url)

@app.get("/")
def home():
    return {"status": "online", "message": "Agente de IA operante. Envie POST para /contato"}

@app.post("/contato")
def receber_contato(dado: Contato):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Cria a tabela se não existir (Autocorreção)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id SERIAL PRIMARY KEY,
                nome TEXT,
                email TEXT,
                mensagem TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Insere o lead
        cur.execute(
            "INSERT INTO leads (nome, email, mensagem) VALUES (%s, %s, %s)",
            (dado.nome, dado.email, dado.mensagem)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"Lead recebido: {dado.email}")
        return {"status": "sucesso", "mensagem": "Lead registrado no Neon."}
        
    except Exception as e:
        print(f"Erro no Backend: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
