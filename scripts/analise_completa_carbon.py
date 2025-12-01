import csv
from collections import defaultdict
import os
import subprocess
from pathlib import Path

def analyze_redash_components(csv_path, repo_path):
    # Dicionário para armazenar os dados dos componentes
    components = defaultdict(lambda: {
        'file': '',
        'smells': set(),
        'commit_count': 0,
        'author_count': 0
    })
    
    # Ler o arquivo CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            component = row['Component']
            file_path = row['file']
            smell = row['Smell']
            
            # Adiciona o smell ao componente
            components[component]['file'] = file_path
            components[component]['smells'].add(smell)
    
    # Contar commits e autores para cada arquivo
    for component, data in components.items():
        file_path = data['file']
        if not file_path:
            continue
            
        # Converter o caminho para relativo ao repositório
        rel_path = os.path.relpath(file_path, repo_path)
        
        try:
            # Contar número de commits
            commit_count = int(subprocess.check_output(
                ['git', 'log', '--follow', '--format=%H', '--', rel_path],
                cwd=repo_path,
                stderr=subprocess.STDOUT
            ).decode('utf-8').strip().count('\n')) + 1
            
            # Contar número de autores únicos
            authors = subprocess.check_output(
                ['git', 'log', '--follow', '--format=%aN', '--', rel_path],
                cwd=repo_path,
                stderr=subprocess.STDOUT
            ).decode('utf-8').strip().split('\n')
            
            author_count = len(set(authors))
            
            components[component]['commit_count'] = commit_count
            components[component]['author_count'] = author_count
            
        except subprocess.CalledProcessError as e:
            print(f"Erro ao processar {file_path}: {e}")
    
    return components

def generate_report(components, output_file):
    # Calcular estatísticas
    total_components = len(components)
    total_commits = sum(c['commit_count'] for c in components.values())
    total_authors = sum(c['author_count'] for c in components.values())
    avg_commits = total_commits / total_components if total_components > 0 else 0
    avg_authors = total_authors / total_components if total_components > 0 else 0
    
    # Contar ocorrências de cada smell
    smell_counts = defaultdict(int)
    for component in components.values():
        for smell in component['smells']:
            smell_counts[smell] += 1
    
    # Gerar o relatório
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Redash - Análise de Componentes com Code Smells\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Total de componentes analisados: {total_components}\n")
        f.write(f"Média de commits por componente: {avg_commits:.2f}\n")
        f.write(f"Média de autores por componente: {avg_authors:.2f}\n\n")
        
        f.write("Distribuição de Code Smells:\n")
        f.write("-" * 50 + "\n")
        for smell, count in sorted(smell_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_components) * 100
            f.write(f"{smell}: {count} ocorrências ({percentage:.1f}% dos componentes)\n")
        
        f.write("\nDetalhes por componente:\n")
        f.write("=" * 80 + "\n")
        for component, data in sorted(components.items(), key=lambda x: x[1]['commit_count'], reverse=True):
            f.write(f"\nComponente: {component}\n")
            f.write(f"Arquivo: {data['file']}\n")
            f.write(f"Commits: {data['commit_count']}\n")
            f.write(f"Autores: {data['author_count']}\n")
            f.write("Code Smells:\n")
            for smell in data['smells']:
                f.write(f"  - {smell}\n")
    
    print(f"Relatório gerado em: {output_file}")

if __name__ == "__main__":
    # Caminhos
    base_dir = Path(__file__).parent.parent.parent
    csv_path = base_dir / "analises" / "carbon" / "components_smells_carbon.csv"
    repo_path = base_dir / "carbon"
    output_file = base_dir / "analises" / "carbon" / "analise_carbon_smells.txt"
    
    # Criar diretório de saída se não existir
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Executar análise
    components = analyze_redash_components(csv_path, repo_path)
    generate_report(components, output_file)