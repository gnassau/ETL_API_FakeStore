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
