## Medallion Architecture

### 🥉 Bronze Layer
- Consumes raw data from the FakeStore API
- Stores data in raw format within the Docker container
- Maintains complete fidelity to the original source

### 🥈 Silver Layer
- Data cleaning and standardization
- Structure normalization
- Persistence in PostgreSQL

### 🥇 Gold Layer
🚧 Not yet implemented  

Planned to contain:
- Analytical aggregations
- Business metrics
- Optimized tables for BI


## 🛠 Technologies Used

- **Python** (Requests, Pandas, SQLAlchemy)
- **PostgreSQL**
- **Apache Airflow**
- **Docker & Docker Compose**
- **Medallion Architecture (Bronze/Silver/Gold)**


## 📂 Project Structure
```
data-engineering-fakestore/
├── README.md
├── requirements.txt
├── src/
│ ├── ingestion/
│ ├── loading/
│ ├── transformation_silver/
│ └── transformation_gold/ (planned)
├── data/
│ ├── bronze/
│ ├── silver/
│ └── gold/
├── airflow/
│ ├── dags/
│ ├── docker-compose.yml
```
## 🐳 Running the Project

The `docker-compose.yml` is located inside the `airflow/` folder.

### Starting the environment:

```bash
cd airflow
docker compose up --build
```

## 🔐 Environment Variables
Create a .env file at the project root with:
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
```

## 🚀 Data Pipeline
The pipeline performs:

* Extraction of data from the FakeStore API
* Raw storage (Bronze)
* Transformation and cleaning (Silver)
* Structured loading into PostgreSQL
* Orchestration via Airflow

## 📌 Roadmap / Future Improvements

- [ ] Implement Gold layer
- [ ] Create analytical aggregations
- [ ] Add automated testing
- [ ] Implement structured logging
- [ ] Cloud deployment (AWS/GCP)
- [ ] Implement CI/CD

## 🎯 Project Objective

Demonstrate expertise in:

- Data pipeline architecture
- Layered organization (Medallion Architecture)
- Orchestration with Airflow
- Relational database persistence
- Version control best practices
- Production-ready project structure



## ⚙️ Load Strategy – Airflow Parameters

The pipeline was configured to allow different extraction strategies through parameters in the Airflow DAG.

The `extract_products()` function supports three execution modes:

- **Full Load**
- **Range Load**
- **Incremental Load (default)**

---

### 1️⃣ Full Load (`mode="full"`)

Performs a complete load of all available data from the API.

- Removes all existing data in the Bronze file
- Reprocesses all IDs available in FakeStore (1–20)
- Overwrites the `products.json` file

📌 Recommended use:
- First load
- Full reprocessing
- Inconsistency correction

### 🔢 2️⃣ Range Load (`mode="range"`)

Allows reprocessing a specific range of IDs.

Required parameters:
- `min_id`
- `max_id`

The pipeline will:
- Fetch only IDs within the specified range
- Update or replace those records in Bronze

📌 Recommended use:
- Correction of specific records
- Controlled reprocessing
- Testing

### 📈 3️⃣ Incremental Load (default)

If no parameters are provided, the pipeline automatically executes in incremental mode.

Behavior:

- Checks IDs already present in the Bronze file
- Identifies the next available ID
- Fetches only the new record
- Preserves existing data

📌 This is the default DAG behavior.

## 🎯 Benefits of This Approach

- Operational flexibility
- Controlled reprocessing
- Support for full and incremental loads
- Greater control over data ingestion
- Simulates real data engineering scenarios