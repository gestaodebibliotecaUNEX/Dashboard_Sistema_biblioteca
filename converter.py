# converter.py
import pandas as pd

# Nome do seu ficheiro Excel de origem
arquivo_excel = "assets/planilha_lyceum_e_minha_biblioteca.xlsx"

# Nome do novo ficheiro Parquet que será criado
arquivo_parquet = "assets/dados_otimizados.parquet"

print(f"A ler o ficheiro Excel '{arquivo_excel}'...")

# Carrega os dados exatamente como na aplicação principal
df = pd.read_excel(arquivo_excel, header=3)
df.dropna(subset=['Unidade', 'Curso', 'Titulo do Livro'], inplace=True)
df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0).astype(int)
df = df[df['Total'] > 0]

print("A converter para o formato Parquet...")

# Salva o DataFrame no novo formato
df.to_parquet(arquivo_parquet)

print(f"Sucesso! O ficheiro '{arquivo_parquet}' foi criado.")
print("Pode agora alterar o seu 'utils.py' para usar este novo ficheiro.")