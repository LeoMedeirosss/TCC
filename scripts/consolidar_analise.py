from collections import defaultdict

def consolidate_analysis():
    """Consolida a análise de code smells dos três projetos"""
    
    # Dados dos projetos
    grafana_data = {
        'total_files': 14,
        'avg_commits': 16.7,  # Média de commits do Grafana.txt
        'avg_authors': 5.4,   # Média de autores do Grafana.txt
        'smells': {
            'Large Component': 11,
            'Too many props': 8,
            'Inheritance instead of composition': 1
        }
    }
    
    metabase_data = {
        'total_files': 12,
        'avg_commits': 28.8,  # Média de commits do Metabase.txt
        'avg_authors': 7.4,   # Média de autores do Metabase.txt
        'smells': {
            'Large Component': 10,
            'Too many props': 6,
            'JSX outside the render method': 2,
            'Uncontrolled Component': 2
        }
    }
    
    react_data = {
        'total_files': 89,
        'avg_commits': 37.57,  # Média de commits do analise_componentes_smells.txt
        'avg_authors': 11.5,    # Média de autores do analise_componentes_smells.txt
        'smells': {
            'Direct DOM Manipulation': 51,
            'Large Component': 48,
            'JSX outside the render method': 36,
            'Too many props': 26,
            'Force Update': 12,
            'Uncontrolled component': 7,
            'Props in initial state': 3,
            'Inheritance instead of composition': 3
        }
    }
    
    # Consolidar dados
    total_files = grafana_data['total_files'] + metabase_data['total_files'] + react_data['total_files']
    consolidated_smells = defaultdict(int)
    
    # Somar ocorrências de cada tipo de smell
    for data in [grafana_data, metabase_data, react_data]:
        for smell, count in data['smells'].items():
            consolidated_smells[smell] += count
    
    # Calcular porcentagens
    print("ANÁLISE CONSOLIDADA DE CODE SMELLS")
    print("=" * 60)
    print(f"Total de arquivos analisados: {total_files}")
    print(f"  - Grafana: {grafana_data['total_files']} arquivos")
    print(f"  - Metabase: {metabase_data['total_files']} arquivos")
    print(f"  - React: {react_data['total_files']} arquivos")
    print()
    
    print("Distribuição por tipo de Code Smell:")
    print("-" * 50)
    
    # Ordenar por frequência
    sorted_smells = sorted(consolidated_smells.items(), key=lambda x: x[1], reverse=True)
    
    for smell, count in sorted_smells:
        percentage = (count / total_files) * 100
        print(f"{smell}: {count} ocorrências ({percentage:.1f}% dos arquivos)")
    
    print()
    print("Análise por projeto:")
    print("=" * 30)
    
    # Análise individual por projeto
    for project_name, data in [("Grafana", grafana_data), ("Metabase", metabase_data), ("React", react_data)]:
        print(f"\n{project_name} ({data['total_files']} arquivos):")
        print("-" * 25)
        for smell, count in sorted(data['smells'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / data['total_files']) * 100
            print(f"  {smell}: {count} ({percentage:.1f}%)")
    
    print()
    print("ANÁLISE FINAL CONSOLIDADA")
    print("=" * 50)
    
    # Calcular médias ponderadas
    weighted_avg_commits = (
        (grafana_data['avg_commits'] * grafana_data['total_files']) +
        (metabase_data['avg_commits'] * metabase_data['total_files']) +
        (react_data['avg_commits'] * react_data['total_files'])
    ) / total_files
    
    weighted_avg_authors = (
        (grafana_data['avg_authors'] * grafana_data['total_files']) +
        (metabase_data['avg_authors'] * metabase_data['total_files']) +
        (react_data['avg_authors'] * react_data['total_files'])
    ) / total_files
    
    print(f"Média ponderada de commits por arquivo: {weighted_avg_commits:.2f}")
    print(f"Média ponderada de autores por arquivo: {weighted_avg_authors:.2f}")
    print()
    
    print("Resumo das médias por projeto:")
    print("-" * 30)
    for project_name, data in [("Grafana", grafana_data), ("Metabase", metabase_data), ("React", react_data)]:
        print(f"{project_name}:")
        print(f"  - Média commits: {data['avg_commits']}")
        print(f"  - Média autores: {data['avg_authors']}")
        print(f"  - Total arquivos: {data['total_files']}")
        print()
    
    print("Principais insights:")
    print("-" * 20)
    
    # Insights específicos
    print("1. Code Smells mais comuns em todos os projetos:")
    top_smells = sorted_smells[:3]
    for i, (smell, count) in enumerate(top_smells, 1):
        print(f"   {i}. {smell}: {count} ocorrências ({(count/total_files)*100:.1f}%)")
    
    print()
    print("2. Large Component é predominante:")
    large_component_total = (consolidated_smells.get('Large Component', 0) / total_files) * 100
    print(f"   - Presente em {large_component_total:.1f}% de todos os arquivos")
    
    print()
    print("3. Problemas específicos por projeto:")
    print("   - React: Direct DOM Manipulation é o smell mais frequente")
    print("   - Metabase: Large Component afeta 83% dos arquivos")
    print("   - Grafana: Large Component afeta 78% dos arquivos")
    
    print()
    print("4. Análise de colaboração:")
    print(f"   - React tem a maior média de autores ({react_data['avg_authors']})")
    print(f"   - React tem a maior média de commits ({react_data['avg_commits']})")
    print(f"   - Grafana tem as menores médias, indicando código mais focado")
    
    return consolidated_smells, total_files, weighted_avg_commits, weighted_avg_authors

if __name__ == "__main__":
    consolidate_analysis()
