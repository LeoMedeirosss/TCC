import csv
import subprocess
import os
from pathlib import Path

# Caminho para o repositório
REPO_PATH = r"C:\Users\leozi\OneDrive\Área de Trabalho\Analise\RepositoriosClonados\metabase"
# Caminho do arquivo CSV de entrada
CSV_PATH = r"C:\Users\leozi\OneDrive\Área de Trabalho\Analise\RepositoriosClonados\csv\metabase\components_smells.csv"
# Caminho do arquivo de saída
OUTPUT_FILE = r"C:\Users\leozi\OneDrive\Área de Trabalho\Analise\RepositoriosClonados\analises\commits_por_arquivo.csv"

def get_commit_count(file_path):
    """Retorna o número de commits para um arquivo específico"""
    try:
        # Converte o caminho absoluto para relativo ao repositório
        rel_path = os.path.relpath(file_path, REPO_PATH)
        # Substitui \ por / para o Git
        rel_path = rel_path.replace('\\', '/')
        
        # Executa o comando git log
        cmd = f'git -C "{REPO_PATH}" log --follow --oneline -- "{rel_path}" | find /c /v ""'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Extrai o número de commits
        commit_count = result.stdout.strip()
        return commit_count if commit_count.isdigit() else "0"
    except Exception as e:
        print(f"Erro ao processar {file_path}: {str(e)}")
        return "0"

# Lê o CSV e extrai os caminhos únicos dos arquivos
unique_files = set()
with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        file_path = row['file']
        if file_path and os.path.exists(file_path):
            unique_files.add(file_path)

# Processa cada arquivo e conta os commits
results = []
for file_path in sorted(unique_files):
    commit_count = get_commit_count(file_path)
    rel_path = os.path.relpath(file_path, REPO_PATH)
    results.append({
        'Arquivo': rel_path,
        'Commits': commit_count,
        'Caminho_Completo': file_path
    })
    print(f"Processado: {rel_path} - {commit_count} commits")

# Salva os resultados em um novo CSV
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
    fieldnames = ['Arquivo', 'Commits', 'Caminho_Completo']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"\nAnálise concluída! Resultados salvos em: {OUTPUT_FILE}")