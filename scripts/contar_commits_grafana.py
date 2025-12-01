import subprocess
import os

# Caminho para o repositório
REPO_PATH = r"C:\Users\leozi\OneDrive\Área de Trabalho\Analise\RepositoriosClonados\grafana"

# Mapeamento dos arquivos para seus caminhos completos
FILE_PATHS = {
    "HistoryWrapper.tsx": "packages/grafana-runtime/src/services/LocationService.tsx",
    "ControlledCombobox.tsx": "packages/grafana-ui/src/components/Combobox/Combobox.test.tsx",  # Adicionado
    "Combobox.tsx": "packages/grafana-ui/src/components/Combobox/Combobox.tsx",
    "FilterPopup.tsx": "packages/grafana-ui/src/components/Table/TableNG/Filter/FilterPopup.tsx",  # Adicionado
    "DataSourceRuleListItem.tsx": "public/app/features/alerting/unified/rule-list/DataSourceRuleListItem.tsx",
    "DashboardEditPaneSplitter.tsx": "public/app/features/dashboard-scene/edit-pane/DashboardEditPaneSplitter.tsx",
    "AutoGridItem.tsx": "public/app/features/dashboard-scene/scene/layout-auto-grid/AutoGridItem.tsx",
    "DashboardGridItem.tsx": "public/app/features/dashboard-scene/scene/layout-default/DashboardGridItem.tsx",
    "RowItem.tsx": "public/app/features/dashboard-scene/scene/layout-rows/RowItem.tsx",
    "TabItem.tsx": "public/app/features/dashboard-scene/scene/layout-tabs/TabItem.tsx",
    "LogsQueryBuilder.tsx": "public/app/plugins/datasource/azuremonitor/components/LogsQueryBuilder/LogsQueryBuilder.tsx",
    "OrderBySection.tsx": "public/app/plugins/datasource/azuremonitor/components/LogsQueryBuilder/OrderBySection.tsx",
    "TableSection.tsx": "public/app/plugins/datasource/azuremonitor/components/LogsQueryBuilder/TableSection.tsx"
}

def get_commit_count(file_path):
    """Retorna o número de commits para um arquivo específico"""
    try:
        cmd = f'git -C "{REPO_PATH}" log --follow --oneline -- "{file_path}" | find /c /v ""'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.stdout.strip().isdigit() else "0"
    except Exception as e:
        print(f"Erro ao processar {file_path}: {str(e)}")
        return "0"

# Conta os commits para cada arquivo
results = {}
for name, path in FILE_PATHS.items():
    full_path = os.path.join(REPO_PATH, path)
    if os.path.exists(full_path):
        commit_count = get_commit_count(path)
        results[name] = commit_count
        print(f"Processado: {name} - {commit_count} commits")
    else:
        print(f"Arquivo não encontrado: {path}")

# Exibe os resultados
print("\nResumo de commits por arquivo:")
for name, count in results.items():
    print(f"{name}: {count} commits")

# Atualiza o arquivo Grafana.txt
with open("Grafana.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("Grafana.txt", "w", encoding="utf-8") as f:
    for line in lines:
        line = line.strip()
        if "=" in line:
            file_name = line.split("=")[0].strip()
            if file_name in results:
                line = f"        {file_name} = {line.split('=')[1].strip()} - {results[file_name]} commits"
        f.write(line + "\n")

print("\nArquivo Grafana.txt atualizado com sucesso!")