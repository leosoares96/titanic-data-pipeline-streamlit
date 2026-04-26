# Arquitetura de Dados — Titanic Data Pipeline (completo)

## 1. Visão Geral

Pipeline local e reprodutível que ingere o dataset público do Titanic, aplica limpeza e engenharia de features com Pandas, executa checagens de qualidade, persiste resultados (Parquet + SQLite) e expõe um dashboard interativo com Streamlit + Plotly. Projetado para aprendizado, validação de conceitos e análises exploratórias.

## 2. Objetivos

- Garantir reprodutibilidade de execuções batch.
- Fornecer dados processados prontos para análise e visualização.
- Manter código modular e testável (extract/transform/quality/load).
- Permitir execução fácil em máquina local (Windows).

## 3. Escopo

Inclui extração do CSV público, armazenamento de snapshot raw, transformação determinística, validações básicas de qualidade, persistência em Parquet e SQLite, e um app Streamlit para consumo. Não cobre orquestração distribuída, alta disponibilidade ou ingestão em tempo real.

## 4. Camadas e Componentes

- Data Source
  - CSV público (ex.: URL do repositório ou Kaggle).
- Ingestão (src/extract.py)
  - Baixa/valida/gera snapshots em data/raw/.
- Raw Layer (data/raw/)
- Processamento / Transform (src/transform.py)
  - Limpeza, tipagem, normalização, criação de colunas (ex.: faixa etária, indicadores).
- Validação de Qualidade (src/quality.py)
  - Regras de schema, presença de colunas, limites de nulos, unicidade de chave.
- Persistência (src/load.py)
  - Escrita em Parquet (data/processed/) e carga em SQLite (data/titanic.db).
- Serving (app/app.py)
  - Streamlit dashboard que consome SQLite e gera KPIs + gráficos Plotly.

## 5. Fluxo de Dados

`Data Source → src.extract → data/raw/{snapshot}.csv → src.transform → data/processed/{dataset}.parquet → src.quality → src.load → data/titanic.db (SQLite) → app/app.py (Streamlit)`

## 6. Contratos de Dados / Esquema esperado

Tabela `passengers` (exemplo de colunas padrão Titanic):

- passenger_id (int) — chave primária (pode ser índice original)
- survived (int: 0/1)
- pclass (int)
- name (string)
- sex (string)
- age (float)
- sibsp (int)
- parch (int)
- ticket (string)
- fare (float)
- cabin (string)
- embarked (string)
- processed_at (datetime) — timestamp de processamento

Contrato: tipos coerentes, colunas obrigatórias presentes, "survived" normalizado para int 0/1.

## 7. Regras de Qualidade e Validações

- Dataset não vazio após transformação.
- Colunas obrigatórias presentes: [passenger_id, survived, pclass, sex, age, fare].
- Percentual máximo de nulos por coluna (ex.: age <= 40% nulos) — regra configurável.
- Faixas plausíveis: age ∈ [0, 120], fare ≥ 0.
- Tipos coerentes (conversão segura com errors='coerce' seguida de validação).
- Checagem de duplicatas em passenger_id.
- Alertas/erros levantados em falha (ex.: exceção ou log de erro).

## 8. Observabilidade e Logs

- Logging centralizado em src/utils/logger.py (logs em console e arquivo).
- Métricas básicas:
  - Registros processados
  - Percentual de nulos por coluna
  - Tempo de execução por etapa

## 9. Segurança e Governança

- Dados locais; controlar permissões do diretório data/ (não versionar raw CSV em repo público).
- SQLite não é adequado para dados sensíveis em produção.
- Evitar exposição de dados pessoais no dashboard; anonimizar se necessário.
- Validar entradas do usuário no Streamlit para prevenir injeção de SQL (usar pandas.read_sql com parâmetros seguros).

## 10. Armazenamento e Retenção

- Raw snapshots: conservar N últimas execuções (configurável).
- Processed Parquet: manter histórico por versão (ou sobrescrever em pipelines idempotentes).
- SQLite: banco analítico local; backup periódico recomendado (cópia do .db).
- Recomendação: mover para S3/Blob + Athena/BigQuery para escala.

## 11. Execução Local (Runbook — Windows)

1. Criar e ativar venv:
   - python -m venv venv
   - venv\Scripts\activate
2. Instalar dependências:
   - python -m pip install -r requirements.txt
3. Executar pipeline (gera Parquet e SQLite):
   - python main.py
4. Rodar dashboard Streamlit:
   - streamlit run app/app.py
5. Ver logs:
   - type logs\pipeline.log (ou abrir em editor)

## 12. Testes e Qualidade de Código

- Unit tests para:
  - src.extract: teste com URL mock / arquivo local.
  - src.transform: casos com valores nulos e tipos incorretos.
  - src.quality: validação de regras com dataframes de exemplo.
  - src.load: escrita/lesura em SQLite temporário.
- Recomendações:
  - Usar pytest; fixtures para sample CSVs.
  - Coverage target mínimo: 70%.

## 13. CI / CD

- Pipeline de CI (GitHub Actions) sugerido:
  - Lint (flake8/black)
  - Unit tests (pytest)
  - Build artifacts (opcional: wheel)
- CD: release manual; para produção, pipeline deve publicar artefatos e agendar execuções.

## 14. Trade-offs e Limitações

- Prós:
  - Simples, de fácil entendimento e execução local.
  - Boa plataforma para prototipagem e ensino.
- Contras:
  - Não escalável para grandes volumes.
  - Sem orquestração nem monitoramento de produção.
  - SQLite não é adequado para concorrência/alta carga.

## 15. Roadmap / Melhorias Sugeridas

- Adicionar orquestrador (Airflow/Prefect) + agendamento.
- Implementar ingestão incremental e CDC.
- Migrar armazenamento processado para Parquet em S3 e usar Athena/BigQuery.
- Adicionar data versioning (DVC or Delta Lake).
- Implementar alertas (email/Slack) em falha de qualidade.
- Containerizar (Docker) e adicionar deployment scripts.

## 16. Mapeamento de Arquivos (projeto atual)

- main.py — orquestra pipeline local
- app/app.py — Streamlit dashboard
- src/extract.py — extração e snapshot
- src/transform.py — limpeza e engenharia de features
- src/quality.py — validação de regras
- src/load.py — persistência Parquet/SQLite
- src/utils/config.py — configurações (paths, limites)
- src/utils/logger.py — logging
- data/raw/ — CSVs brutos
- data/processed/ — Parquet processados
- data/titanic.db — SQLite final
- requirements.txt — dependências

## 17. Referências rápidas

- Como rodar: ver seção 11 (Windows)
- Para inspecionar dados: abrir data/titanic.db com DB Browser for SQLite
- Para editar dashboard: app/app.py (Streamlit recarrega automaticamente)

---

Documento criado para ser usado como referência técnica e base para evolução do projeto. Substitua parâmetros (limiares de nulos, políticas de retenção) conforme necessidade operacional.
