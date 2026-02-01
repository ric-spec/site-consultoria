from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Agente de Governanca Henrique Oliver")

class Lead(BaseModel):
    nome: str
    email: str
    mensagem: str

@app.post("/api/chat")
async def handle_lead(lead: Lead):
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
        cur = conn.cursor()
        cur.execute("INSERT INTO leads_consultoria (nome, email, resumo_ia) VALUES (%s, %s, %s)", 
                    (lead.nome, lead.email, lead.mensagem))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "sucesso", "msg": "Dados salvos com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))