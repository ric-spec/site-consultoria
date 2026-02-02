import os
import uvicorn
import psycopg2
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração de CORS (Permitir acesso do Site e Scripts)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "online", "mode": "Debug Raw"}

# Note o uso de 'request: Request' em vez do modelo Pydantic
@app.post("/contato")
async def receber_contato(request: Request):
    try:
        # 1. Força a leitura do JSON bruto
        data = await request.json()
        print(f"📦 PAYLOAD RECEBIDO: {data}")
        
        # 2. Extrai os dados manualmente
        nome = data.get("nome")
        email = data.get("email")
        mensagem = data.get("mensagem")
        
        if not email:
            raise HTTPException(status_code=400, detail="Campo email obrigatório")

        # 3. Conecta no Neon
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("❌ ERRO: DATABASE_URL não configurada")
            # Retorna 500 para sabermos que é erro de banco
            raise HTTPException(status_code=500, detail="Erro de Configuração do Banco")
            
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id SERIAL PRIMARY KEY,
                nome TEXT,
                email TEXT,
                mensagem TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cur.execute(
            "INSERT INTO leads (nome, email, mensagem) VALUES (%s, %s, %s)",
            (nome, email, mensagem)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "sucesso", "mensagem": "Lead gravado com sucesso"}

    except Exception as e:
        print(f"💀 Erro: {e}")
        # Se der erro, devolve 500 com a mensagem real
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
