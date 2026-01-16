import pandas as pd
from sqlalchemy import create_engine
import datetime as dt

# 1. Connexion
engine = create_engine("postgresql://analyst:password123@localhost:5432/olist_ecommerce")
df = pd.read_sql("SELECT customer_id, purchased_at, total_amount FROM analytics.fct_orders", engine)
df['purchased_at'] = pd.to_datetime(df['purchased_at'])

# On définit une date de référence (le lendemain du dernier achat du dataset)
NOW = df['purchased_at'].max() + dt.timedelta(days=1)

# 2. Calcul des valeurs RFM
rfm = df.groupby('customer_id').agg({
    'purchased_at': lambda x: (NOW - x.max()).days, # Récence
    'customer_id': 'count',                         # Fréquence
    'total_amount': 'sum'                           # Montant
})

rfm.columns = ['recency', 'frequency', 'monetary']

# 3. Attribution des scores (de 1 à 5)
# Plus la récence est faible, plus le score est haut (5)
rfm['R_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
# Pour la fréquence, on gère les doublons, car beaucoup de clients n'ont qu'1 achat
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_score'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

# 4. Score final combiné
rfm['rfm_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

print(rfm.head())

# 5. Définition des segments avec Regex
segs = {
    r'[1-2][1-2]': 'Hibernants',
    r'[1-2][3-4]': 'À risque',
    r'[1-2]5': 'On ne peut pas les perdre',
    r'3[1-2]': 'À surveiller',
    r'33': 'Nécessitent une attention',
    r'[3-4][4-5]': 'Clients fidèles',
    r'41': 'Prometteurs',
    r'51': 'Nouveaux clients',
    r'[4-5][2-3]': 'Potentiels fidèles',
    r'5[4-5]': 'Champions'
}

# On applique le mapping sur les scores Récence et Fréquence
rfm['Segment'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str)
rfm['Segment'] = rfm['Segment'].replace(segs, regex=True)

# 6. Aperçu du résultat
print(rfm['Segment'].value_counts())

# On renvoie le résultat dans un nouveau schéma 'gold'
rfm.to_sql('rfm_segmentation', engine, schema='analytics', if_exists='replace')
print("✅ Segmentation exportée avec succès dans le schéma 'analytics' !")