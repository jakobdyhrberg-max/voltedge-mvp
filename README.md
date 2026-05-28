# VoltEdge Charger Monitoring MVP

## Design og implementering af digitale løsninger – 6. Semester Eksamen

**Erhvervsakademi København**
Gruppe 19
Jakob Dyhrberg Adamsen & Tobias Nüchel Kristensen

---

# 1. Projektbeskrivelse

VoltEdge Charger Monitoring MVP er en cloud-native overvågningsplatform udviklet som en del af 6. semester eksamensprojektet i Design og implementering af digitale løsninger.

Projektet tager udgangspunkt i casen:

> VoltEdge Mobility A/S – Smart EV Charging Infrastructure

MVP’et adresserer virksomhedens mest kritiske operationelle udfordringer:

* Manglende observability
* Manuel incident-håndtering
* Ustabil telemetri
* Mangelfuld alarmering
* Begrænset realtime indsigt i ladestanderes tilstand

Løsningen overvåger EV-ladestandere i realtime ved hjælp af telemetridata og genererer automatisk alerts og incidents ved fejl, afvigelser eller risikoadfærd.

---

# 2. Strategisk kobling

Projektet er udviklet med direkte udgangspunkt i VoltEdges strategiske mål.

| Strategisk mål                 | Hvordan MVP’et understøtter målet                                       |
| ------------------------------ | ----------------------------------------------------------------------- |
| Scale Operations               | Automatiseret overvågning reducerer manuel drift                        |
| Data-driven Services           | Telemetridata analyseres aktivt og bruges til predictive maintenance    |
| Secure & Reliable Platform     | Logging, incidents og alerts skaber observability og sporbarhed         |
| Partner API Ecosystem          | API-first arkitektur muliggør fremtidige integrationer                  |
| Automated Billing & Settlement | Etablerer stabilt operationelt fundament for fremtidig settlement-logik |

MVP’et fokuserer bevidst på ét centralt bounded context:

> Charger Monitoring Context

Dette valg reducerer kompleksitet og gør det muligt at demonstrere en realistisk og velafgrænset implementering af Domain Driven Design.

---

# 3. Arkitektur

Løsningen er udviklet som en lagdelt cloud-native arkitektur med inspiration fra:

* Domain Driven Design (DDD)
* Clean Architecture
* DevSecOps
* Cloud-native design principles

## Arkitekturlag

```text
Swagger UI / Client
        ↓
FastAPI REST API Layer
        ↓
Application Layer
        ↓
Domain Layer
        ↓
Infrastructure Layer
        ↓
MySQL Database
        ↓
Power BI Analytics
```

---

# 4. Domain Driven Design

Projektet er designet omkring ét bounded context:

## Charger Monitoring Context

Contextet har ansvar for:

* Charger monitoring
* Telemetry ingestion
* Incident detection
* Alert generation
* Predictive maintenance

## Centrale domæneobjekter

| Rapportbegreb    | Kode               | Database             |
| ---------------- | ------------------ | -------------------- |
| Charger          | `Charger`          | `chargers`           |
| TelemetryReading | `TelemetryReading` | `telemetry_readings` |
| Incident         | `Incident`         | `incidents`          |
| Alert            | `Alert`            | `alerts`             |

## Domain Services

### TelemetryAnalysisService

Ansvar:

* Analyse af telemetrydata
* Severity classification
* Incident generation
* Alert creation

### PredictiveMaintenanceService

Ansvar:

* Risk scoring
* Predictive maintenance analyse
* ML prediction
* Generering af predictive incidents

## Aggregate Root

`Incident` fungerer som aggregate root.

Dette sikrer:

* Konsistens mellem incidents og alerts
* Tydelig transaction boundary
* Samlet håndtering af driftshændelser

## Domain Events

Systemet arbejder konceptuelt med følgende domain events:

* `TelemetryReceived`
* `AnomalyDetected`
* `IncidentCreated`
* `AlertCreated`

I MVP’et håndteres disse events primært internt i applikationsflowet.

---

# 5. Tech Stack

| Teknologi       | Formål                 |
| --------------- | ---------------------- |
| Python          | Backend udvikling      |
| FastAPI         | REST API               |
| SQLAlchemy      | ORM                    |
| MySQL           | Operationel database   |
| Docker          | Containerisering       |
| Docker Compose  | Lokal orchestration    |
| Power BI        | Analytics & dashboards |
| GitHub Actions  | CI/CD                  |
| Pytest          | Testing                |
| Swagger/OpenAPI | API dokumentation      |

---

# 6. Funktionalitet

## Implementeret funktionalitet

### Charger Monitoring

* Overvågning af ladestandere
* Realtime telemetry ingestion
* Status tracking
* Temperature monitoring
* Voltage/current/power monitoring

### Incident Detection

* Automatisk fejlidentifikation
* Severity classification
* Incident generation
* Predictive maintenance alerts

### Operational Alerting

* Alert generation
* Severity levels
* Incident linking
* Timestamp tracking

### Analytics

* Power BI dashboards
* Incident statistics
* Charger uptime analysis
* Temperature monitoring
* Predictive maintenance insights

---

# 7. API Endpoints

## Base URL

```text
http://localhost:8000
```

## Swagger Documentation

```text
http://localhost:8000/docs
```

---

## Telemetry

### POST /telemetry

Indsender telemetrydata fra en charger.

### Example Request

```json
{
  "charger_id": 1,
  "voltage": 400,
  "current": 32,
  "power": 22,
  "temperature": 95,
  "status": "FAULTED",
  "error_code": "OVERHEAT"
}
```

---

## Chargers

### GET /chargers

Returnerer alle chargers.

### GET /chargers/{id}

Returnerer specifik charger.

---

## Incidents

### GET /incidents

Returnerer alle incidents.

### GET /incidents/{id}

Returnerer specifikt incident.

---

## Alerts

### GET /alerts

Returnerer alle alerts.

### GET /alerts/{id}

Returnerer specifik alert.

---

## Analytics

### GET /analytics

Returnerer analytics data.

---

# 8. Database

Systemet anvender MySQL som operationel database.

## Centrale tabeller

| Tabel              | Formål               |
| ------------------ | -------------------- |
| chargers           | Ladestandere         |
| telemetry_readings | Telemetry data       |
| incidents          | Driftshændelser      |
| alerts             | Operationelle alerts |

## Datamodel

Telemetrydata lagres og analyseres operationelt.

Data bruges efterfølgende i:

* Predictive maintenance
* Incident detection
* Analytics
* Power BI dashboards

---

# 9. Power BI Analytics

Projektet inkluderer Power BI dashboards til visualisering af operationelle data.

## Dashboard metrics

* Total incidents
* Charger uptime
* Severity distribution
* Temperature trends
* Predictive maintenance alerts
* Average risk score

## Formål

Power BI anvendes til:

* Driftsoverblik
* KPI-monitorering
* Historisk analyse
* Predictive insights
* Beslutningsstøtte

---

# 10. Docker Setup

Projektet køres via Docker Compose.

## Start systemet

```bash
docker compose up --build
```

## Stop systemet

```bash
docker compose down
```

## Services

| Service | Port |
| ------- | ---- |
| FastAPI | 8000 |
| MySQL   | 3306 |

---

# 11. Lokal installation

## Clone repository

```bash
git clone https://github.com/jakobdyhrberg-max/voltedge-mvp.git
```

## Gå ind i projektet

```bash
cd voltedge-mvp
```

## Start løsningen

```bash
docker compose up --build
```

---

# 12. Testing

Projektet anvender Pytest til automatiseret testing.

## Kør tests

```bash
pytest
```

## Testtyper

* Unit tests
* API tests
* Service tests
* Validation tests

Testing anvendes som en del af CI/CD pipeline.

---

# 13. CI/CD

Projektet anvender GitHub Actions som CI/CD platform.

## Pipeline indeholder

* Dependency installation
* Automated testing
* Build validation
* Docker workflow

## Formål

CI/CD understøtter:

* Hurtigere feedback
* Stabilitet
* Kvalitetssikring
* Reduceret fejlrisiko
* Reproducerbare builds

---

# 14. Security

MVP’et anvender en simpel API-key mekanisme til autentifikation.

## Security features

* API key validation
* Environment variables
* Container isolation
* Input validation via Pydantic

## MVP-afgrænsning

I en produktionsløsning ville følgende blive implementeret:

* OAuth2 / OpenID Connect
* Azure Key Vault / Secrets Manager
* Centralized identity management
* Rate limiting
* SIEM integration
* Distributed tracing

---

# 15. Observability & Drift

Projektet adresserer observability som et centralt strategisk problem.

## Driftshensyn

* Structured logging
* Incident generation
* Alerting
* Error handling
* Containerized deployment

## Fremtidige forbedringer

* Prometheus metrics
* Grafana dashboards
* Distributed tracing
* Centralized logging
* Kubernetes deployment
* Autoscaling

---

# 16. Predictive Maintenance

Løsningen inkluderer en simpel predictive maintenance model.

## Model

MVP’et anvender:

* Rule-based risk scoring
* Simpel Logistic Regression prediction

## Analyseparametre

* Temperatur
* Voltage
* Current
* Power
* Error codes

## Formål

Predictive maintenance anvendes til:

* Tidlig fejlidentifikation
* Reduceret downtime
* Forbedret oppetid
* Datadrevne operationer

---

# 17. Demo Flow

Følgende flow kan anvendes til demo.

## Step 1 – Start systemet

```bash
docker compose up --build
```

---

## Step 2 – Åbn Swagger UI

```text
http://localhost:8000/docs
```

---

## Step 3 – Send normal telemetry

Indsend telemetry med normal temperatur og status.

Resultat:

* Telemetry gemmes
* Ingen incidents genereres

---

## Step 4 – Send fault telemetry

Indsend telemetry med:

* Høj temperatur
* Faulted status
* Error code

Resultat:

* Incident oprettes
* Alert genereres
* Severity klassificeres
* Risk score beregnes

---

## Step 5 – Se incidents og alerts

Brug:

```text
GET /incidents
GET /alerts
```

---

## Step 6 – Åbn Power BI dashboard

Visualiser:

* Incidents
* Alerts
* Charger health
* Predictive maintenance trends

---

# 18. MVP Scope og afgrænsning

Projektet er bevidst afgrænset til ét bounded context.

Følgende områder er uden for MVP scope:

* Billing & settlement
* Roaming agreements
* Fleet management
* Smart charging orchestration
* Multi-region deployment
* Full event-driven microservices

Dette valg er truffet for at sikre:

* Tydeligt domænefokus
* Konsistent ubiquitous language
* Realistisk implementering
* Lavere arkitektonisk kompleksitet

---

# 19. Fremtidig videreudvikling

Mulige næste skridt:

* Event-driven architecture
* Kafka / RabbitMQ
* Kubernetes deployment
* Multi-tenant architecture
* Real ML model training
* Streaming analytics
* Advanced observability
* Azure cloud deployment
* OCPP integration
* Load forecasting

---

# 20. Repository Struktur

```text
voltedge-mvp/
│
├── app/
├── tests/
├── .github/workflows/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 21. Formål med projektet

Projektets formål er at demonstrere:

* Strategisk alignment
* Domain Driven Design
* Cloud-native arkitektur
* Data-driven services
* DevSecOps principper
* Operationel observability
* Analytics og visualisering

Projektet er udviklet som en realistisk MVP der kobler strategi, arkitektur, data og drift i én samlet digital løsning.

---

# 22. Links

## GitHub Repository

```text
https://github.com/jakobdyhrberg-max/voltedge-mvp
```

---

# 23. Bilag og dokumentation

Projektet understøttes af:

* Eksamenrapport
* Arkitekturdiagrammer
* Domain model
* Capability map
* Power BI dashboards
* CI/CD workflows
* Docker setup
* Test suite

---

# 24. Konklusion

VoltEdge Charger Monitoring MVP demonstrerer hvordan Domain Driven Design, dataanalyse og cloud-native principper kan anvendes til at udvikle en skalerbar og driftssikker overvågningsplatform til EV-ladeinfrastruktur.

Projektet etablerer et operationelt fundament for:

* Realtime observability
* Incident management
* Predictive maintenance
* Data-driven services

og understøtter dermed VoltEdges strategiske ambition om at udvikle sig fra platform-operatør til platform-first partner i mobilitetsøkosystemet.