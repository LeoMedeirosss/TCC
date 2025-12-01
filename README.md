# 📄 Análises do Estudo de Code Smells em Aplicações React

Este repositório reúne todos os arquivos, resultados e scripts utilizados durante a condução das análises do Trabalho de Conclusão de Curso (TCC) sobre *code smells em aplicações React*. A pasta contém tanto os dados brutos extraídos automaticamente quanto as análises consolidadas manualmente.

---

## 📁 Estrutura dos Arquivos

### 🔹 1. Pastas por Repositório Analisado

Cada repositório open-source analisado possui sua própria pasta:

- `carbon/`
- `grafana/`
- `metabase/`
- `redash/`
- `prometheus/`

Além disso, todos os repositórios acima foram clonados, porém, por questões de tamanho, não estão presentes nesse repositório

Dentro de cada pasta encontram-se:

| Arquivo | Descrição |
|--------|-----------|
| `analise_<repo>_clean_components.txt` | Análise manual dos componentes **sem code smells**. |
| `analise_<repo>_smells.txt` | Análise manual dos componentes **com code smells**. |
| `component_smells_<repo>.csv` | Arquivo **gerado automaticamente pelo ReactSniffer**, contendo os smells detectados. |
(Grafana e Metabase tem a análise mais detalhada dos autores)

📌 *Todos os arquivos `.csv` foram produzidos pela ferramenta ReactSniffer.*

---

### 🔹 2. Scripts Python Utilizados

O repositório contém scripts criados para automatizar partes do processo de análise:

| Script | Função |
|--------|--------|
| `contar_commits_<repo>.py` | Conta o número de commits por arquivo com `git log --oneline path | wc -l`. |
| `contar_autores_<repo>.py` | Conta autores distintos de cada arquivo usando `git log --format='%an' path | sort | uniq | wc -l`. |
| `contar_autores_semsmell_<repo>.py` | Versão adaptada para arquivos **sem code smells**. |
| `consolidar_arquivos_limpos.py` | Consolida todos os arquivos sem smells dos repositórios. |
| `consolidar_analise.py` | Consolida todos os arquivos com smells. |
| `analise_completa_<repo>.py` | Executa o ciclo completo de análise para cada repositório. |

Os scripts foram produzidos parcialmente com apoio de Inteligência Artificial e ajustados manualmente para cada projeto.

---

### 🔹 3. Análise Final

| Arquivo | Descrição |
|---------|-----------|
| `analise_final.txt` | Documento final consolidando os achados, escrito com auxílio de IA e revisado manualmente. |

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

- **Python** — automação, extração de métricas e manipulação de arquivos.  
- **ReactSniffer** — ferramenta principal de detecção automática de code smells.  
- **Git** — utilizado para calcular commits e autores por arquivo.  
- **VS Code** — utilizado para edição de scripts e organização das análises.  
- Arquivos **.txt** — usados para armazenar resultados parciais ao longo do processo.

---

## 📌 Observações Importantes

- Os arquivos `.csv` são resultados **diretos** do ReactSniffer.  
- As análises em `.txt` foram cuidadosamente revisadas manualmente para corrigir falhas da ferramenta.  
- A combinação entre inspeção manual e dados automatizados garantiu maior precisão na análise.

---
