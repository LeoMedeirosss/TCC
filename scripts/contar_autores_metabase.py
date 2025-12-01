import os
import subprocess
from pathlib import Path
import csv

def count_authors(repo_path, filepath):
    """Conta o número de autores únicos de um arquivo"""
    try:
        # Verifica se o arquivo existe
        full_path = Path(repo_path) / filepath
        if not full_path.exists():
            return 0, [], "Arquivo não encontrado"
            
        # Executa o comando git para obter os autores
        cmd = f'git -C "{repo_path}" log --follow --format="%an" -- "{filepath}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Processa os resultados
        authors = [a.strip() for a in result.stdout.splitlines() if a.strip()]
        unique_authors = sorted(list(set(authors)))  # Remove duplicados e ordena
        
        return len(unique_authors), unique_authors, None
    except Exception as e:
        return 0, [], f"Erro: {str(e)}"

def main():
    # Configurações
    repo_path = r"C:\Users\leozi\OneDrive\Área de Trabalho\Analise\RepositoriosClonados\metabase"
    csv_input = r"C:\Users\leozi\OneDrive\Área de Trabalho\Analise\RepositoriosClonados\analises\metabase\components_smells_metabase.csv"
    output_file = r"C:\Users\leozi\OneDrive\Área de Trabalho\Analise\RepositoriosClonados\analises\metabase\analise_autores_metabase_from_csv.csv"
    
    # Lê o arquivo CSV de entrada
    files_data = []
    try:
        with open(csv_input, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Pula o cabeçalho (primeiras 3 linhas)
            for _ in range(3):
                next(reader, None)
            
            for row in reader:
                if len(row) >= 4:
                    # Extrai o caminho do arquivo (coluna 2, índice 1)
                    full_path = row[1]
                    # Extrai o nome do arquivo
                    filename = Path(full_path).name
                    # Determina se tem code smell (todos neste CSV têm)
                    has_smell = "Sim"
                    
                    files_data.append({
                        'filename': filename,
                        'full_path': full_path,
                        'has_smell': has_smell
                    })
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {str(e)}")
        return
    
    # Cabeçalho do CSV de saída
    results = [["Arquivo", "Caminho", "Tem Code Smell", "Número de Autores", "Autores"]]
    
    print(f"Processando {len(files_data)} arquivos com code smells...")
    
    for i, file_data in enumerate(files_data, 1):
        # Converte o caminho absoluto para relativo ao repositório
        abs_path = file_data['full_path']
        if abs_path.startswith(repo_path):
            rel_path = os.path.relpath(abs_path, repo_path)
        else:
            # Se não começar com o caminho do repo, tenta extrair a parte relativa
            if "metabase" in abs_path:
                rel_path = abs_path.split("metabase", 1)[1].lstrip("\\/")
            else:
                rel_path = Path(abs_path).name
        
        count, authors, error = count_authors(repo_path, rel_path)
        
        if error:
            print(f"{i}. {file_data['filename']}: {error}")
            results.append([file_data['filename'], rel_path, file_data['has_smell'], 0, error])
        else:
            print(f"{i}. {file_data['filename']}: {count} autores")
            results.append([file_data['filename'], rel_path, file_data['has_smell'], count, ", ".join(authors)])
    
    # Salva os resultados em CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(results)
        
        print(f"\nAnálise concluída. Resultados salvos em: {output_file}")
        print(f"Total de arquivos processados: {len(files_data)}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo de saída: {str(e)}")

if __name__ == "__main__":
    main()
