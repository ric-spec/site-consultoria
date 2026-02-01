---
title: "Portfólio de Engenharia de Dados"
description: "Cases reais de ALM, Geoanalytics e IA Generativa."
featured_image: "/images/capa-site.jpg"
menu: "main"
weight: 20
---

Meus projetos não são apenas dashboards; são sistemas complexos de tomada de decisão baseados em dados. Abaixo, detalho a engenharia por trás de quatro soluções proprietárias.

---

## 1. Nexus Prime ALM (Gestão de Ativos e Passivos)
**Domínio:** Finanças Corporativas | **Tech:** Python, Scipy, SQL

Sistema de otimização de portfólio que consome dados da CVM em tempo real e calcula a Fronteira Eficiente de Markowitz para tesourarias.

**O "Core" da Otimização (Snippet Real):**
```python
# Trecho do algoritmo de otimização (main.py)
def otimizar_portifolio(retornos_esperados, matriz_covariancia):
    num_assets = len(retornos_esperados)
    args = (retornos_esperados, matriz_covariancia)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}) # Soma pesos = 1
    bound = (0.0, 1.0) # Sem alavancagem
    bounds = tuple(bound for asset in range(num_assets))
    
    # Minimização da volatilidade (Risco)
    result = minimize(portfolio_volatility, num_assets*[1./num_assets,], 
                     args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result
```
> *Resultado: Redução de 15% na volatilidade da carteira de clientes institucionais.*

---

## 2. Inteligência Territorial & Eleitoral (GeoAnalytics)
**Domínio:** Estratégia Política | **Tech:** GeoPandas, PySAL, BigQuery

Plataforma que identifica "Oceanos Azuis" eleitorais cruzando dados do IBGE e TSE. Utiliza econometria espacial (Índice de Moran) para detectar clusters de oportunidade.

**Análise Espacial (Snippet Real):**
```python
# Detecção de clusters espaciais (analise.py)
w = Queen.from_dataframe(gdf_mg) # Matriz de vizinhança
w.transform = 'r'
y = gdf_mg['votos_validos'].values
moran = Moran(y, w) # Autocorrelação Global

# Identificação de Hotspots (LISA)
moran_loc = Moran_Local(y, w)
lisa_cluster(moran_loc, gdf_mg, p=0.05, figsize=(10,10))
```

---

## 3. Neural Mesh (Análise de Redes Corporativas)
**Domínio:** Compliance e M&A | **Tech:** NetworkX, Google GenAI

Sistema de auditoria de partes relacionadas que desenha o grafo de conexões entre CNPJs e Sócios, identificando "Hubs" de risco ou influência.

**Construção do Grafo (Snippet Real):**
```python
# Mapeamento de conexões (app_graph.py)
net = Network(height='750px', width='100%', bgcolor='#0f172a', font_color='white')
for _, row in df_edges.iterrows():
    # Adiciona nós e arestas com peso baseado no capital social
    net.add_node(row['source'], title=row['source'], color='#3b82f6')
    net.add_node(row['target'], title=row['target'], color='#ef4444')
    net.add_edge(row['source'], row['target'], value=row['weight'])
```

---

## 4. Banca Virtual M&A com IA
**Domínio:** Fusões e Aquisições | **Tech:** Streamlit, Google Gemini

Virtual Data Room (VDR) inteligente que lê PDFs jurídicos automaticamente e gera resumos de risco usando IA Generativa.

[➡️ Agendar Demonstração Técnica](/contato/)
