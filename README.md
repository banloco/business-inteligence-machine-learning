# E‑Commerce Data Strategy (Olist) — BI & ML

## Objectif
Construire un pipeline data complet (Bronze → Silver → Gold) pour transformer les données e‑commerce Olist en indicateurs BI et en analyses prédictives (RFM + churn). Le projet vise à rendre les insights actionnables pour les équipes marketing et produit.

## Stack
- Python (pandas, scikit-learn, SQLAlchemy)
- PostgreSQL (Docker)
- dbt (modèles et tests)
- Streamlit (dashboard simple)

## Architecture
1. **Bronze (Raw)** : chargement des CSV dans PostgreSQL via [scripts/load_data.py](scripts/load_data.py).
2. **Silver (Staging)** : normalisation/typage avec dbt.
3. **Gold (Business)** : tables analytiques dans le schéma analytics.
4. **Analytics** :
	- Segmentation RFM via [scripts/rfm_analysis.py](scripts/rfm_analysis.py).
	- Modèle de churn (RandomForest) via [scripts/churn_prediction.py](scripts/churn_prediction.py).

## Démarrage rapide
### 1) Lancer PostgreSQL
```bash
docker compose up -d
```

### 2) Installer les dépendances Python
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Charger les données brutes
```bash
python scripts/load_data.py
```

### 4) Exécuter dbt
```bash
cd dbt_project
dbt deps
dbt seed
dbt run
dbt test
```

### 5) Lancer les analyses avancées
```bash
python scripts/rfm_analysis.py
python scripts/churn_prediction.py
```

### 6) Dashboard Streamlit (optionnel)
```bash
streamlit run scripts/dashboard.py
```

## Résultats produits
- Table analytics.rfm_segmentation (segments RFM)
- Graphe d’importance des variables : scripts/churn_importance_plot.png
- Visuals BI disponibles dans dashboards/

## Structure du projet
```
├── data/                      # CSV Olist
├── dbt_project/               # Modèles dbt (staging + marts)
├── scripts/
│   ├── load_data.py           # Ingestion CSV → Postgres
│   ├── rfm_analysis.py        # Segmentation RFM
│   ├── churn_prediction.py    # Modèle de churn
│   └── dashboard.py           # Dashboard Streamlit
├── dashboards/                # Captures BI
├── docker-compose.yml         # Postgres local
├── requirements.txt
└── README.md
```

## Dataset
Olist Brazilian E‑Commerce Dataset (Kaggle).