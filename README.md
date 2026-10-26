# 🛡️ NOCTRIX: Non-Human Identity Security Posture Management (ISPM)

**NOCTRIX** is a framework that continuously discovers Non-Human Identities (NHIs) — API keys, service accounts, IAM roles, and Kubernetes tokens — across multi-cloud and container environments, maps their blast radiuses in a Neo4j graph database, evaluates risk using a multi-factor equation, and automatically remediates high-risk identities.

---

## 🏗️ System Architecture

NOCTRIX is organized into 5 decoupled layers:
```
[ 1. Discovery ] ──> [ 2. Graph Ingestion ] ──> [ 3. Risk Engine ] ──> [ 4. Remediation ] ──> [ 5. Dashboard ]
  Parallel Scanners    Neo4j Database (MERGE)   Score R & Ghost Detect   Vault/AWS + Slack   Streamlit + Pyvis
```

1. **Discovery Layer (`discovery/`)**: Concurrent parallel scanning via `ThreadPoolExecutor` across AWS IAM (`boto3`), Kubernetes (`kubernetes` SDK), Git secrets (`TruffleHog CLI`), and Azure/GCP fixtures.
2. **Graph Persistence Layer (`graph/`)**: Idempotent Cypher `MERGE` ingestion into Neo4j modeling `USES`, `HAS_PERMISSION_ON`, and `CREATED_BY` relationships.
3. **Analysis & Risk Engine (`analysis/`)**: Multi-factor composite risk scoring ($R = 0.4P + 0.3E + 0.3A$) and 90-day orphaned Ghost Identity detection.
4. **Automated Remediation & Alerting (`remediation/`)**: Triggers HashiCorp Vault secret rotation and AWS IAM key deactivation (with safety allow-list guardrails) for identities with $R \ge 70$, dispatching alerts to Slack.
5. **Presentation Layer (`output/`)**: Live Streamlit dashboard with KPI cards, interactive Pyvis force-directed graph, and audit logs.

---

## 🔍 Live vs. Simulated Integrations

| Integration | Type | Description |
| :--- | :---: | :--- |
| **AWS IAM Scanner** | 🟢 Live | Real `boto3` scanning of roles, users, policies, and access keys |
| **Kubernetes Scanner** | 🟢 Live | Real Kubernetes SDK scanning against `kind` or `minikube` |
| **Secret Scanner** | 🟢 Live | Live `TruffleHog CLI` / regex scanning on git repositories |
| **Neo4j Graph DB** | 🟢 Live | Real Neo4j 5.x Community Edition instance in Docker |
| **Risk Scorer & Ghost Detector** | 🟢 Live | Real-time mathematical scoring and graph querying |
| **HashiCorp Vault Rotation** | 🟢 Live | Real secret rotation via `hvac` against Vault in Docker |
| **AWS Key Deactivation** | 🟢 Live | Real `boto3` key deactivation bounded by strict allow-list |
| **Slack Webhook Alerts** | 🟢 Live | Real HTTP POST alerts to Slack channels |
| **Streamlit Dashboard** | 🟢 Live | Interactive UI reading live from Neo4j |
| **Azure Service Principals** | 🟡 Fixture | Realistic JSON fixture matching Microsoft Graph API |
| **GCP Service Accounts** | 🟡 Fixture | Realistic JSON fixture matching Google Cloud IAM API |

---

## 🚀 Quickstart & Setup

### 1. Prerequisites
* Python 3.12+
* Docker & Docker Compose (for Neo4j and Vault)

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Local Neo4j & HashiCorp Vault Containers
```bash
docker compose up -d
```
* **Neo4j Browser**: `http://localhost:7474` (User: `neo4j`, Password: `password`)
* **Vault Web UI**: `http://localhost:8200` (Token: `root`)

### 4. Run the Full End-to-End Pipeline
```bash
python main.py
```

### 5. Launch the Interactive Dashboard
```bash
streamlit run output/dashboard.py
```

---

## 🧪 Running Automated Tests

Run the complete test suite with `pytest`:
```bash
pytest tests/ -v
```

---

## 🛡️ Safety Guardrails
* **Read-Only Scanners**: All discovery scanners only require read-only cloud permissions.
* **No Plaintext Secrets in Database**: Neo4j only stores metadata and risk scores; plaintext keys are never stored.
* **AWS Safety Allow-List**: Automated disabling of AWS keys is strictly restricted in code to the usernames specified in `config.yaml` (`remediation.aws.allowed_targets`).
