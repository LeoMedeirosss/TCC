import os
import random
import subprocess
from pathlib import Path
from collections import defaultdict

def find_react_components(repo_path, exclude_dirs=None, exclude_files=None):
    """Encontra arquivos React (.jsx, .tsx) no repositório, excluindo diretórios e arquivos específicos"""
    if exclude_dirs is None:
        exclude_dirs = {'node_modules', 'dist', 'migrations', 'test', 'tests', 'build', 'config',"cypress","api","svg", "lib"}
    if exclude_files is None:
        exclude_files = set()
    
    react_components = []
    
    for root, dirs, files in os.walk(repo_path):
        # Remove diretórios que devem ser ignorados
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith(('.js','.jsx', '.tsx')):
                file_path = os.path.join(root, file)
                if file_path not in exclude_files:
                    react_components.append(file_path)
    
    return react_components

def get_commit_and_author_count(file_path, repo_path):
    """Obtém o número de commits e autores únicos de um arquivo"""
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
        
        return commit_count, author_count
    except subprocess.CalledProcessError as e:
        print(f"Erro ao processar {file_path}: {e}")
        return 0, 0

def analyze_clean_components(repo_path, output_file, base_dir, sample_size=20):
    try:
        # Obter arquivos com code smells para excluí-los
        with open(str(base_dir / 'analises' / 'carbon' / 'components_smells_carbon.csv'), 'r', encoding='utf-8') as f:
            smelly_files = {line.split(',')[1].strip('"') for line in f if not line.startswith('id,file')}
    except FileNotFoundError:
        print(f"Arquivo de code smells não encontrado em: {base_dir / 'analises' / 'carbon' / 'components_smells_carbon.csv'}")
        return
    
    # Encontrar todos os componentes React
    all_components = find_react_components(repo_path)
    
    if not all_components:
        print("Nenhum componente React encontrado no diretório especificado.")
        return
    
    # Filtrar componentes sem code smells
    clean_components = [c for c in all_components if c not in smelly_files]
    
    if not clean_components:
        print("Nenhum componente sem code smells encontrado.")
        return
    
    # Amostrar aleatoriamente até sample_size componentes
    sample_size = min(sample_size, len(clean_components))
    sample = random.sample(clean_components, sample_size)
    
    # Coletar estatísticas
    results = []
    total_commits = 0
    total_authors = 0
    
    print(f"\nAnalisando {len(sample)} componentes...")
    for i, file_path in enumerate(sample, 1):
        print(f"Processando componente {i}/{len(sample)}: {os.path.basename(file_path)}")
        commit_count, author_count = get_commit_and_author_count(file_path, repo_path)
        component_name = os.path.splitext(os.path.basename(file_path))[0]
        
        results.append({
            'name': component_name,
            'file': file_path,
            'commits': commit_count,
            'authors': author_count
        })
        
        total_commits += commit_count
        total_authors += author_count
    
    # Gerar relatório
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Carbon - Análise de Componentes sem Code Smells\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Total de componentes analisados: {len(sample)}\n")
        f.write(f"Total de componentes React encontrados: {len(all_components)}\n")
        f.write(f"Total de componentes sem code smells: {len(clean_components)}\n\n")
        
        if sample:
            f.write(f"Média de commits por componente: {total_commits/len(sample):.2f}\n")
            f.write(f"Média de autores por componente: {total_authors/len(sample):.2f}\n\n")
        
        f.write("Detalhes por componente (ordenados por número de commits):\n")
        f.write("=" * 80 + "\n")
        
        if not results:
            f.write("\nNenhum componente para exibir.\n")
        else:
            for component in sorted(results, key=lambda x: x['commits'], reverse=True):
                f.write(f"\nComponente: {component['name']}\n")
                f.write(f"Arquivo: {component['file']}\n")
                f.write(f"Commits: {component['commits']}\n")
                f.write(f"Autores: {component['authors']}\n")
    
    print(f"\nRelatório gerado em: {output_file}")

if __name__ == "__main__":
    # Caminhos
    base_dir = Path(__file__).parent.parent.parent
    repo_path = base_dir / "carbon"
    output_file = base_dir / "analises" / "carbon" / "analise_carbon_clean_components.txt"
    
    # Criar diretório de saída se não existir
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Executar análise
    analyze_clean_components(repo_path, output_file, base_dir)