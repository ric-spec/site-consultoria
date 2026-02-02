import os
import uvicorn
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- LIBERAÇÃO TOTAL DE SEGURANÇA (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que a Vercel acesse
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contato(BaseModel):
    nome: str
    email: str
    mensagem: str

@app.get("/")
def home():
    return {"status": "online", "system": "Henrique Oliver Agent"}

@app.post("/contato")
def receber_contato(dado: Contato):
    try:
        # Tenta conectar ao banco
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            return {"status": "erro", "mensagem": "Sem conexão com Banco de Dados"}
            
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Cria tabela se não existir
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id SERIAL PRIMARY KEY,
                nome TEXT,
                email TEXT,
                mensagem TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Salva o contato
        cur.execute(
            "INSERT INTO leads (nome, email, mensagem) VALUES (%s, %s, %s)",
            (dado.nome, dado.email, dado.mensagem)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "sucesso", "mensagem": "Lead salvo no Neon!"}
        
    except Exception as e:
        print(f"Erro Crítico: {e}")
        # Retorna o erro para o site ver o que houve
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
