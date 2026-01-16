import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# 1. Connexion et récupération des données
engine = create_engine("postgresql://analyst:password123@localhost:5432/olist_ecommerce")

# On récupère les données de la table Gold créée par dbt et enrichie par RFM
query = """
    SELECT * FROM analytics.rfm_segmentation
"""
df = pd.read_sql(query, engine)

# 2. Définition de la Target (Ex : Churn = pas d'achat depuis plus de 90 jours)
# On simule le churn basé sur la récence pour l'exercice
df['is_churned'] = (df['recency'] > 90).astype(int)

# 3. Préparation des Features (Variables explicatives)
X = df[['frequency', 'monetary']] # On peut ajouter d'autres colonnes si disponibles
y = df['is_churned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entraînement du modèle
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 5. Évaluation et Logs
y_pred = model.predict(X_test)

print("--- RAPPORT DE CLASSIFICATION ---")
print(classification_report(y_test, y_pred))

# 6. Sauvegarde du graphique d'importance pour ton futur README
plt.figure(figsize=(10, 6))
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.title('Importance des variables dans la prédiction du Churn')
plt.savefig('churn_importance_plot.png') # Sauvegarde dans le dossier scripts
print("✅ Graphique sauvegardé dans scripts/churn_importance_plot.png")