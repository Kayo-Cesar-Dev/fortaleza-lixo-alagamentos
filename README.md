# Fortaleza - Lixo e Alagamentos

## Descrição

Projeto de extensão acadêmica que analisa a relação entre produção de resíduos sólidos e ocorrência de alagamentos em Fortaleza. O objetivo é fornecer ferramentas visuais e análises de dados para apoiar a gestão pública e conscientizar a população.

## Objetivos

* Demonstrar a correlação entre lixo e alagamentos.
* Criar mapas temáticos integrando dados de infraestrutura urbana.
* Propor projeções e ações preventivas para reduzir riscos.

## Estrutura do Repositório

* `data/` - Pasta para colocar os arquivos de dados baixados (CSV e GeoJSON)
* `src/` - Scripts Python para processar dados e gerar JSON para o frontend
* `frontend/` - HTML, CSS e JS para exibição do mapa com Leaflet
* `notebooks/` - (Opcional) Notebooks Jupyter para análises exploratórias
* `reports/` - (Opcional) Relatórios e gráficos gerados

## Tecnologias

* Python
* Pandas, Geopandas
* Leaflet.js para mapas interativos
* Chart.js para gráficos

## Download dos Dados

Para rodar o projeto, você precisará dos arquivos CSV e GeoJSON originais.
Os dados estão disponíveis no Google Drive:

[Baixar dados](https://drive.google.com/drive/folders/17K1tM-U_Yh8x6tE9jYNuwslyPZ6L65G0?usp=sharing)

Após o download, coloque os arquivos na pasta `data/raw/`.

## Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/Kayo-Cesar-Dev/fortaleza-lixo-alagamentos.git
cd fortaleza-lixo-alagamentos
```

### 2. Criar e ativar o ambiente virtual

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar o ETL para gerar o JSON

```bash
python src/data_processing/etl_lixo_alagamento.py
```

* Isso vai gerar o arquivo `result.json` usado pelo frontend.

### 5. Abrir o frontend

* Abra `frontend/index.html` em um navegador web para visualizar o mapa interativo.

## Observações

* Certifique-se de que os dados baixados do Drive estão em `data/raw/` antes de rodar o ETL.
* Todos os scripts Python devem ser rodados dentro do ambiente virtual ativo (`venv`).
