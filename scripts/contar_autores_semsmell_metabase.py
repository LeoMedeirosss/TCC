import os
import subprocess
from pathlib import Path

def count_authors(repo_path, filepath):
    """Conta o número de autores únicos de um arquivo"""
    try:
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
    
    # Lista de arquivos sem code smells com seus caminhos encontrados
    files_without_smells = [
        ("LoginHistory.jsx", "frontend/src/metabase/account/login-history/components/LoginHistory/LoginHistory.jsx"),
        ("AdminNav.tsx", "frontend/src/metabase/admin/components/AdminNav/AdminNav.tsx"),
        ("PasswordButton.tsx", "frontend/src/metabase/auth/components/PasswordButton/PasswordButton.tsx"),
        ("CollectionMenu.tsx", "frontend/src/metabase/collections/components/CollectionMenu/CollectionMenu.tsx"),
        ("FormRadioGroup.tsx", "frontend/src/metabase/forms/components/FormRadioGroup/FormRadioGroup.tsx"),
        ("CurrencyPicker.tsx", "frontend/src/metabase/metadata/components/CurrencyPicker/CurrencyPicker.tsx"),
        ("DropdownSidebarFilter.tsx", "frontend/src/metabase/search/components/DropdownSidebarFilter/DropdownSidebarFilter.tsx"),
        ("FormCollectionPicker.tsx", "frontend/src/metabase/collections/containers/FormCollectionPicker/FormCollectionPicker.tsx"),
        ("CreateCollectionModal.tsx", "frontend/src/metabase/collections/containers/CreateCollectionModal.tsx"),
        ("UploadOverlay.tsx", "frontend/src/metabase/collections/components/UploadOverlay/UploadOverlay.tsx"),
        ("UpsellWhitelabel.tsx", "frontend/src/metabase/admin/upsells/UpsellWhitelabel.tsx"),
        ("UpsellStorage.tsx", "frontend/src/metabase/admin/upsells/UpsellStorage.tsx")
    ]
    
    print("Analisando arquivos SEM code smells...")
    print("=" * 60)
    
    results = []
    total_authors = 0
    
    for i, (filename, filepath) in enumerate(files_without_smells, 1):
        count, authors, error = count_authors(repo_path, filepath)
        
        if error:
            print(f"{i}. {filename}: {error}")
            results.append((filename, 0, []))
        else:
            authors_str = ", ".join(authors)
            print(f"{i}. {filename}: {count} autores")
            results.append((filename, count, authors))
            total_authors += count
    
    # Calcula a média
    valid_results = [r for r in results if r[1] > 0]
    if valid_results:
        avg_authors = total_authors / len(valid_results)
        print(f"\nMédia de autores em arquivos sem code smell: {avg_authors:.1f} autores")
    else:
        print("\nNão foi possível calcular a média de autores")
    
    # Gera o texto para atualizar o arquivo
    print("\n" + "=" * 60)
    print("Texto para atualizar o Metabase.txt:")
    print("=" * 60)
    
    print("    Alguns arquivos que não foram encontrados code smells:")
    for filename, count, authors in results:
        if count == 1:
            autor_text = f"{count} autor"
        else:
            autor_text = f"{count} autores"
        print(f"        {filename} - {autor_text}")

if __name__ == "__main__":
    main()
