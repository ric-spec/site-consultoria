CREATE TABLE leads_consultoria (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    resumo_ia TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);