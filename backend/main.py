import os
import uvicorn
import psycopg2
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. Configuração de CORS (Liberar acesso do site)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Modelo de Dados (Garante que os nomes batem)
class Contato(BaseModel):
    nome: str
    email: str
    mensagem: str

@app.get("/")
def home():
    return {"status": "online", "system": "Henrique Oliver Agent V2"}

@app.post("/contato")
def receber_contato(dado: Contato):
    print(f"📥 Recebido: {dado}")  # Isso vai aparecer no log do Render
    
    try:
        # 3. Conexão com Banco de Dados Neon
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("❌ ERRO: Variável DATABASE_URL não encontrada!")
            raise HTTPException(status_code=500, detail="Servidor sem configuração de Banco")
            
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Cria a tabela se não existir
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id SERIAL PRIMARY KEY,
                nome TEXT,
                email TEXT,
                mensagem TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Insere o dado
        cur.execute(
            "INSERT INTO leads (nome, email, mensagem) VALUES (%s, %s, %s)",
            (dado.nome, dado.email, dado.mensagem)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "sucesso", "mensagem": "Lead salvo no Neon!"}

    except Exception as e:
        print(f"💀 Erro Crítico no Banco: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
