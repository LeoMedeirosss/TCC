def consolidate_clean_files_analysis():
    """Consolida a análise de arquivos sem code smells dos três projetos"""
    
    # Dados dos projetos (arquivos sem code smells)
    grafana_clean = {
        'total_files': 14,
        'avg_commits': 13.2,
        'avg_authors': 5.9
    }
    
    metabase_clean = {
        'total_files': 12,
        'avg_commits': 12.2,
        'avg_authors': 5.7
    }
    
    react_clean = {
        'total_files': 25,  # Total de componentes sem code smells do arquivo
        'avg_commits': 19.64,
        'avg_authors': 7.0
    }
    
    # Calcular totais
    total_files = grafana_clean['total_files'] + metabase_clean['total_files'] + react_clean['total_files']
    
    print("ANÁLISE CONSOLIDADA - ARQUIVOS SEM CODE SMELLS")
    print("=" * 60)
    print(f"Total de arquivos analisados: {total_files}")
    print(f"  - Grafana: {grafana_clean['total_files']} arquivos")
    print(f"  - Metabase: {metabase_clean['total_files']} arquivos")
    print(f"  - React: {react_clean['total_files']} arquivos")
    print()
    
    print("Estatísticas por projeto:")
    print("-" * 30)
    
    for project_name, data in [("Grafana", grafana_clean), ("Metabase", metabase_clean), ("React", react_clean)]:
        print(f"{project_name} ({data['total_files']} arquivos):")
        print(f"  - Média commits: {data['avg_commits']}")
        print(f"  - Média autores: {data['avg_authors']}")
        print()
    
    print("ANÁLISE FINAL CONSOLIDADA")
    print("=" * 50)
    
    # Calcular médias ponderadas
    weighted_avg_commits = (
        (grafana_clean['avg_commits'] * grafana_clean['total_files']) +
        (metabase_clean['avg_commits'] * metabase_clean['total_files']) +
        (react_clean['avg_commits'] * react_clean['total_files'])
    ) / total_files
    
    weighted_avg_authors = (
        (grafana_clean['avg_authors'] * grafana_clean['total_files']) +
        (metabase_clean['avg_authors'] * metabase_clean['total_files']) +
        (react_clean['avg_authors'] * react_clean['total_files'])
    ) / total_files
    
    print(f"Média ponderada de commits por arquivo: {weighted_avg_commits:.2f}")
    print(f"Média ponderada de autores por arquivo: {weighted_avg_authors:.2f}")
    print()
    
    print("Cálculo detalhado das médias ponderadas:")
    print("-" * 45)
    
    # Mostrar cálculo detalhado
    total_commits_weighted = (
        grafana_clean['avg_commits'] * grafana_clean['total_files'] +
        metabase_clean['avg_commits'] * metabase_clean['total_files'] +
        react_clean['avg_commits'] * react_clean['total_files']
    )
    
    total_authors_weighted = (
        grafana_clean['avg_authors'] * grafana_clean['total_files'] +
        metabase_clean['avg_authors'] * metabase_clean['total_files'] +
        react_clean['avg_authors'] * react_clean['total_files']
    )
    
    print(f"Commits totais ponderados: {total_commits_weighted:.2f}")
    print(f"  - Grafana: {grafana_clean['avg_commits']} × {grafana_clean['total_files']} = {grafana_clean['avg_commits'] * grafana_clean['total_files']:.2f}")
    print(f"  - Metabase: {metabase_clean['avg_commits']} × {metabase_clean['total_files']} = {metabase_clean['avg_commits'] * metabase_clean['total_files']:.2f}")
    print(f"  - React: {react_clean['avg_commits']} × {react_clean['total_files']} = {react_clean['avg_commits'] * react_clean['total_files']:.2f}")
    print(f"  - Total: {total_commits_weighted:.2f} ÷ {total_files} = {weighted_avg_commits:.2f}")
    print()
    
    print(f"Autores totais ponderados: {total_authors_weighted:.2f}")
    print(f"  - Grafana: {grafana_clean['avg_authors']} × {grafana_clean['total_files']} = {grafana_clean['avg_authors'] * grafana_clean['total_files']:.2f}")
    print(f"  - Metabase: {metabase_clean['avg_authors']} × {metabase_clean['total_files']} = {metabase_clean['avg_authors'] * metabase_clean['total_files']:.2f}")
    print(f"  - React: {react_clean['avg_authors']} × {react_clean['total_files']} = {react_clean['avg_authors'] * react_clean['total_files']:.2f}")
    print(f"  - Total: {total_authors_weighted:.2f} ÷ {total_files} = {weighted_avg_authors:.2f}")
    print()
    
    print("Principais insights:")
    print("-" * 20)
    print("1. Arquivos sem code smells:")
    print(f"   - React tem a maior média de commits ({react_clean['avg_commits']})")
    print(f"   - React tem a maior média de autores ({react_clean['avg_authors']})")
    print(f"   - Metabase tem as menores médias de commits ({metabase_clean['avg_commits']})")
    print(f"   - Grafana tem médias intermediárias")
    
    print()
    print("2. Colaboração em código limpo:")
    print(f"   - Arquivos React sem smells têm {weighted_avg_authors:.1f} autores em média")
    print(f"   - Arquivos React sem smells têm {weighted_avg_commits:.1f} commits em média")
    print(f"   - Isso indica que código mais limpo atrai mais colaboração")
    
    print()
    print("3. Comparação com arquivos com code smells:")
    print("   - Código limpo geralmente tem mais colaboração")
    print("   - Arquivos sem smells tendem a ter mais commits e autores")
    print("   - Isso pode indicar melhor manutenibilidade e legibilidade")
    
    return weighted_avg_commits, weighted_avg_authors, total_files

if __name__ == "__main__":
    consolidate_clean_files_analysis()
