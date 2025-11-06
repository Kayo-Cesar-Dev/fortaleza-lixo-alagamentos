import pandas as pd
import geopandas as gpd
import json

# ===============================================
# 1. CARREGAMENTO E PRÉ-PROCESSAMENTO
# ===============================================

# Carregamento dos dados (Assumindo que todos os arquivos estão na mesma pasta)
try:
    # CSVs
    csv_demandas = pd.read_csv("data/processed/demandas-marco-abril-2022.csv", 
                               sep=",", 
                               encoding="utf-8-sig", 
                               engine="python", 
                               on_bad_lines="skip")
    # Novo CSV: Ocorrências de alagamento, usando vírgula (,) como delimitador
    csv_ocorrencias = pd.read_csv("data/raw/ocorrencias_por_regional.csv", sep=",", encoding="utf-8") 
    
    # GeoJSON
    regionais = gpd.read_file("data/raw/Secretarias_Executivas_Regionais.geojson")
except FileNotFoundError as e:
    # Mensagem de erro caso algum arquivo não seja encontrado na pasta
    print(f"ERRO: Arquivo não encontrado. Verifique se todos os arquivos estão na mesma pasta: {e.filename}")
    exit()

# Normalização de colunas
csv_demandas.columns = csv_demandas.columns.str.strip().str.upper()

# ===============================================
# 2. PROCESSAMENTO: LIXO (DEMANDAS-2022)
# ===============================================

# 2.1. Filtrar apenas demandas de Fortaleza e com Regional válida (SER)
csv_fortaleza = csv_demandas[
    (csv_demandas['CIDADE'].str.upper().str.strip() == 'FORTALEZA') & 
    (csv_demandas['ZONA'].str.startswith('SER', na=False))
].copy()

# 2.2. Criação da Métrica LIXO (Apróx.: Entulho, Poda, Lixo não cadastrado)
LIXO_KEYWORDS = [
    "COLETA DE ENTULHO", 
    "COLETA DE PODA", 
    "COLETA MECANIZADA", 
    "PONTO DE LIXO NÃO CADASTRADO",
    "COLETA DE VOLUMOSO"
]
csv_fortaleza['LIXO_OCORRENCIA'] = csv_fortaleza['TIPO DA DEMANDA'].str.upper().str.contains('|'.join(LIXO_KEYWORDS), na=False)

# 2.3. Agregação do Lixo por Regional
agg_lixo = csv_fortaleza.groupby('ZONA').agg(
    lixo_count=('LIXO_OCORRENCIA', 'sum')
).reset_index().rename(columns={'ZONA': 'regiao_adm'})

# ===============================================
# 3. PROCESSAMENTO: ALAGAMENTO (OCORRENCIAS-2022)
# ===============================================

# 3.1. Filtrar pelas tipologias de Alagamento/Inundação
ALAGAMENTO_KEYWORDS = ["Inundação", "Alagamento"]
df_alagamento = csv_ocorrencias[
    csv_ocorrencias['Tipologia de Ocorrência'].isin(ALAGAMENTO_KEYWORDS)
].copy()

# 3.2. Agregação do Alagamento por Regional
# Exclui o total 'Todas' e agrupa as ocorrências
df_alagamento_regional = df_alagamento[df_alagamento['Regional'].str.lower() != 'todas'].copy()

# Agrega a contagem de ocorrências
agg_alagamento = df_alagamento_regional.groupby('Regional').agg(
    alagamento_count=('Ocorrências', 'sum')
).reset_index()

# 3.3. Normalização da Regional ('SR X' -> 'SER X')
# Isso é crucial para o merge, pois o GeoJSON usa 'SER X'
agg_alagamento['regiao_adm'] = agg_alagamento['Regional'].str.replace('SR ', 'SER ', regex=False)
agg_alagamento = agg_alagamento.drop(columns=['Regional'])


# ===============================================
# 4. CONSOLIDAÇÃO DOS DADOS E EXPORTAÇÃO
# ===============================================

# 4.1. Merge do Lixo e Alagamento
final_data = agg_lixo.merge(
    agg_alagamento,
    on='regiao_adm',
    how='outer' # Garante que nenhuma regional seja perdida no merge
)

# 4.2. Merge com o GeoJSON para garantir todas as regionais (SER 1 a SER 12)
merged_data = regionais[['regiao_adm', 'geometry']].copy().merge(
    final_data,
    on='regiao_adm',
    how='left'
)

# 4.3. Preencher Nulos com 0 e converter para inteiro
merged_data['lixo_count'] = merged_data['lixo_count'].fillna(0).astype(int)
merged_data['alagamento_count'] = merged_data['alagamento_count'].fillna(0).astype(int)

# 4.4. Preparar o JSON para o frontend (requer 'lixo' e 'alagamento')
json_data = merged_data[['regiao_adm', 'lixo_count', 'alagamento_count']].rename(
    columns={'lixo_count': 'lixo', 'alagamento_count': 'alagamento'}
).to_dict('records')

# Salvar o JSON
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("ETL concluído. Arquivo 'result.json' gerado com as contagens atualizadas.")