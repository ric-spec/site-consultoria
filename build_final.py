import os

def write_file(path, content):
    # Garante que o caminho seja tratado corretamente pelo SO
    absolute_path = os.path.join(os.getcwd(), path)
    directory = os.path.dirname(absolute_path)
    
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(absolute_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Criado: {path}")

# --- DEFINIÇÃO DOS ARQUIVOS ---
files = {
    "backend/main.py": """
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
""",
    "backend/requirements.txt": "fastapi\nuvicorn\npsycopg2-binary\npython-dotenv",

    "frontend/hugo.toml": "baseURL = 'https://henriqueoliver.adm.br/'\ntitle = 'Henrique Oliver | Financas e Governanca'\ntheme = 'ananke'",

    "dashboard/app.py": """
import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="BI Consultoria Oliver", layout="wide")

def get_data():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
    df = pd.read_sql("SELECT * FROM leads_consultoria", conn)
    conn.close()
    return df

st.title("📊 Dashboard de Governanca")
try:
    df = get_data()
    st.dataframe(df)
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
""",
    "dashboard/requirements.txt": "streamlit\npandas\npsycopg2-binary\npython-dotenv",

    "database/schema.sql": """
CREATE TABLE leads_consultoria (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    resumo_ia TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""",
    "deploy.sh": "#!/bin/bash\ngit add .\ngit commit -m 'Deploy Completo'\ngit push origin main"
}

if __name__ == "__main__":
    print(f"📂 Iniciando geracao de arquivos em: {os.getcwd()}")
    for path, content in files.items():
        write_file(path, content)
    
    # Dar permissão de execução ao deploy.sh
    os.chmod("deploy.sh", 0o755)
    print("\n🚀 Projeto pronto para o próximo passo!")
