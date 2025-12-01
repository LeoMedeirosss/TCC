import os
import subprocess
from pathlib import Path
import csv

def count_authors(repo_path, file_path):
    """Conta o número de autores únicos de um arquivo"""
    try:
        # Verifica se o arquivo existe
        full_path = Path(repo_path) / file_path
        if not full_path.exists():
            return 0, []
            
        # Executa o comando git para obter os autores
        cmd = f'git -C "{repo_path}" log --follow --format="%an" -- "{file_path}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Processa os resultados
        authors = [a.strip() for a in result.stdout.splitlines() if a.strip()]
        unique_authors = list(set(authors))  # Remove duplicados
        
        return len(unique_authors), unique_authors
    except Exception as e:
        print(f"Erro ao processar {file_path}: {str(e)}")
        return 0, []

def main():
    # Configurações
    repo_path = r"C:\Users\leozi\OneDrive\Área de Trabalho\Analise\RepositoriosClonados\grafana"
    output_file = r"C:\Users\leozi\OneDrive\Área de Trabalho\Analise\RepositoriosClonados\analises\grafana\analise_autores.csv"
    
    # Lista de arquivos com code smells
    files_with_smells = [
        "public/app/core/components/AppChrome/History/HistoryWrapper.tsx",
        "packages/grafana-ui/src/components/Combobox/Combobox.test.tsx",
        "packages/grafana-ui/src/components/Table/TableNG/Filter/FilterPopup.tsx",
    ]
    
    # Lista de arquivos sem code smells
    files_without_smells = [
        "public/app/plugins/panel/xychart/XYChartPanel.tsx",
        "public/app/plugins/panel/welcome/Welcome.tsx",
        "public\app\features\dashboard\components\DashboardPermissions\AccessControlDashboardPermissions.tsx",
        "public/app/plugins/panel/trend/TrendPanel.tsx",
        "public/app/plugins/panel/traces/TracesPanel.tsx",
        "public\app\features\dashboard\components\VersionHistory\VersionHistoryComparison.tsx",
        "public\app\core\components\ValidationLabels\ValidationLabels.tsx",
        "public\app\features\visualization\data-hover\DataHoverRows.tsx",
        "public\app\features\visualization\data-hover\DataHoverTabs.tsx",
        "public\app\features\geo\editor\GazetteerPathEditor.tsx"
    ]
    
    # Cabeçalho do CSV
    results = [["Arquivo", "Tem Code Smell", "Número de Autores", "Autores"]]
    
    # Processa arquivos com code smells
    for file in files_with_smells:
        count, authors = count_authors(repo_path, file)
        results.append([file, "Sim", count, ", ".join(authors)])
    
    # Processa arquivos sem code smells
    for file in files_without_smells:
        count, authors = count_authors(repo_path, file)
        results.append([file, "Não", count, ", ".join(authors)])
    
    # Salva os resultados em CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(results)
    
    print(f"Análise concluída. Resultados salvos em: {output_file}")

if __name__ == "__main__":
    main()