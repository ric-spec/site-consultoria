import requests
import json

# URL do seu Agente no Render
url = "https://agente-consultoria.onrender.com/contato"

# O pacote de dados
payload = {
    "nome": "Henrique Teste Python",
    "email": "admin@henriqueoliver.com",
    "mensagem": "Verificando se o Neon esta gravando."
}

print(f"📡 Enviando dados para: {url}...")

try:
    response = requests.post(url, json=payload, timeout=10)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Resposta do Servidor: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ SUCESSO! O Site, o Render e o Neon estão conectados.")
    elif response.status_code == 500:
        print("\n⚠️ ERRO 500: O Render recebeu, mas não conseguiu falar com o Banco.")
        print("SOLUÇÃO: Verifique se a variável DATABASE_URL foi configurada no painel do Render.")
    else:
        print("\n❌ ERRO DESCONHECIDO.")

except Exception as e:
    print(f"\n💀 Erro de conexão: {e}")
