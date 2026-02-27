## Arquitetura Medallion

### 🥉 Bronze Layer
- Consome dados brutos da API FakeStore
- Armazena dados em formato bruto dentro do container Docker
- Mantém fidelidade total à fonte original

### 🥈 Silver Layer
- Limpeza e padronização dos dados
- Normalização de estruturas
- Persistência em PostgreSQL

### 🥇 Gold Layer
🚧 Ainda não implementada  

Planejada para conter:
- Agregações analíticas
- Métricas de negócio
- Tabelas otimizadas para BI


## 🛠 Tecnologias Utilizadas

- **Python** (Requests, Pandas, SQLAlchemy)
- **PostgreSQL**
- **Apache Airflow**
- **Docker & Docker Compose**
- **Arquitetura Medallion (Bronze/Silver/Gold)**


## 📂 Estrutura do Projeto
```
data-engineering-fakestore/
├── README.md
├── requirements.txt
├── src/
│ ├── ingestion/
│ ├── loading/
│ ├── transformation_silver/
│ └── transformation_gold/ (planejado)
├── data/
│ ├── bronze/
│ ├── silver/
│ └── gold/
├── airflow/
│ ├── dags/
│ ├── docker-compose.yml
```
## 🐳 Executando o Projeto

O `docker-compose.yml` está localizado dentro da pasta `airflow/`.

### Subir ambiente:

```bash
cd airflow
docker compose up --build
```

## 🔐 Variáveis de Ambiente
Criar arquivo .env na raiz do projeto com:
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
```

## 🚀 Pipeline de Dados
O pipeline realiza:

* Extração de dados da API FakeStore
* Armazenamento bruto (Bronze)
* Transformação e limpeza (Silver)
* Carga estruturada no PostgreSQL
* Orquestração via Airflow

## 📌 Roadmap / Melhorias Futuras

- [ ] Implementar camada Gold
- [ ] Criar agregações analíticas
- [ ] Adicionar testes automatizados
- [ ] Implementar logging estruturado
- [ ] Deploy em cloud (AWS/GCP)
- [ ] Implementar CI/CD

## 🎯 Objetivo do Projeto

Demonstrar conhecimento em:

- Arquitetura de pipelines de dados
- Organização em camadas (Medallion Architecture)
- Orquestração com Airflow
- Persistência em banco relacional
- Boas práticas de versionamento
- Estruturação de projeto para produção



## ⚙️ Estratégia de Carga – Parâmetros do Airflow

O pipeline foi configurado para permitir diferentes estratégias de extração através de parâmetros na DAG do Airflow.

A função `extract_products()` suporta três modos de execução:

- **Full Load**
- **Range Load**
- **Incremental Load (padrão)**

---

### 🥉 1️⃣ Full Load (`mode="full"`)

Realiza uma carga completa dos dados disponíveis na API.

- Remove todos os dados existentes no arquivo Bronze
- Reprocessa todos os IDs disponíveis na FakeStore (1–20)
- Sobrescreve o arquivo `products.json`

📌 Uso recomendado:
- Primeira carga
- Reprocessamento total
- Correção de inconsistências

### 🔢 2️⃣ Range Load (`mode="range"`)

Permite reprocessar um intervalo específico de IDs.

Parâmetros necessários:
- `min_id`
- `max_id`

O pipeline irá:
- Buscar apenas os IDs dentro do intervalo informado
- Atualizar ou substituir esses registros no Bronze

📌 Uso recomendado:
- Correção de registros específicos
- Reprocessamento controlado
- Testes

### 📈 3️⃣ Incremental Load (padrão)

Se nenhum parâmetro for informado, o pipeline executa automaticamente em modo incremental.

Comportamento:

- Verifica os IDs já existentes no arquivo Bronze
- Identifica o próximo ID disponível
- Busca apenas o novo registro
- Mantém os dados já existentes

📌 Esse é o comportamento padrão da DAG.

## 🎯 Benefícios da Abordagem

- Flexibilidade operacional
- Reprocessamento controlado
- Suporte a cargas completas e incrementais
- Maior controle sobre ingestão de dados
- Simula cenários reais de engenharia de dados